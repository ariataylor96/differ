from time import time

from .app import app, cache
from .db import Token
from .utils import check_authentication, get_repo, get_commit_before, get_file_changes

from flask import request


@cache.memoize(timeout=30)
def _is_authenticated(key):
    if key is None:
        return False

    return Token.select().where(Token.value == key).exists()


@app.route("/")
def index():
    if not check_authentication():
        return {}, 403

    required_keys = ["repo", "file", "last_updated"]

    for key in required_keys:
        if key not in request.args:
            return {"error": f"{key} is a required parameter"}, 400

    repo_url: str = request.args["repo"]
    file_name: str = request.args["file"]
    last_timestamp: int = int(request.args["last_updated"])

    repo = get_repo(repo_url)
    repo.remotes.origin.pull()

    previous_head = get_commit_before(repo, last_timestamp)
    current = repo.head.commit

    changes = get_file_changes(previous_head, current, file_name)

    return changes
