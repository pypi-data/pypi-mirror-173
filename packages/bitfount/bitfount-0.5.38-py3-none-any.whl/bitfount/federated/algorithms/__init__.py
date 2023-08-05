"""Algorithms for remote processing of data.

Federated algorithm plugins can also be imported from this package.
"""
import pkgutil as _pkgutil

from bitfount.config import (
    BITFOUNT_FEDERATED_PLUGIN_PATH as _BITFOUNT_FEDERATED_PLUGIN_PATH,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.utils import _get_module_from_file

_logger = _get_federated_logger(__name__)


# Create `algorithms` plugin subdir if it doesn't exist
_algorithms_plugin_path = _BITFOUNT_FEDERATED_PLUGIN_PATH / "algorithms"
_algorithms_plugin_path.mkdir(parents=True, exist_ok=True)


def _log_import_error(pkg: str) -> None:
    _logger.error(f"Issue importing {pkg}")


# Add algorithms plugin modules to the `algorithms` namespace alongside the existing
# built-in algorithms modules. This is not essential, but it allows users to import
# the entire plugin module as opposed to just the built-in class which is what is done
# in the `bitfount.federated` __init__ module.
for _module_info in _pkgutil.walk_packages(
    [str(_algorithms_plugin_path)],
):
    try:
        _module = _get_module_from_file(
            _algorithms_plugin_path / f"{_module_info.name}.py"
        )
        globals().update({_module.__name__: _module})
        _logger.info(f"Loaded algorithms plugin: {_module_info.name}")
    except ImportError:
        pass
