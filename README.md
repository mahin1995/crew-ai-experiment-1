# CrewAI Learning Roadmap

CrewAI দিয়ে multi-agent AI system বানানো শেখার জন্য একটা hands-on roadmap। প্রতিটা phase-এর experiment এই repo-তেই থাকবে।

> **Environment setup:** uv দিয়ে Python আর CrewAI কীভাবে install করবেন, তার ধাপগুলো [SETUP.md](SETUP.md)-তে আছে।

## Quick Start

```bash
git clone https://github.com/mahin1995/crew-ai-experiment-1.git
cd crew-ai-experiment-1
uv sync                   # Python 3.12 আর সব dependency install করে
cp .env.example .env      # তারপর .env-এ ANTHROPIC_API_KEY বসান
uv run main.py --ping     # setup ঠিক আছে কিনা check করে
```

## CrewAI কী?

**CrewAI** একটি Python framework, যা দিয়ে একাধিক AI **Agent** কে একটা টিমের (**Crew**) মতো সাজিয়ে কাজ করানো যায়। প্রতিটা Agent-এর নিজের **role**, **goal** আর **tools** থাকে। তারা নিজেদের মধ্যে **Task** ভাগ করে নেয়, আর একজনের output পরের জনের input হিসেবে যায়।

> Java dev হিসেবে এভাবে ভাবতে পারেন: Agent হলো একটা Spring `@Service`, তবে তার ভেতরের logic লেখে LLM। Crew হলো সেই orchestrator, যে service গুলোকে একসাথে চালায়।

| CrewAI concept | কী করে | Java/Spring-এ যার মতো |
|---|---|---|
| `Agent` | role, goal, backstory আর tools সহ একজন AI worker | `@Service` bean |
| `Task` | একটা নির্দিষ্ট কাজ, সাথে `expected_output` | service method call |
| `Crew` | agents আর tasks একসাথে চালায় | orchestrator / facade |
| `Tool` | agent যে function call করতে পারে (API, DB, file) | inject করা client বা repository |
| `Flow` | event-driven, deterministic workflow | workflow engine / state machine |

## CrewAI দিয়ে কী কী করা যায়

| Use case | উদাহরণ |
|---|---|
| Research ও report | Researcher agent web ঘাঁটে, Writer agent report লেখে, Editor agent সেটা review করে |
| Code review বা generation | PR diff analyze করা, bug খোঁজা, test লেখা |
| Customer support | Ticket classify করা, সাথে RAG দিয়ে উত্তর বের করা |
| Data analysis | SQL query বানানো, result বিশ্লেষণ করা, summary দেওয়া |
| Content pipeline | Blog, SEO, social post বানানো |
| Business automation | Lead qualify করা, email draft করা, CRM update করা |
| Backend-এর সাথে integration | Spring Boot API থেকে FastAPI-এর পেছনে থাকা CrewAI service call করা |

## Learning Roadmap (প্রায় ৮ সপ্তাহ)

প্রতিটা item শেষ হলে checkbox টিক দিন। প্রতিটা phase-এর project এই repo-তে আলাদা folder-এ থাকবে।

### Phase 0: Prerequisites (সপ্তাহ ১)

- [ ] **Python basics**: `uv`, virtual environment, type hints, `pydantic`, `async`/`await`। Java জানা থাকলে এটা দ্রুত হয়ে যাবে।
- [ ] **LLM fundamentals**: prompt, token, context window, tool/function calling, structured output।
- [ ] একটা LLM API key (Claude বা OpenAI), অথবা free-তে চালাতে Ollama-তে local model।
- [ ] [SETUP.md](SETUP.md) অনুযায়ী environment ready করে `uv run main.py --ping` চালানো।

### Phase 1: Core Concepts (সপ্তাহ ২)

- [ ] `Agent`: `role`, `goal`, `backstory`, `llm`, `tools`
- [ ] `Task`: `description`, `expected_output`, কোন agent কাজটা করবে
- [ ] `Crew`: agents আর tasks একসাথে, `Process.sequential` দিয়ে
- [ ] `crewai create crew <name> --classic` দিয়ে official scaffold দেখা: `config/agents.yaml`, `config/tasks.yaml`, `crew.py`, `main.py`
- 🎯 **Project:** "Topic Researcher + Writer" crew, যেটা একটা topic নিয়ে markdown report বানাবে।

### Phase 2: Tools ও Structured Output (সপ্তাহ ৩)

- [ ] Built-in tools (`crewai_tools`): `SerperDevTool` (web search), `ScrapeWebsiteTool`, `FileReadTool`
- [ ] `BaseTool` subclass বা `@tool` decorator দিয়ে **custom tool** বানানো। যেমন নিজের REST API বা PostgreSQL call করা।
- [ ] `output_pydantic` / `output_json` দিয়ে typed output নেওয়া। Java-র DTO-র মতোই ধারণা।
- [ ] Task-এর `guardrail` দিয়ে output validate করা
- 🎯 **Project:** একটা agent যে PostgreSQL-এ read-only query চালিয়ে রিপোর্ট দেবে।

### Phase 3: Advanced Orchestration (সপ্তাহ ৪)

- [ ] `Process.hierarchical`: একজন manager agent (`manager_llm`) কাজ ভাগ করে দেয়
- [ ] Task-এর `context` (dependency), `async_execution`, `human_input`
- [ ] `allow_delegation`: এক agent আরেকজনকে কাজ দিতে পারবে কিনা
- [ ] **Memory** (`memory=True`) আর **Knowledge sources** (RAG)
- 🎯 **Project:** Code Review crew। Analyzer, Security Reviewer আর Summarizer মিলে কাজ করবে।

