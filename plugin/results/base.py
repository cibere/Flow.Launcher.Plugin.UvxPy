from __future__ import annotations

from typing import TYPE_CHECKING, Any, Unpack

from flogin import Result, ResultConstructorKwargs

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from ..plugin import UvxPyPlugin
else:
    UvxPyPlugin = Any


class BaseResult(Result[UvxPyPlugin]):
    def __init__(
        self, tool_name: str, **kwargs: Unpack[ResultConstructorKwargs]
    ) -> None:
        self.tool_name = tool_name
        super().__init__(**kwargs)

    async def actual_callback(self) -> AsyncGenerator[Any, Result]:
        yield

    async def callback(self) -> bool:
        assert self.plugin
        assert self.plugin.last_query

        results = [res async for res in self.actual_callback()]
        await self.plugin.last_query.update_results(results)

        return False
