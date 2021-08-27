import argparse

from differ.db import Token
from peewee import DoesNotExist


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Unique identifier for the user")
    args = parser.parse_args()

    try:
        token = Token.get(Token.user == args.username)
        token.delete_instance()

        print(f"Token for {args.username} revoked")
    except DoesNotExist:
        print("No such user")
