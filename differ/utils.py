import difflib
import os

from flask import request
import git

from . import env
from .app import cache
from .constants import REPO_DIRECTORY
from .db import Token


@cache.memoize(timeout=30)
def _key_is_valid(key: str) -> bool:
    if env("FLASK_ENV", default="prod") == "development":
        return True

    if key is None:
        return False

    return Token.select().where(Token.value == key).exists()


def check_authentication() -> bool:
    key = request.headers.get("X-Token")

    return _key_is_valid(key)


def repo_name_from_url(repo_url: str) -> str:
    return repo_url.split("/")[-1].replace(".git", "")


def get_repo(repo_url: str) -> git.Repo:
    repo_name: str = repo_name_from_url(repo_url)
    repo_path: str = os.path.join(REPO_DIRECTORY, repo_name)

    if os.path.exists(repo_path):
        return git.Repo(repo_path)

    return git.Repo.clone_from(repo_url, repo_path)


def get_commit_before(repo, date) -> git.Commit:
    last_commit = None
    for commit in repo.iter_commits():
        last_commit = commit

        if commit.committed_date <= date:
            return commit
    return last_commit


def _blob_to_arr(blob) -> list[str]:
    return [line.rstrip() for line in blob.data_stream.read().decode().split("\n")]


@cache.memoize(timeout=60)
def get_file_changes(
    previous: git.Commit,
    current: git.Commit,
    file_path,
) -> dict[str, list[str]]:
    differ = difflib.Differ()
    git_diff = current.diff(previous, paths=file_path)
    default_ret = {"added": [], "removed": []}

    # If we have no diff, give no information
    if len(git_diff) == 0:
        return default_ret

    git_diff = git_diff[0]
    if git_diff.a_blob is None and git_diff.b_blob is None:
        return default_ret

    # A-blob is current, B-blob is past

    # If the file did not exist and now it does, all lines are added
    if git_diff.a_blob is not None and git_diff.b_blob is None:
        return {"added": _blob_to_arr(git_diff.a_blob), "removed": []}

    # If the file did exist but now it doesn't, all lines are removed
    if git_diff.b_blob is not None and git_diff.a_blob is None:
        return {"removed": _blob_to_arr(git_diff.b_blob), "added": []}

    # Otherwise, we need to actually run a diff
    a_lines = _blob_to_arr(git_diff.a_blob)
    b_lines = _blob_to_arr(git_diff.b_blob)

    results = differ.compare(b_lines, a_lines)

    added = set()
    removed = set()

    for line in results:
        operand = line[0]
        data = line[2:]

        if operand == "-":
            if data in added:
                added.remove(data)
                continue

            removed.add(data)

        if operand == "+":
            if data in removed:
                removed.remove(data)
                continue

            added.add(data)

    return {"added": list(added), "removed": list(removed)}
