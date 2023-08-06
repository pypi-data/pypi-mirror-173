# Copyright 2022 The Feathub Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from datetime import timedelta
from pathlib import Path

from feathub.feature_tables.sinks.file_system_sink import FileSystemSink

from feathub.feature_tables.sources.file_system_source import FileSystemSource

from feathub.feature_views.feature_view import FeatureView
from feathub.table.schema import Schema

sys.path.append(str(Path(__file__).parent.parent.parent.resolve()))

from feathub.feature_views.feature import Feature
from feathub.common import types
from feathub.feathub_client import FeathubClient
from feathub.feature_views.transforms.over_window_transform import (
    OverWindowTransform,
)
from feathub.feature_views.transforms.agg_func import AggFunc
from feathub.feature_views.derived_feature_view import DerivedFeatureView


def main() -> None:
    client = FeathubClient(
        config={
            "processor": {
                "processor_type": "flink",
                "flink": {
                    "deployment_mode": "kubernetes-application",
                    "flink.containerized.master.env.ENABLE_BUILT_IN_PLUGINS": "flink-s3-fs-hadoop-1.15.2.jar",  # noqa
                    "flink.containerized.taskmanager.env.ENABLE_BUILT_IN_PLUGINS": "flink-s3-fs-hadoop-1.15.2.jar",  # noqa
                    "flink.s3.endpoint": "http://minio:9000",
                    "flink.s3.path.style.access": "true",
                    "flink.s3.access-key": "flinkfeathub",
                    "flink.s3.secret-key": "flinkfeathub",
                },
            },
            "online_store": {
                "memory": {},
            },
            "registry": {
                "registry_type": "local",
                "local": {
                    "namespace": "default",
                },
            },
            "feature_service": {
                "service_type": "local",
                "local": {},
            },
        }
    )

    # Define features as transformations on the file_feature_table dataset
    features = build_features(client)

    # Transform features into Pandas DataFrame for offline training.
    client.materialize_features(
        features,
        FileSystemSink("s3://flink/output.json", "json"),
        allow_overwrite=True,
    ).wait()


def build_features(client: FeathubClient) -> FeatureView:
    # source_file_path = "https://azurefeathrstorage.blob.core.windows.net/public" \
    #                    "/sample_data/green_tripdata_2020-04_with_index.csv"

    source_file_path = "s3://flink/sample_data.csv"

    schema = Schema(
        field_names=[
            "trip_id",
            "VendorID",
            "lpep_pickup_datetime",
            "lpep_dropoff_datetime",
            "store_and_fwd_flag",
            "RatecodeID",
            "PULocationID",
            "DOLocationID",
            "passenger_count",
            "trip_distance",
            "fare_amount",
            "extra",
            "mta_tax",
            "tip_amount",
            "tolls_amount",
            "ehail_fee",
            "improvement_surcharge",
            "total_amount",
            "payment_type",
            "trip_type",
            "congestion_surcharge",
        ],
        field_types=[
            types.Int64,
            types.Float64,
            types.String,
            types.String,
            types.String,
            types.Float64,
            types.Int64,
            types.Int64,
            types.Float64,
            types.Float64,
            types.Float64,
            types.Float64,
            types.Float64,
            types.Float64,
            types.Float64,
            types.Float64,
            types.Float64,
            types.Float64,
            types.Float64,
            types.Float64,
            types.Float64,
        ],
    )

    source = FileSystemSource(
        name="source_1",
        path=source_file_path,
        data_format="csv",
        timestamp_field="lpep_dropoff_datetime",
        timestamp_format="%Y-%m-%d %H:%M:%S",
        schema=schema,
    )

    f_trip_time_duration = Feature(
        name="f_trip_time_duration",
        dtype=types.Int32,
        transform="UNIX_TIMESTAMP(CAST(lpep_dropoff_datetime AS STRING)) - "
        "UNIX_TIMESTAMP(CAST(lpep_pickup_datetime AS STRING))",
    )

    # f_trip_distance = Feature(
    #     name="f_trip_distance", dtype=types.Float32, transform="trip_distance"
    # )
    #
    # f_day_of_week = Feature(
    #     name="f_day_of_week",
    #     dtype=types.Int32,
    #     transform="dayofweek(lpep_dropoff_datetime)",
    # )
    #
    # f_trip_time_distance = Feature(
    #     name="f_trip_time_distance",
    #     dtype=types.Float32,
    #     transform="trip_distance * f_trip_duration",
    #     input_features=[f_trip_distance, f_trip_time_duration],
    # )

    f_location_avg_fare = Feature(
        name="f_location_avg_fare",
        dtype=types.Float32,
        transform=OverWindowTransform(
            expr="cast(fare_amount AS float)",
            agg_func=AggFunc.AVG,
            group_by_keys=["DOLocationID"],
            window_size=timedelta(days=90),
        ),
    )

    f_location_max_fare = Feature(
        name="f_location_max_fare",
        dtype=types.Float32,
        transform=OverWindowTransform(
            expr="cast(fare_amount AS float)",
            agg_func=AggFunc.MAX,
            group_by_keys=["DOLocationID"],
            window_size=timedelta(days=90),
        ),
    )

    f_location_total_fare_cents = Feature(
        name="f_location_total_fare_cents",
        dtype=types.Float32,
        transform=OverWindowTransform(
            expr="cast(fare_amount * 100 as float)",
            agg_func=AggFunc.SUM,
            group_by_keys=["DOLocationID"],
            window_size=timedelta(days=90),
        ),
    )

    feature_view_1 = DerivedFeatureView(
        name="feature_view_1",
        source=source,
        features=[
            f_location_avg_fare,
            f_location_max_fare,
            f_location_total_fare_cents,
        ],
        keep_source_fields=True,
    )

    f_trip_time_rounded = Feature(
        name="f_trip_time_rounded",
        dtype=types.Float32,
        transform="f_trip_time_duration / 10",
        input_features=[f_trip_time_duration],
    )

    f_is_long_trip_distance = Feature(
        name="f_is_long_trip_distance",
        dtype=types.Bool,
        transform="cast(trip_distance as float)>30",
    )

    feature_view_2 = DerivedFeatureView(
        name="feature_view_2",
        source="feature_view_1",
        features=[
            "f_location_avg_fare",
            f_trip_time_rounded,
            f_is_long_trip_distance,
            "f_location_total_fare_cents",
        ],
        keep_source_fields=True,
    )

    client.build_features(features_list=[feature_view_1, feature_view_2])

    return feature_view_2


if __name__ == "__main__":
    main()
