import json

from libcove.lib.tools import get_file_type  # type: ignore

from libcoveofds.common_checks import common_checks_ofds
from libcoveofds.config import LibCoveOFDSConfig
from libcoveofds.lib.api import context_api_transform
from libcoveofds.schema import SchemaOFDS


class APIException(Exception):
    pass


def ofds_json_output(
    output_dir: str,
    file: str,
    file_type: str = None,
    json_data: dict = None,
    lib_cove_ofds_config: LibCoveOFDSConfig = None,
) -> dict:

    if not lib_cove_ofds_config:
        lib_cove_ofds_config = LibCoveOFDSConfig()

    if not file_type:
        file_type = get_file_type(file)
    context: dict = {"file_type": file_type}

    if file_type == "json":
        if not json_data:
            with open(file, encoding="utf-8") as fp:
                try:
                    json_data = json.load(fp)
                except ValueError:
                    raise APIException("The file looks like invalid json")

        schema_ofds: SchemaOFDS = SchemaOFDS(
            json_data=json_data, lib_cove_ofds_config=lib_cove_ofds_config
        )

    else:

        raise Exception("JSON only for now, sorry!")

    context["schema_version"] = schema_ofds.schema_version

    context = context_api_transform(
        common_checks_ofds(
            context,
            output_dir,
            json_data,
            schema_ofds,
            lib_cove_ofds_config=lib_cove_ofds_config,
        )
    )

    return context
