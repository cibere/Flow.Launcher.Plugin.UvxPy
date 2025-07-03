from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flogin import Result

from .base import BaseResult

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


class UpgradeResult(BaseResult):
    async def actual_callback(self) -> AsyncGenerator[Any, Result]:
        assert self.plugin

        _, response = await self.plugin.uvx("upgrade", self.tool_name)

        for line in response.splitlines():
            line = line.strip()

            if not line.startswith(("-", "+")):
                yield Result(line, icon="assets/app.png")
