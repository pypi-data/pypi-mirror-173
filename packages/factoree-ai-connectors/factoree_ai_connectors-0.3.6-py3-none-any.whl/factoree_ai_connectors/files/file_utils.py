from datetime import datetime

from factoree_ai_connectors.common.system_params import SEPARATOR_CHAR, PATH_SEPARATOR_CHAR


def get_silver_file_name(
        data_type: str,
        facility: str,
        sensor_type: str,
        first_sample: datetime,
        last_sample: datetime,
        is_test: bool = False,
) -> str:
    first_sample_display = first_sample.strftime("%Y_%m_%dT%H_%M_%S%z").replace("+", "_")
    last_sample_display = last_sample.strftime("%Y_%m_%dT%H_%M_%S%z").replace("+", "_")
    folder = 'tests' if is_test else 'input'

    file_base_name = SEPARATOR_CHAR.join([
        facility,
        sensor_type,
        first_sample_display,
        last_sample_display
    ])
    file_name = f'{file_base_name}.json'

    return PATH_SEPARATOR_CHAR.join([
        folder,
        data_type,
        file_name
    ])
