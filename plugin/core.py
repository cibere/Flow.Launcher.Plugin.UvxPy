import re

from flogin import Glyph, Query
from flogin.utils import print

from .plugin import UvxPyPlugin
from .results.install_result import InstallResult
from .results.list_result_entry import ListEntryResult
from .results.uninstall_result import UninstallResult
from .results.upgrade_result import UpgradeResult

plugin = UvxPyPlugin()


@plugin.search(pattern=r"install\s?(?P<args>.*)?")
async def install_cmd(query: Query[re.Match[str]]):
    assert query.condition_data
    tool_name = query.condition_data["args"]

    return InstallResult(
        tool_name, title=f"Install the {tool_name!r} tool?", glyph=Glyph("?", "Calibri")
    )


@plugin.search(pattern=r"uninstall\s?(?P<args>.*)?")
async def uninstall_cmd(query: Query[re.Match[str]]):
    assert query.condition_data
    tool_name = query.condition_data["args"]

    return UninstallResult(
        tool_name,
        title=f"Uninstall the {tool_name!r} tool?",
        glyph=Glyph("?", "Calibri"),
    )


@plugin.search(pattern=r"upgrade\s(?P<args>.*)?")
async def upgrade_cmd(query: Query[re.Match[str]]):
    assert query.condition_data
    tool_name = query.condition_data["args"]

    return UpgradeResult(
        tool_name, title=f"Upgrade the {tool_name!r} tool?", glyph=Glyph("?", "Calibri")
    )


@plugin.search(pattern=r"upgrade$")
async def upgrade_all_cmd(query: Query[re.Match[str]]):
    return UpgradeResult(
        "--all", title="Upgrade all tools?", glyph=Glyph("?", "Calibri")
    )


@plugin.search(pattern=r"list")
async def list_cmd(query: Query):
    response, _ = await plugin.uvx("list")

    data: dict[str, list[str]] = {}
    temp: list[str] = []
    current = ""

    for line in response.splitlines():
        line = line.strip()

        if line.startswith("-"):
            temp.append(line.strip("- "))
        else:
            if temp:
                data[current] = temp
                temp = []
            current = line
    data[current] = temp

    print(f"{data=}")

    for idx, (name, scripts) in enumerate(data.items()):
        yield ListEntryResult(
            name.split(" ")[0],
            title=name,
            sub=", ".join(scripts),
            glyph=Glyph(str(idx + 1), "Calibri"),
        )
