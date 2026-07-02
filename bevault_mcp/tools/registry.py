import importlib
import inspect
import logging
import pkgutil
from types import ModuleType
from typing import Callable

from fastmcp import FastMCP

from ..client import BeVaultClient

logger = logging.getLogger(__name__)


def register_metavault_tools_fastmcp(mcp: FastMCP, client: BeVaultClient) -> None:
    """Register MetaVault module tools with FastMCP instance."""
    package = __package__  # "bevault_mcp.tools"
    package_module = importlib.import_module(package)
    package_path = package_module.__path__  # type: ignore[attr-defined]

    for module_info in pkgutil.iter_modules(package_path, package + "."):
        short_name = module_info.name.rsplit(".", 1)[-1]
        if short_name in ("states", "registry"):
            continue
        module = importlib.import_module(module_info.name)
        _try_register_module_fastmcp(module, mcp, client)


def _try_register_module_fastmcp(
    module: ModuleType, mcp: FastMCP, client: BeVaultClient
) -> None:
    """Try to register tools from a module using FastMCP."""
    register: Callable | None = getattr(module, "register_fastmcp", None)
    if register and inspect.isfunction(register):
        register(mcp, client)
    elif hasattr(module, "register"):
        register_legacy: Callable | None = getattr(module, "register", None)
        if register_legacy and inspect.isfunction(register_legacy):
            if module.__name__ != "bevault_mcp.tools.example":
                logger.warning(
                    "Module %s uses legacy register() function. "
                    "Consider migrating to register_fastmcp()",
                    module.__name__,
                )
