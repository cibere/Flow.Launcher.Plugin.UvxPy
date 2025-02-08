from __future__ import annotations

from typing import TYPE_CHECKING, Any, Unpack

from flogin import Result, ResultConstructorKwargs

if TYPE_CHECKING:
    from ..plugin import UvxPyPlugin
else:
    UvxPyPlugin = Any


class ListEntryResult(Result[UvxPyPlugin]):
    def __init__(
        self, tool_name: str, **kwargs: Unpack[ResultConstructorKwargs]
    ) -> None:
        self.tool_name = tool_name
        super().__init__(**kwargs)

    async def context_menu(self):
        return []

        """
        This code will only work with 1.20.0 whenever that gets released
        """

        from .uninstall_result import UninstallResult
        from .upgrade_result import UpgradeResult

        return [
            UninstallResult(self.tool_name, title="Uninstall"),
            UpgradeResult(self.tool_name, title="Upgrade"),
        ]
