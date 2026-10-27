"""Offline tests for the Phase 1 Researcher + Writer crew (no real LLM calls)."""

import json

import pytest
from crewai import Process

from phase1_research_crew.__main__ import main, slugify
from phase1_research_crew.crew import ResearchCrew

NOTES = "Kafka stores events in an append-only, partitioned log."
REPORT = "# Apache Kafka\n\nKafka is a distributed event streaming platform."


def reply_as_agent(body: dict) -> str:
    """Answer as the researcher or the writer, depending on the agent's system prompt."""
    return NOTES if "Research Analyst" in json.dumps(body.get("system")) else REPORT


@pytest.mark.parametrize(
    ("topic", "expected"),
    [
        ("Kafka vs RabbitMQ", "kafka-vs-rabbitmq"),
        ("Java 21: Virtual Threads!", "java-21-virtual-threads"),
        ("বাংলা", "report"),
    ],
)
def test_slugify(topic: str, expected: str) -> None:
    assert slugify(topic) == expected


def test_crew_runs_researcher_then_writer() -> None:
    crew = ResearchCrew().crew()

    researcher, writer = crew.agents
    research_task, writing_task = crew.tasks
    assert crew.process == Process.sequential
    assert research_task.agent is researcher
    assert writing_task.agent is writer


def test_cli_stops_with_clear_message_when_model_is_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MODEL")
    monkeypatch.setattr("phase1_research_crew.__main__.load_dotenv", lambda: None)  # ignore a local .env
    monkeypatch.setattr("sys.argv", ["prog", "Apache Kafka"])

    with pytest.raises(SystemExit, match="MODEL is not set"):
        main()


def test_cli_saves_report_and_passes_research_to_writer(
    fake_anthropic, monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    fake_anthropic.reply = reply_as_agent
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "Apache Kafka", "--language", "Bangla"])

    main()

    assert (tmp_path / "output" / "apache-kafka.md").read_text(encoding="utf-8") == REPORT

    research_call, writing_call = fake_anthropic.requests
    assert "Apache Kafka Senior Research Analyst" in json.dumps(research_call["system"])
    assert NOTES in json.dumps(writing_call["messages"])  # sequential: research output is the writer's context
    assert "in Bangla" in json.dumps(writing_call["messages"])
    for call in fake_anthropic.requests:
        assert "temperature" not in call  # newer Claude models reject sampling params
