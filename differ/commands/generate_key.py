import argparse

from differ.db import Token


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Unique identifier for the user")
    args = parser.parse_args()

    token = Token.get_or_create(user=args.username)[0]

    print(f"Token for {args.username}: {token.value}")
