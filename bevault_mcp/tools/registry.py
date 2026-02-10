import importlib
import inspect
import logging
import pkgutil
from types import ModuleType
from typing import Callable

from fastmcp import FastMCP

from ..client import BeVaultClient

logger = logging.getLogger(__name__)


def register_all_tools_fastmcp(mcp: FastMCP, client: BeVaultClient) -> None:
    """Register all tools with FastMCP instance"""
    package = __package__  # "bevault_mcp.tools"
    # Import the package module to access __path__
    package_module = importlib.import_module(package)
    package_path = package_module.__path__  # type: ignore[attr-defined]
    
    for module_info in pkgutil.iter_modules(package_path, package + "."):
        module = importlib.import_module(module_info.name)
        _try_register_module_fastmcp(module, mcp, client)


def _try_register_module_fastmcp(module: ModuleType, mcp: FastMCP, client: BeVaultClient) -> None:
    """Try to register tools from a module using FastMCP"""
    register: Callable | None = getattr(module, "register_fastmcp", None)
    if register and inspect.isfunction(register):
        register(mcp, client)
    # Also check for legacy register function for backward compatibility
    elif hasattr(module, "register"):
        register_legacy: Callable | None = getattr(module, "register", None)
        if register_legacy and inspect.isfunction(register_legacy):
            # Skip example.py and other modules that don't need registration
            if module.__name__ != "bevault_mcp.tools.example":
                logger.warning(
                    "Module %s uses legacy register() function. "
                    "Consider migrating to register_fastmcp()",
                    module.__name__,
                )


