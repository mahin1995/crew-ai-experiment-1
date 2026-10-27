# Environment Setup (uv)

এই repo-র Python environment [uv](https://docs.astral.sh/uv) দিয়ে manage করা হয়। uv একাই Python install, virtual environment আর dependency সামলায়, তাই আলাদা করে Python, pip বা venv install করতে হবে না।

## Java dev-এর জন্য uv cheat sheet

| uv / Python | Java world-এ যার মতো |
|---|---|
| `pyproject.toml` | `pom.xml` / `build.gradle` |
| `uv.lock` | Gradle dependency lock file (প্রতিটা dependency-র exact version) |
| `.venv/` | এই project-এর নিজস্ব dependency folder (project-ভিত্তিক `~/.m2` ভাবতে পারেন) |
| `.python-version` | `.sdkmanrc` বা toolchain-এ JDK version pin করা |
| `uv sync` | `mvn dependency:resolve` |
| `uv add <package>` | `pom.xml`-এ dependency যোগ করা |
| `uv run <command>` | `mvn exec:java` / `./gradlew run` |

## ১. uv install করুন

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

অন্য উপায়: `brew install uv` (macOS), `winget install --id=astral-sh.uv -e` (Windows), বা `pipx install uv`।

Install-এর পর নতুন terminal খুলে check করুন:

```bash
uv --version
```

## ২. Repo clone করুন

```bash
git clone https://github.com/mahin1995/crew-ai-experiment-1.git
cd crew-ai-experiment-1
```

## ৩. Python আর dependencies install করুন

```bash
uv sync
```

এই একটা command যা করে:

- `.python-version` দেখে Python 3.12 না থাকলে নিজেই download করে
- `.venv/` folder-এ virtual environment বানায়
- `uv.lock` অনুযায়ী exact version-এ সব dependency install করে, যার মধ্যে আছে `crewai[anthropic,tools]` (CrewAI, Claude provider আর built-in tools)

প্রথমবার কয়েক মিনিট লাগতে পারে, কারণ CrewAI-এর dependency অনেক (`.venv` প্রায় 1 GB হয়)। পরের বার uv cache থেকে দ্রুত হয়।

> CrewAI-এর জন্য Python `>=3.10, <3.14` লাগে। এই repo Python 3.12-এ pin করা।

## ৪. API key সেট করুন (`.env`)

```bash
cp .env.example .env        # Windows: copy .env.example .env
```

তারপর `.env` খুলে key বসান:

```dotenv
MODEL=anthropic/claude-opus-5-5
ANTHROPIC_API_KEY=sk-ant-...
```

- Claude API key পাবেন [Claude Console](https://platform.claude.com)-এর API Keys page থেকে।
- CrewAI `MODEL` variable থেকে সব agent-এর default LLM নেয়। Format হলো `provider/model-id`।
- অন্য option (Sonnet, Haiku, Ollama-তে local model) `.env.example`-এ comment করা আছে।
- `.env` git-ignored, তাই key কখনো commit হবে না।

## ৫. Setup verify করুন

```bash
uv run main.py          # Python, CrewAI version আর .env check করে (কোনো API call হয় না)
uv run main.py --ping   # configured LLM-কে একটা ছোট request পাঠায়
```

সব ঠিক থাকলে output এরকম হবে:

```text
Python  : 3.12.13
CrewAI  : 1.15.30
MODEL   : anthropic/claude-opus-5-5
Provider: anthropic
Ping    : pong
Setup OK
```

## ৬. IDE setup

- **VS Code:** Command Palette → `Python: Select Interpreter` → `.venv/bin/python` (Windows: `.venv\Scripts\python.exe`)
- **IntelliJ IDEA / PyCharm:** Python Interpreter settings-এ existing environment হিসেবে `.venv`-এর python select করুন। IntelliJ IDEA-তে Python plugin লাগবে।

## রোজকার uv commands

| কাজ | Command |
|---|---|
| Script চালানো | `uv run main.py` |
| Test চালানো (offline, API খরচ নেই) | `uv run pytest` |
| নতুন package যোগ করা | `uv add <package>` (যেমন `uv add fastapi`) |
| শুধু development-এর package | `uv add --dev <package>` (যেমন `uv add --dev pytest`) |
| Package বাদ দেওয়া | `uv remove <package>` |
| `uv.lock` অনুযায়ী `.venv` মেলানো | `uv sync` |
| CrewAI upgrade (1.x-এর মধ্যে) | `uv lock --upgrade-package crewai`, তারপর `uv sync` |
| Dependency tree দেখা | `uv tree` |
| Python version বদলানো | `uv python pin 3.13`, তারপর `uv sync` |
| CrewAI CLI | `uv run crewai --help` |

`uv run` নিজেই আগে environment sync করে নেয়, তাই `.venv` activate করার দরকার নেই। চাইলে activate করেও কাজ করতে পারেন:

```bash
source .venv/bin/activate     # Windows: .venv\Scripts\activate
python main.py
```

## CrewAI CLI দিয়ে crew scaffold

CrewAI-এর CLI এই environment-এই install করা আছে:

```bash
uv run crewai create crew research_crew --classic
```

- `--classic` দিলে চেনা Python/YAML structure পাবেন: `config/agents.yaml`, `config/tasks.yaml`, `crew.py`, `main.py`। না দিলে CLI একটা interactive wizard চালায়। এই repo-র [`phase1_research_crew/`](phase1_research_crew/)-ও একই structure মেনে চলে।
- এটা নিজের `pyproject.toml` সহ আলাদা একটা uv project বানায়, আর তার ভেতরে নতুন `git init` করে। এই repo-র ভেতরে বানালে নতুন folder-এর `.git` মুছে দিন (`rm -rf research_crew/.git`), নাহলে nested git repo হয়ে যাবে।

## Troubleshooting

| সমস্যা | কারণ ও সমাধান |
|---|---|
| `uv: command not found` | Install-এর পর নতুন terminal খুলুন, বা `PATH`-এ `~/.local/bin` যোগ করুন |
| `MODEL is not set` | `.env` file নেই। `cp .env.example .env` করুন |
| `No API key found for 'anthropic'` | `.env`-এ `ANTHROPIC_API_KEY` বসান |
| `401 authentication_error` | API key ভুল বা বাতিল হয়ে গেছে। Console থেকে নতুন key নিন |
| `.env` বদলানোর পরও পুরোনো key বা model নিচ্ছে | Shell-এ export করা variable `.env`-এর চেয়ে priority পায়। `unset MODEL ANTHROPIC_API_KEY` করে আবার চালান |
| `temperature` বা `top_p` নিয়ে `400` error | নতুন Claude model এগুলো নেয় না। `LLM(...)` থেকে `temperature`/`top_p` সরিয়ে দিন |
| `requires-python` নিয়ে error | `uv python pin 3.12`, তারপর `uv sync` |

CrewAI default-এ anonymous usage telemetry পাঠায়। বন্ধ করতে `.env`-এ `CREWAI_DISABLE_TELEMETRY=true` দিন।