### Phase 4: Flows, অর্থাৎ Production-grade workflow (সপ্তাহ ৫)

- [ ] `Flow`: `@start`, `@listen`, `@router` দিয়ে event-driven, deterministic pipeline বানানো
- [ ] **Crew vs Flow**: Crew চলে autonomous ভাবে, Flow-তে control আপনার হাতে থাকে আর ফলাফল predictable। Production-এ সাধারণত Flow-এর ভেতরে Crew রাখা হয়।
- [ ] Structured state (Pydantic model) দিয়ে state management
- 🎯 **Project:** Support ticket flow। Classify করে এরপর route করে: billing crew, tech crew, নাহলে human escalation।

### Phase 5: Production ও Integration (সপ্তাহ ৬–৭)

- [ ] CrewAI-কে **FastAPI** দিয়ে wrap করা, তারপর **Spring Boot** থেকে `RestClient`/`WebClient` দিয়ে call করা
- [ ] দীর্ঘ সময় লাগে এমন crew-এর জন্য async job pattern: request এলে job id ফেরত দিন, তারপর polling বা webhook। এখানে Kafka বা RabbitMQ ব্যবহার করা যায়।
- [ ] **Observability**: token usage, cost tracking, tracing (Langfuse, AgentOps ইত্যাদি)
- [ ] **Reliability**: `max_iter`, `max_rpm`, timeout, retry, guardrails
- [ ] **Testing**: `crewai test`, LLM output-এর evaluation
- [ ] Docker দিয়ে deploy
- 🎯 **Project:** Phase 2-এর crew-কে FastAPI service বানিয়ে Spring Boot app থেকে call করা।

### Phase 6: Capstone (সপ্তাহ ৮)

- 🎯 একটা end-to-end project। যেমন **"Spring Boot + CrewAI Job Analyzer"**: CV আর JD নেবে, তুলনা করবে, gap দেখাবে, interview-এর প্রশ্ন বানাবে। ফলাফল PostgreSQL-এ save হবে।

## Trade-offs: CrewAI নাকি অন্য কিছু?

| Option | কখন ব্যবহার করবেন |
|---|---|
| **CrewAI** | Multi-agent prototype দ্রুত বানাতে চাইলে। Role-based ধারণাটা সহজ। |
| **LangGraph** | Agent কোন পথে চলবে তার উপর খুব সূক্ষ্ম control লাগলে (graph আর state machine)। |
| **Spring AI / LangChain4j** | পুরো stack Java-তে রাখতে চাইলে। Multi-agent support এখনও তুলনামূলক কম। |
| **Plain API + tool calling** | কাজটা সহজ হলে। অনেক সময় একটা agent-ই যথেষ্ট, framework লাগে না। |

## Common Pitfalls

- Agent বেশি হলে token খরচ আর latency দুটোই বাড়ে। কম agent দিয়ে শুরু করুন।
- Agent loop-এ আটকে যেতে পারে। `max_iter` সেট করে রাখুন।
- Output non-deterministic। `output_pydantic` আর `guardrail` দিয়ে validate করুন।
- নতুন Claude model-এ (Opus 5.5, Sonnet 5.5 ইত্যাদি) `temperature`/`top_p` দেবেন না। দিলে API 400 error দেয়।
- CrewAI-এর API দ্রুত বদলায়। এই repo `uv.lock`-এ `crewai 1.15.30`-এ pin করা। Upgrade করার আগে [release notes](https://github.com/crewAIInc/crewAI/releases) দেখে নিন।

## Interview Questions

1. **Agent আর সাধারণ LLM call-এর পার্থক্য কী?**
   Agent নিজে reason করে, tool বেছে নেয়, আর loop-এ কাজ করে লক্ষ্যে পৌঁছায়। সাধারণ LLM call একটা request, একটা response।
2. **Sequential আর hierarchical process-এর পার্থক্য কী?**
   Sequential-এ task-এর ক্রম আগে থেকে ঠিক করা। Hierarchical-এ manager LLM কাজ ভাগ করে দেয়, ফলে flexibility বাড়ে কিন্তু খরচও বাড়ে।
3. **Production-এ LLM cost আর latency কীভাবে কমাবেন?**
   Caching, ছোট model দিয়ে routing, কম agent রাখা, structured output, আর async processing।
4. **Crew আর Flow কখন কোনটা?**
   যে কাজের পথ আগে থেকে জানা নেই, সেখানে Crew। যে business process-এর ধাপ নির্দিষ্ট আর audit লাগে, সেখানে Flow (দরকার হলে Flow-এর ভেতরে Crew)।
5. **Agent-এর tool call নিরাপদ রাখবেন কীভাবে?**
   Least privilege (যেমন DB-তে read-only user), input validation, timeout, আর বিপজ্জনক action-এর আগে `human_input` দিয়ে মানুষের approval।

## Repo Structure

```text
crew-ai-experiment-1/
├── README.md         # এই roadmap
├── SETUP.md          # uv দিয়ে environment setup
├── pyproject.toml    # dependencies (Maven-এর pom.xml-এর মতো)
├── uv.lock           # exact version lock, commit করা থাকে
├── .python-version   # Python 3.12 pin
├── .env.example      # .env-এর template (MODEL, API keys)
└── main.py           # environment check: uv run main.py --ping
```

## Resources

- CrewAI docs: <https://docs.crewai.com>
- CrewAI GitHub: <https://github.com/crewAIInc/crewAI>
- CrewAI examples: <https://github.com/crewAIInc/crewAI-examples>
- uv docs: <https://docs.astral.sh/uv>
- Claude API docs: <https://platform.claude.com/docs>
