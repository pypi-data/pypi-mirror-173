import argparse
import json
import shutil
import tempfile

import libcoveofds.api


def main():
    parser = argparse.ArgumentParser(description="Lib Cove OFDS CLI")
    parser.add_argument("filename")
    parser.add_argument(
        "--raw", help="show raw output from the library", action="store_true"
    )

    args = parser.parse_args()

    cove_temp_folder = tempfile.mkdtemp(
        prefix="lib-cove-ofds-cli-", dir=tempfile.gettempdir()
    )
    try:
        result = libcoveofds.api.ofds_json_output(
            cove_temp_folder, args.filename, file_type="json"
        )
    finally:
        shutil.rmtree(cove_temp_folder)

    if not args.raw:
        del result["json_data"]

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
