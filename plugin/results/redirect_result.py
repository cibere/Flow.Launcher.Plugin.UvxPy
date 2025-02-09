from __future__ import annotations

from typing import TYPE_CHECKING, Any, Unpack

from flogin import Result, ResultConstructorKwargs

if TYPE_CHECKING:
    from ..plugin import UvxPyPlugin
else:
    UvxPyPlugin = Any


class RedirectResult(Result[UvxPyPlugin]):
    def __init__(
        self, new_query: str, **kwargs: Unpack[ResultConstructorKwargs]
    ) -> None:
        self.new_query = new_query
        kwargs["auto_complete_text"] = new_query
        super().__init__(**kwargs)

    async def callback(self) -> bool:
        assert self.plugin
        assert self.plugin.last_query

        await self.plugin.api.change_query(self.new_query)
        return False
