import asyncio
import shlex
from typing import Tuple

import config
from ..logging import LOGGER


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())


# ================= FIXED GIT FUNCTION =================
def git():
    try:
        from git import Repo
        from git.exc import GitCommandError, InvalidGitRepositoryError
    except Exception:
        LOGGER(__name__).info("❌ GitPython or git not available, skipping...")
        return

    REPO_LINK = config.UPSTREAM_REPO

    if config.GIT_TOKEN:
        try:
            GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
            TEMP_REPO = REPO_LINK.split("https://")[1]
            UPSTREAM_REPO = f"https://{GIT_USERNAME}:{config.GIT_TOKEN}@{TEMP_REPO}"
        except Exception:
            UPSTREAM_REPO = REPO_LINK
    else:
        UPSTREAM_REPO = REPO_LINK

    try:
        repo = Repo()
        LOGGER(__name__).info("✅ Git Repo Found")
        return

    except InvalidGitRepositoryError:
        LOGGER(__name__).info("⚠️ Not a git repo, skipping init")
        return

    except GitCommandError:
        LOGGER(__name__).info("⚠️ Git command error, skipping")
        return

    except Exception:
        LOGGER(__name__).info("⚠️ Git not supported on this environment (Heroku)")
        return
