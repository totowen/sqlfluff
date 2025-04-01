"""An example of a custom rule implemented through the plugin system.

This uses the rules API supported from 0.4.0 onwards.
"""

from typing import Any, Dict, List, Type

from sqlfluff.core.config import load_config_resource
from sqlfluff.core.plugin import hookimpl
from sqlfluff.core.rules import BaseRule


@hookimpl
def get_rules() -> List[Type[BaseRule]]:
    """Get plugin rules.
    """
    # i.e. we DO recommend importing here:
    from sqlfluff_plugin_limit_left_joins.limit_left_joins import Rule_Green_L041  # noqa: F811

    return [Rule_Green_L041]

@hookimpl
def load_default_config() -> Dict[str, Any]:
    """Loads the default configuration for the plugin."""
    return load_config_resource(
        package="sqlfluff_plugin_limit_left_joins",
        file_name="plugin_default_config.cfg",
    )


@hookimpl
def get_configs_info() -> Dict[str, Dict[str, Any]]:
    """Get rule config validations and descriptions."""
    return {
        "max_left_joins": {
            "definition": "允许的最大LEFT JOIN次数",
            "default": 3
        }
    }

