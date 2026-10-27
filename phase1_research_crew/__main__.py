"""Run the Phase 1 Researcher + Writer crew and save its report.

    uv run python -m phase1_research_crew "Java virtual threads"
    uv run python -m phase1_research_crew "Kafka vs RabbitMQ" --language Bangla
"""

import argparse
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

OUTPUT_DIR = Path("output")


def slugify(text: str) -> str:
    """Turn a topic into a safe file name: 'Kafka vs RabbitMQ' -> 'kafka-vs-rabbitmq'."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "report"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m phase1_research_crew",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("topic", help="what the crew should research")
    parser.add_argument("--language", default="English", help="report language (default: English)")
    args = parser.parse_args()

    load_dotenv()
    if not os.getenv("MODEL"):
        # Without MODEL, CrewAI silently falls back to an OpenAI model and fails with a confusing error.
        sys.exit("MODEL is not set: copy .env.example to .env and fill it in (see SETUP.md).")

    from phase1_research_crew.crew import ResearchCrew  # imported here so --help stays fast

    result = ResearchCrew().crew().kickoff(inputs={"topic": args.topic, "language": args.language})

    OUTPUT_DIR.mkdir(exist_ok=True)
    report = OUTPUT_DIR / f"{slugify(args.topic)}.md"
    report.write_text(result.raw, encoding="utf-8")

    usage = result.token_usage
    print(f"\nReport saved to {report}")
    print(
        f"Tokens: {usage.total_tokens} total ({usage.prompt_tokens} input, "
        f"{usage.completion_tokens} output) in {usage.successful_requests} LLM calls"
    )


if __name__ == "__main__":
    main()
