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
from pathlib import Path

from feathub.feature_tables.sinks.kafka_sink import KafkaSink
from feathub.feature_tables.sources.kafka_source import KafkaSource
from feathub.feature_views.derived_feature_view import DerivedFeatureView
from feathub.feature_views.feature_view import FeatureView
from feathub.table.schema import Schema

sys.path.append(str(Path(__file__).parent.parent.parent.resolve()))

from feathub.feature_views.feature import Feature
from feathub.common import types
from feathub.feathub_client import FeathubClient

bootstrap_servers = (
    "alikafka-post-cn-2r42vqkdq00d-1-vpc.alikafka.aliyuncs.com:9092,"
    "alikafka-post-cn-2r42vqkdq00d-2-vpc.alikafka.aliyuncs.com:9092,"
    "alikafka-post-cn-2r42vqkdq00d-3-vpc.alikafka.aliyuncs.com:9092"
)


def main() -> None:
    client = FeathubClient(
        config={
            "processor": {
                "processor_type": "flink",
                "flink": {},
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
    features = build_features()

    # Transform features into Pandas DataFrame for offline training.
    client.materialize_features(
        features,
        KafkaSink(
            bootstrap_server=bootstrap_servers,
            topic="feathub-demo-output",
            key_format=None,
            value_format="json",
        ),
        allow_overwrite=True,
    ).wait()


def build_features() -> FeatureView:

    schema = Schema(
        field_names=["id", "value", "ts"],
        field_types=[types.Int64, types.Int64, types.String],
    )

    source = KafkaSource(
        name="source_1",
        bootstrap_server=bootstrap_servers,
        topic="feathub-demo-input",
        key_format=None,
        value_format="json",
        schema=schema,
        consumer_group="feathub-demo",
        keys=["id"],
        timestamp_field="ts",
        timestamp_format="%Y-%m-%d %H:%M:%S",
        startup_mode="group-offsets",
        consumer_properties={"auto.offset.reset": "earliest"},
    )

    feature_view = DerivedFeatureView(
        name="feature_view",
        source=source,
        features=[
            Feature(
                name="value_plus_one",
                dtype=types.Int64,
                transform="`value` + 1",
                keys=["id"],
            )
        ],
    )

    return feature_view


if __name__ == "__main__":
    main()
