from asyncio import subprocess

from flogin import Plugin
from flogin.utils import print


class UvxPyPlugin(Plugin):
    async def uvx(self, *args: str) -> tuple[str, str]:
        proc = await subprocess.create_subprocess_exec(
            "uv",
            "tool",
            *args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=0x08000000,
        )
        stdout, stderr = await proc.communicate(None)
        await proc.wait()
        # proc.kill()

        args = stdout.decode(), stderr.decode()
        print(f"{args=}")
        return args
