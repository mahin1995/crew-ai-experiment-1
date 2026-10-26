"""Check that the CrewAI environment of this repo is ready.

    uv run main.py          # Python, CrewAI and .env check (no API call)
    uv run main.py --ping   # also send one tiny request to the configured LLM
"""

import argparse
import os
import platform
import sys
from importlib.metadata import version

from dotenv import load_dotenv


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--ping", action="store_true", help="send one tiny request to the configured LLM"
    )
    args = parser.parse_args()

    load_dotenv()

    print(f"Python  : {platform.python_version()}")
    print(f"CrewAI  : {version('crewai')}")

    model = os.getenv("MODEL")
    if not model:
        sys.exit("MODEL is not set: copy .env.example to .env and fill it in (see SETUP.md).")
    print(f"MODEL   : {model}")

    from crewai import LLM  # imported here because importing crewai takes a few seconds

    try:
        # Resolves the provider and reads its API key from the environment; no network call.
        llm = LLM(model=model)
    except Exception as exc:
        sys.exit(f"LLM config error: {exc}")
    print(f"Provider: {llm.provider}")
    if llm.api_key is None:
        sys.exit(f"No API key found for '{llm.provider}': add it to .env (see .env.example).")

    if args.ping:
        # No temperature/top_p here: newer Claude models reject them with HTTP 400.
        try:
            reply = llm.call("Reply with exactly one word: pong")
        except Exception as exc:
            sys.exit(f"Ping failed: {exc}")
        print(f"Ping    : {reply}")

    print("Setup OK")


if __name__ == "__main__":
    main()
