from __future__ import annotations

from typing import TYPE_CHECKING, Any, Unpack

from flogin import Result, ResultConstructorKwargs

if TYPE_CHECKING:
    from ..plugin import UvxPyPlugin
else:
    UvxPyPlugin = Any


class UrlResult(Result[UvxPyPlugin]):
    def __init__(self, url: str, **kwargs: Unpack[ResultConstructorKwargs]) -> None:
        self.url = url
        super().__init__(**kwargs)

    async def callback(self) -> None:
        assert self.plugin

        await self.plugin.api.open_url(self.url)
