from pathlib import Path
from datetime import datetime, timedelta

import iso8601
from jinja2 import Environment, FileSystemLoader


# Custom Jinja2 filters
def iso8601_to_dt(dt_string):
    return iso8601.parse_date(dt_string)

def datetime_adjust(dt, seconds=0):
    """
    Adjust datetime by adding or subtracting seconds.

    Args:
        dt: datetime object to adjust
        seconds: number of seconds to add (positive) or subtract (negative)

    Returns:
        datetime: adjusted datetime object
    """
    if not isinstance(dt, datetime):
        raise TypeError("First argument must be a datetime object")

    return dt + timedelta(seconds=seconds)


def datetime_to_unix_millis(dt):
    """
    Convert datetime to Unix timestamp in milliseconds.

    Args:
        dt: datetime object to convert

    Returns:
        int: Unix timestamp in milliseconds
    """
    if not isinstance(dt, datetime):
        raise TypeError("Argument must be a datetime object")

    return int(dt.timestamp() * 1000)


# Engine setup.
def load_j2_template_engine(template_file_path: str):
    """ Loads a J2 template engine from given template file path. """
    # Template file
    template_file = Path(template_file_path)

    # Template directory.
    resolved_template_dir_path = template_file.parent.resolve(strict=True)

    # Load J2 environment.
    j2_environment = Environment(
        loader=FileSystemLoader(str(resolved_template_dir_path))
    )

    # Register custom filters
    j2_environment.filters['add_seconds'] = datetime_adjust
    j2_environment.filters['to_unix_millis'] = datetime_to_unix_millis
    j2_environment.filters['dt_from_grafana_ts'] = datetime_to_unix_millis

    # Return template.
    return j2_environment.get_template(template_file.name)
