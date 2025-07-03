from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from flogin import Glyph, Result
from flogin.utils import print

from .base import BaseResult

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

_resolved_in_package_pattern = re.compile(
    r"^Resolved\s(?P<num>[0-9]+)\spackages?\sin\s(?P<ms>[0-9]+)ms$"
)
_prepared_in_package_pattern = re.compile(
    r"^Prepared\s(?P<num>[0-9]+)\spackages\sin\s(?P<ms>[0-9]+)ms$"
)
_installed_in_package_pattern = re.compile(
    r"^Installed\s(?P<num>[0-9]+)\spackages?\sin\s(?P<ms>[0-9]+)ms$"
)
_added_pck_pattern = re.compile(r"^(?:\s?\+\s(?P<content>.*==.*))$")

MULTIPLICATION_SIGN = "\U000000d7"


class InstallResult(BaseResult):
    async def actual_callback(self) -> AsyncGenerator[Any, Result]:
        assert self.plugin

        _, response = await self.plugin.uvx("install", self.tool_name)
        response = response.strip()
        lines = response.splitlines()

        if response.strip() == f"`{self.tool_name}` is already installed":
            yield Result(response.strip())
            return
        elif lines[0].startswith(MULTIPLICATION_SIGN):
            yield Result(
                lines.pop(0).removeprefix(MULTIPLICATION_SIGN).strip(),
                sub=" ".join(
                    [line.strip().removeprefix("`->").strip() for line in lines]
                ),
                icon="assets/error.png",
            )
            return

        installed_packages = []
        trace_parts = []

        for line in lines:
            line = line.strip()

            print(f"Processing line: {line!r}")

            if line.startswith("warning"):
                yield Result(line, score=100)
            elif match := _added_pck_pattern.match(line):
                installed_packages.append(match["content"])
            elif match := _resolved_in_package_pattern.match(line):
                trace_parts.append(f"Resolved: {match['ms']}ms")
            elif match := _prepared_in_package_pattern.match(line):
                trace_parts.append(f"Prepared: {match['ms']}ms")
            elif match := _installed_in_package_pattern.match(line):
                trace_parts.append(f"Installed: {match['ms']}ms")
            else:
                print(f"Line did not match any pattern: {line!r}")

        assert installed_packages
        assert trace_parts

        yield Result(
            f"Installed {len(installed_packages)} packages",
            sub=", ".join(installed_packages),
            icon="assets/success.png",
        )
        yield Result(
            "Time Trace", sub=" | ".join(trace_parts), glyph=Glyph("🕓", "Calibri")
        )
