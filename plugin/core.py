import re

from flogin import Glyph, Query
from flogin.utils import print

from .plugin import UvxPyPlugin
from .results.install_result import InstallResult
from .results.list_result_entry import ListEntryResult
from .results.redirect_result import RedirectResult
from .results.uninstall_result import UninstallResult
from .results.upgrade_result import UpgradeResult
from .results.url_result import UrlResult

plugin = UvxPyPlugin()


async def _uvx_not_installed_callback(query: Query):
    return UrlResult(
        "https://docs.astral.sh/uv/getting-started/installation/",
        title="uv is either not installed or not added to path",
        icon="assets/error.png",
        sub="click to open installation instructions",
    )


@plugin.event
async def on_initialization():
    try:
        await plugin.uvx()
    except FileNotFoundError:
        plugin._search_handlers.clear()
        plugin.search()(_uvx_not_installed_callback)


@plugin.search(pattern=r"install$")
async def install_cmd_base(query: Query):
    await plugin.api.change_query(query.raw_text + " ")
    return UrlResult(
        "https://docs.astral.sh/uv/reference/cli/#uv-tool-install",
        title="Type the name of the package you want to install",
        icon="assets/app.png",
        sub="Click to open up the docs on the install command",
    )


@plugin.search(pattern=r"install\s(?P<args>.*)")
async def install_cmd(query: Query[re.Match[str]]):
    assert query.condition_data
    tool_name = query.condition_data["args"]

    return InstallResult(
        tool_name, title=f"Install the {tool_name!r} tool?", glyph=Glyph("?", "Calibri")
    )


@plugin.search(pattern=r"uninstall$")
async def uninstall_cmd_base(query: Query):
    await plugin.api.change_query(query.raw_text + " ")
    return UrlResult(
        "https://docs.astral.sh/uv/reference/cli/#uv-tool-uninstall",
        title="Type the name of the package you want to uninstall",
        icon="assets/app.png",
        sub="Click to open up the docs on the uninstall command",
    )


@plugin.search(pattern=r"uninstall\s(?P<args>.*)")
async def uninstall_cmd(query: Query[re.Match[str]]):
    assert query.condition_data
    tool_name = query.condition_data["args"]

    return UninstallResult(
        tool_name,
        title=f"Uninstall the {tool_name!r} tool?",
        glyph=Glyph("?", "Calibri"),
    )


@plugin.search(pattern=r"upgrade$")
async def upgrade_cmd_base(query: Query):
    await plugin.api.change_query(query.raw_text + " ")
    return UrlResult(
        "https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade",
        title="Type the name of the package you want to upgrade",
        icon="assets/app.png",
        sub="Click to open up the docs on the upgrade command",
    )


@plugin.search(pattern=r"upgrade(?P<args>\s.*)")
async def upgrade_cmd(query: Query[re.Match[str]]):
    assert query.condition_data
    tool_name = query.condition_data["args"].strip()

    return UpgradeResult(
        tool_name, title=f"Upgrade the {tool_name!r} tool?", glyph=Glyph("?", "Calibri")
    )


@plugin.search(pattern=r"up-all$")
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


@plugin.search()
async def index_cmd(query: Query):
    yield RedirectResult(
        f"{query.keyword} install ", title="install package", icon="assets/app.png"
    )
    yield RedirectResult(
        f"{query.keyword} uninstall ", title="uninstall package", icon="assets/app.png"
    )
    yield RedirectResult(
        f"{query.keyword} upgrade ", title="upgrade package", icon="assets/app.png"
    )
    yield RedirectResult(
        f"{query.keyword} up-all", title="upgrade all packages", icon="assets/app.png"
    )
    yield RedirectResult(
        f"{query.keyword} list", title="list installed packages", icon="assets/app.png"
    )
