from libcove.lib.common import SchemaJsonMixin  # type: ignore

from libcoveofds.config import LibCoveOFDSConfig


class SchemaOFDS(SchemaJsonMixin):
    def __init__(
        self, json_data: dict = None, lib_cove_ofds_config: LibCoveOFDSConfig = None
    ):
        lib_cove_ofds_config_object: LibCoveOFDSConfig = (
            lib_cove_ofds_config or LibCoveOFDSConfig()
        )

        self.pkg_schema_url = lib_cove_ofds_config_object.config.get(
            "package_schema_url"
        )
        self.schema_url = lib_cove_ofds_config_object.config.get("schema_url")
        self.schema_version = lib_cove_ofds_config_object.config.get("schema_version")
        self.schema_host = lib_cove_ofds_config_object.config.get("schema_host")

    def get_link_rels_for_external_nodes(self) -> list:
        return [
            "tag:opentelecomdata.net,2022:nodesAPI",
            "tag:opentelecomdata.net,2022:nodesFile",
        ]

    def get_link_rels_for_external_spans(self) -> list:
        return [
            "tag:opentelecomdata.net,2022:spansAPI",
            "tag:opentelecomdata.net,2022:spansFile",
        ]
