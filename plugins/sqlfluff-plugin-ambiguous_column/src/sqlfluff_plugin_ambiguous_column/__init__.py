"""An example of a custom rule implemented through the plugin system.

This uses the rules API supported from 0.4.0 onwards.
"""

from typing import Any, Dict, List, Type

from sqlfluff.core.config import load_config_resource
from sqlfluff.core.plugin import hookimpl
from sqlfluff.core.rules import BaseRule

# For backward compatibility we still support importing
# rules within the body of the root plugin module. This is included
# here for illustration, but also such that support for this import
# order can be tested in the test suite (and that the associated
# warning is triggered).
# See note below in `get_rules()` for more details.
# i.e. we DO NOT recommend importing here:
from sqlfluff_plugin_ambiguous_column.ambiguous_column import Rule_Green_L033  # noqa: F401


@hookimpl
def get_rules() -> List[Type[BaseRule]]:
    """Get plugin rules.
    """
    # i.e. we DO recommend importing here:
    from sqlfluff_plugin_ambiguous_column.ambiguous_column import Rule_Green_L033  # noqa: F811

    return [Rule_Green_L033]

@hookimpl
def load_default_config() -> Dict[str, Any]:
    """Loads the default configuration for the plugin."""
    return load_config_resource(
        package="sqlfluff_plugin_ambiguous_column",
        file_name="plugin_default_config.cfg",
    )


@hookimpl
def get_configs_info() -> Dict[str, Dict[str, Any]]:
    """Get rule config validations and descriptions."""
    return {
        "forbidden_columns": {"definition": "A list of column to forbid"},
    }

