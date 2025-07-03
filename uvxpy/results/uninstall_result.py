from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flogin import Result

from .base import BaseResult

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


class UninstallResult(BaseResult):
    async def actual_callback(self) -> AsyncGenerator[Any, Result]:
        assert self.plugin

        _, response = await self.plugin.uvx("uninstall", self.tool_name)

        yield Result(response.strip(), icon="assets/app.png")
