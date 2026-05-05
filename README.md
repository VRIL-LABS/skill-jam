<div align="center">
  <img src="header.svg" alt="SKILL JAM v1.3 by VRIL LABS" width="100%"/>
</div>

<div align="center">

![Version](https://img.shields.io/badge/version-v1.3-blueviolet?style=flat-square)
![License](https://img.shields.io/badge/license-open%20source-green?style=flat-square)
![Stack](https://img.shields.io/badge/stack-Three.js%20%7C%20React%20Three%20Fiber%20%7C%20TSL-orange?style=flat-square)

![VRIL LABS Original Skills](https://img.shields.io/badge/VRIL%20LABS%20Original%20Skills-100-ff69b4?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0xIDE1aC0ydi02aDJ2NnptMC04aC0yVjdoMnYyeiIvPjwvc3ZnPg==)
<a href="https://github.com/VRIL-LABS/skill-jam/tree/main/featured-skills" title="Featured 3D AI Agent Skills by VRIL LABS">![Featured 3D Skills](https://img.shields.io/badge/Featured%203D%20Skills-10-00bfff?style=flat-square)</a>
<a href="https://github.com/VRIL-LABS/skill-jam/tree/main/popular-skills" title="Popular AI Agent Skills as Submodules">![Total Submodules](https://img.shields.io/badge/Total%20Submodules-16-yellow?style=flat-square)</a>
![Total Skills in Submodules](https://img.shields.io/badge/Total%20Skills%20in%20Submodules-2%2C000%2B-9b59b6?style=flat-square)
![Total Skills Jammed](https://img.shields.io/badge/Total%20Skills%20Jammed-2%2C100%2B-e74c3c?style=flat-square&logoColor=white)

</div>

# ☄️ skill-jam

> A large collection of agent skills, all "jammed" together in one repository. Welcome to the `skill-jam`.

---

## What is skill-jam?

**skill-jam** is a curated library of **agent skills** — modular, reusable capabilities that AI agents can invoke to perform real-world tasks. Think of each skill as a well-defined plugin: it has a clear purpose, a defined input/output contract, and can be composed with other skills to build sophisticated automated workflows.

The goal of this repository is to serve as a central hub where developers, researchers, and AI enthusiasts can discover, contribute, and remix agent skills across every domain — from software engineering and data analysis to productivity, research, and beyond.

---

## 🧠 What is an Agent Skill?

An **agent skill** is a discrete, callable capability that an AI agent can use as a tool. Skills:

- Have a **clear, single responsibility** (e.g., "summarize this document" or "find a bug in this function")
- Accept **structured inputs** and produce **structured outputs**
- Are **composable** — multiple skills can be chained into multi-step workflows
- Are **reusable** — one skill can serve many different agents or use-cases

---

## 📁 Repository Structure

```
skill-jam/
├── README.md              ← You are here
├── header.svg             ← Animated banner (v1.3)
├── .claude-plugin/
│   └── marketplace.json   ← Skills discovery config (enables npx skills add)
├── featured-skills/       ← 10 hand-picked 3D visualizer skills
│   ├── biefeld-brown-electrogravitics-visualizer/
│   ├── hutchison-effect-visualizer/
│   ├── leedskalnin-magnetic-current-visualizer/
│   ├── repulsine-aerodynamics-visualizer/
│   ├── rife-resonance-visualizer/
│   ├── russell-cosmogony-visualizer/
│   ├── schappeller-magnetism-visualizer/
│   ├── schauberger-vortex-flow-visualizer/
│   ├── searl-effect-generator-visualizer/
│   └── tesla-standing-wave-visualizer/
├── popular-skills/        ← 16 curated submodules from leading orgs
│   ├── vercel-labs/agent-skills        (Vercel)
│   ├── anthropics/skills               (Anthropic)
│   ├── microsoft/skills                (Microsoft)
│   ├── addyosmani/agent-skills         (Google / Addy Osmani)
│   ├── K-Dense-AI/scientific-agent-skills
│   ├── agentskills/agentskills         (agentskills.io spec)
│   ├── OthmanAdi/planning-with-files
│   ├── wormhole-foundation/blockchain-interop
│   ├── arpitg1304/robotics-agent-skills
│   ├── machina-sports/sports-skills
│   ├── Agents365-ai/drawio-skill
│   ├── sickn33/antigravity-awesome-skills  (1,400+ skills installer)
│   ├── automazeio/ccpm             (AI project management)
│   ├── mukul975/Anthropic-Cybersecurity-Skills  (754 cybersecurity skills)
│   ├── new-silvermoon/awesome-android-agent-skills  (Android dev)
│   └── hoodini/ai-agents-skills    (AI agent collection)
├── skills/
│   ├── engineering/       ← Software development & DevOps skills
│   ├── data/              ← Data analysis, ETL, and machine learning skills
│   ├── productivity/      ← Scheduling, email, file management skills
│   ├── research/          ← Web search, summarization, and citation skills
│   ├── commerce/          ← E-commerce, finance, and business skills
│   └── creative/          ← Writing, media, and content skills
└── docs/
    └── contributing.md    ← How to add your own skills
```

---

## ⭐ Featured Skills

The `featured-skills/` directory showcases **10 hand-picked, production-quality 3D visualizer skills** built on [Three.js r182+](https://threejs.org/), [React Three Fiber v9](https://docs.pmnd.rs/react-three-fiber), TSL/GLSL shaders, and GPU particle systems. Each visualizer brings an alternative-physics concept to life with interactive real-time 3D rendering.

| # | Skill | Description |
|---|-------|-------------|
| 1 | **Biefeld-Brown Electrogravitics Visualizer** | Real-time 3D visualization of asymmetric high-voltage capacitor thrust, ionic wind flow, and electrogravitics lift vectors. |
| 2 | **Hutchison Effect Visualizer** | Volumetric 3D rendering of overlapping RF, microwave, and Tesla coil interference fields producing anomalous material-behavior zones. |
| 3 | **Leedskalnin Magnetic Current Visualizer** | Dual counter-streaming helical North/South magnetic particle flows through conductors, based on Ed Leedskalnin's magnetic current theory. |
| 4 | **Repulsine Aerodynamics Visualizer** | Viktor Schauberger's vortex implosion disc — dual counter-rotating vortex structure, centripetal dynamics, and toroidal pressure fields. |
| 5 | **Rife Resonance Visualizer** | Plasma tube resonance system with MOR frequency standing waves, spectral emission lines, and cellular resonance targets. |
| 6 | **Russell Cosmogony Visualizer** | Walter Russell's wave universe — dual opposed vortex cone matter formation, cube-sphere pressure geometry, and nine-octave periodic table wave structure. |
| 7 | **Schappeller Magnetism Visualizer** | Karl Schappeller's glowing magnetism sphere — etheric plasma core, self-organizing magnetic field lines, and luminous aether vortex. |
| 8 | **Schauberger Vortex Flow Visualizer** | Viktor Schauberger's "living water" implosion vortex — hyperbolic spiral flow, centripetal suction, and temperature-stratified laminar streams. |
| 9 | **Searl Effect Generator Visualizer** | John Searl's SEG — concentric magnetic rotor rings, self-accelerating roller cylinders, and an electron-spin plasma boundary layer. |
| 10 | **Tesla Standing Wave Visualizer** | Nikola Tesla's Wardenclyffe resonance system — Earth-resonance cavity modes, radial electric field pulses, and toroidal magnifying transmitter fields. |

> Each featured skill lives in `featured-skills/<skill-name>/SKILL.md` and contains full invocation context, process steps, and stack details.

---

## 📦 Installing Skills via `npx skills add`

Skills in this repository follow the [Agent Skills](https://agentskills.io/) open format and are compatible with the `skills` CLI. Install any skill directly into your AI agent (Claude Code, Cursor, Copilot, etc.) with a single command.

### ✨ Install the Vril Skills collection (100 curated skills)

The `vril-skills` collection is the curated flagship bundle — 100 hand-picked, production-ready skills spanning engineering, data, productivity, research, commerce, creative, 3D visualization, Vercel, Cloudflare, browser automation, document processing, blockchain, and more.

```bash
npx skills add https://github.com/VRIL-LABS/skill-jam --plugin vril-skills
```

### Install all 50 general skills

The base command installs the 50 core general skills (engineering, data, productivity, research, commerce, creative) found at the top level of `skills/`. For the full 100-skill Vril collection use the `--plugin vril-skills` command above.

```bash
npx skills add https://github.com/VRIL-LABS/skill-jam
```

### Install a specific skill

Any of the 100 skills in the Vril Skills collection can be installed by name:

```bash
# General skills
npx skills add https://github.com/VRIL-LABS/skill-jam --skill code-reviewer
npx skills add https://github.com/VRIL-LABS/skill-jam --skill bug-diagnoser

# Featured 3D visualizer skills (discovered via .claude-plugin/marketplace.json)
npx skills add https://github.com/VRIL-LABS/skill-jam --skill rife-resonance-visualizer
npx skills add https://github.com/VRIL-LABS/skill-jam --skill tesla-standing-wave-visualizer
```

### Install all 60 skills (general + featured visualizers)

The `featured-skills/` directory lives one level deeper than Vercel's flat layout, so a `.claude-plugin/marketplace.json` is included at the repository root to make all 10 featured 3D visualizer skills discoverable at the same depth as the general skills. No extra flags are needed:

```bash
npx skills add https://github.com/VRIL-LABS/skill-jam --skill "*"
```

### Install skills from a popular-skills submodule

Each `popular-skills/` entry is a full Git submodule pointing to its upstream repository. Install directly from the upstream source (fastest) or via the submodule path in this repo:

```bash
# Direct from upstream (recommended)
npx skills add https://github.com/vercel-labs/agent-skills
npx skills add https://github.com/anthropics/skills
npx skills add https://github.com/microsoft/skills
npx skills add https://github.com/sickn33/antigravity-awesome-skills
npx skills add https://github.com/mukul975/Anthropic-Cybersecurity-Skills

# Via skill-jam submodule path (requires --full-depth)
npx skills add https://github.com/VRIL-LABS/skill-jam --full-depth --skill react-best-practices
```

---

## 🌐 Popular Skills

The `popular-skills/` directory contains **16 curated Git submodules** pointing to the most widely used agent skill repositories from leading organizations. These are tracked at a fixed commit for reproducibility and can be updated with `git submodule update --remote`.

| # | Repository | Organization | Stars | Description |
|---|-----------|--------------|-------|-------------|
| 1 | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Vercel | ⭐ | React best practices, web design guidelines, Vercel deployment, view transitions, and composition patterns. |
| 2 | [anthropics/skills](https://github.com/anthropics/skills) | Anthropic | ⭐ 128k | Anthropic's official Claude skills — creative, technical, enterprise, and document skills. The reference implementation. |
| 3 | [microsoft/skills](https://github.com/microsoft/skills) | Microsoft | ⭐ 2.2k | Microsoft SDK skills for coding agents — Azure, Foundry, MCP servers, and custom agent patterns. |
| 4 | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Addy Osmani (Google) | ⭐ 28k | Production-grade engineering skills from a Google Chrome engineer — performance, accessibility, and web platform best practices. |
| 5 | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | K-Dense AI | ⭐ 20k | Research, science, engineering, bioinformatics, drug discovery, materials science, and data analysis skills. |
| 6 | [agentskills/agentskills](https://github.com/agentskills/agentskills) | agentskills.io | ⭐ 18k | The official Agent Skills specification, SDK, and reference examples maintained by Anthropic. |
| 7 | [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | OthmanAdi | ⭐ 20k | Manus-style persistent markdown planning skill — document-driven workflow with structured task decomposition. |
| 8 | [wormhole-foundation/blockchain-interop](https://github.com/wormhole-foundation/blockchain-interop) | Wormhole Foundation | ⭐ | Cross-chain blockchain interoperability skills covering NTT, CCTP, Connect, Messaging, and Settlement. |
| 9 | [arpitg1304/robotics-agent-skills](https://github.com/arpitg1304/robotics-agent-skills) | arpitg1304 | ⭐ 190 | Production-grade robotics skills for ROS1/ROS2, SOLID principles, design patterns, and testing. |
| 10 | [machina-sports/sports-skills](https://github.com/machina-sports/sports-skills) | Machina Sports | ⭐ 95 | Live sports data and prediction market skills for Football, F1, Kalshi, and Polymarket — zero API keys required. |
| 11 | [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) | Agents365 | ⭐ 1.1k | Generate professional draw.io diagrams from natural language and export to PNG/SVG/PDF. |
| 12 | [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) | sickn33 | ⭐ 36k | Installable library of 1,400+ agentic skills with CLI installer, bundles, and official/community collections. Compatible with Claude Code, Cursor, Codex, Gemini CLI, and more. |
| 13 | [automazeio/ccpm](https://github.com/automazeio/ccpm) | Automazeio | ⭐ 8k | AI-powered project management skills using GitHub Issues and Git worktrees for parallel agent execution. |
| 14 | [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) | mukul975 | ⭐ 5.9k | 754 structured cybersecurity skills mapped to MITRE ATT&CK, NIST CSF 2.0, ATLAS, D3FEND — 26 security domains. |
| 15 | [new-silvermoon/awesome-android-agent-skills](https://github.com/new-silvermoon/awesome-android-agent-skills) | new-silvermoon | ⭐ 784 | Standardized agent skills for modern Android development — Kotlin, Jetpack Compose, and best practices. |
| 16 | [hoodini/ai-agents-skills](https://github.com/hoodini/ai-agents-skills) | Yuval Avidani | ⭐ 201 | Curated collection of specialized skills for Claude Code, GitHub Copilot, Cursor, and Windsurf. |

### Initializing submodules

```bash
# After cloning skill-jam, fetch all submodule content
git submodule update --init --recursive

# Update all submodules to their latest upstream commits
git submodule update --remote --merge
```

---

## 🗂️ All Skills

A complete list of all **100 curated skills** in the Vril Skills collection, spanning engineering, data, productivity, research, commerce, creative, 3D visualization, Vercel, Cloudflare, browser automation, search, document processing, security, and blockchain domains.

| # | Skill | Category | Description |
|---|-------|----------|-------------|
| 1 | **Accessibility Auditor** | Engineering | Scans frontend code and rendered HTML for WCAG 2.1 compliance issues — missing alt text, color contrast, ARIA roles, keyboard navigation. |
| 2 | **API Scaffolder** | Engineering | Generates REST or GraphQL API boilerplate — controllers, routes, models, and validation — from an OpenAPI spec or description. |
| 3 | **Auth Integrator** | Engineering | Adds authentication and authorization flows — OAuth 2.0, JWT, RBAC, API keys — to an existing application. |
| 4 | **Bug Diagnoser** | Engineering | Analyzes stack traces, error logs, and surrounding code to pinpoint root causes and propose fixes. |
| 5 | **Cache Advisor** | Engineering | Recommends caching strategies (in-memory, Redis, CDN) based on access patterns and suggests TTL policies and invalidation logic. |
| 6 | **Calendar Manager** | Productivity | Creates, reschedules, and summarizes calendar events; finds optimal meeting slots across participants and time zones. |
| 7 | **CI/CD Pipeline Builder** | Engineering | Generates GitHub Actions, GitLab CI, or CircleCI pipeline configs tailored to the detected language and framework. |
| 8 | **Code Formatter** | Engineering | Applies language-specific formatting (Prettier, Black, `gofmt`, `rustfmt`) and enforces consistent linting rules across a codebase. |
| 9 | **Code Refactorer** | Engineering | Detects code smells (duplication, long methods, god classes) and applies safe, behavior-preserving refactors. |
| 10 | **Code Reviewer** | Engineering | Performs automated code review with inline comments, flags anti-patterns, and suggests improvements against style guides. |
| 11 | **Competitive Intelligence** | Commerce | Monitors competitor websites, pricing, product launches, and job postings to surface strategic insights. |
| 12 | **Config Manager** | Engineering | Manages environment variables, secrets, and feature flags — generates `.env` templates, validates required keys, and flags hardcoded secrets. |
| 13 | **Customer Support Bot** | Commerce | Triages incoming support tickets, suggests resolutions from a knowledge base, and escalates edge cases to humans. |
| 14 | **Data Analyst** | Data | Loads tabular datasets, generates descriptive statistics, produces charts, and surfaces trends or anomalies. |
| 15 | **Data Validator** | Data | Generates JSON Schema, Pydantic models, or Zod schemas from sample data or descriptions to enforce data contracts. |
| 16 | **Database Query Optimizer** | Data | Analyzes SQL or NoSQL queries, explains query plans, and rewrites them for better performance. |
| 17 | **Dependency Updater** | Engineering | Audits `package.json`, `requirements.txt`, or `go.mod` for outdated or vulnerable packages and proposes safe upgrades. |
| 18 | **Dev Environment Setup** | Engineering | Bootstraps development environments with `.env` templates, `Makefile` targets, editor configs, and local dependency instructions. |
| 19 | **Docker Composer** | Engineering | Creates and validates `Dockerfile` and `docker-compose.yml` files optimized for the detected stack, including multi-stage builds. |
| 20 | **Documentation Writer** | Engineering | Generates inline docstrings, README sections, and API reference docs from source code and function signatures. |
| 21 | **Email Automation** | Productivity | Composes, sends, classifies, and summarizes emails based on rules, templates, or natural-language instructions. |
| 22 | **Error Handler Advisor** | Engineering | Reviews code paths and suggests robust error handling: retries, fallbacks, circuit breakers, and user-friendly messages. |
| 23 | **File Organizer** | Productivity | Categorizes, renames, deduplicates, and archives files based on type, date, content, or custom rules. |
| 24 | **Git Workflow Automator** | Engineering | Automates branching strategies, commit message conventions, changelog generation, and semantic versioning tags. |
| 25 | **Image Describer** | Creative | Generates detailed captions, alt text, and structured metadata for images using vision models. |
| 26 | **Inventory Manager** | Commerce | Tracks stock levels across locations, predicts reorder points using demand forecasting, and triggers purchase orders. |
| 27 | **Invoice Processor** | Commerce | Extracts structured line items, totals, and vendor data from invoice PDFs or images and routes them for approval. |
| 28 | **Language Translator** | Creative | Translates text across 100+ languages while preserving tone, formatting, and domain-specific terminology. |
| 29 | **Lead Qualifier** | Commerce | Scores, enriches, and prioritizes inbound sales leads using firmographic data, behavioral signals, and ICP criteria. |
| 30 | **Legal Document Reviewer** | Research | Scans contracts and legal documents for risky clauses, non-standard terms, missing provisions, and regulatory compliance issues. |
| 31 | **Load Test Script Generator** | Engineering | Generates load testing scripts for k6, Locust, or JMeter from an OpenAPI spec or recorded traffic, including ramp-up scenarios. |
| 32 | **Log Analyzer** | Engineering | Parses structured or unstructured application logs to surface error trends, anomaly spikes, and actionable insights. |
| 33 | **Meeting Scheduler** | Productivity | Identifies optimal meeting windows across participants' calendars and time zones, and sends invites with agendas. |
| 34 | **Message Queue Integrator** | Engineering | Sets up publish/subscribe or task queue patterns using RabbitMQ, Kafka, or SQS, including producer, consumer, and dead-letter configs. |
| 35 | **News Aggregator** | Research | Fetches, deduplicates, and categorizes news articles from multiple sources on a given topic or keyword list. |
| 36 | **OpenAPI Generator** | Engineering | Generates OpenAPI 3.x specifications from annotated code, existing routes, or natural-language descriptions, and vice versa. |
| 37 | **Performance Profiler** | Engineering | Interprets profiling output (flame graphs, heap dumps, `perf` reports) and highlights the top bottlenecks with optimization advice. |
| 38 | **Price Comparator** | Commerce | Searches multiple e-commerce platforms for a product and returns a ranked comparison of prices, sellers, and shipping. |
| 39 | **Recipe Recommender** | Productivity | Suggests recipes based on available ingredients, dietary restrictions, cuisine preferences, and pantry inventory. |
| 40 | **Research Assistant** | Research | Searches the web, fetches sources, synthesizes findings, and formats cited research reports on any topic. |
| 41 | **Resume Parser** | Commerce | Extracts structured candidate data (skills, experience, education) from resumes and CVs in any format. |
| 42 | **Security Scanner** | Engineering | Detects common vulnerability patterns (XSS, SQL injection, path traversal, IDOR) in source code and suggests mitigations. |
| 43 | **SEO Analyzer** | Commerce | Audits web pages for on-page SEO best practices — title tags, meta descriptions, keyword density, Core Web Vitals, and structured data. |
| 44 | **Sentiment Analyzer** | Data | Classifies the sentiment (positive, negative, neutral, mixed) of text at document, sentence, or aspect level. |
| 45 | **Social Media Monitor** | Commerce | Tracks brand mentions, hashtags, and engagement metrics across social platforms and surfaces sentiment trends. |
| 46 | **Test Generator** | Engineering | Reads source code and generates unit tests, integration tests, or snapshot tests with appropriate mocking. |
| 47 | **Text Summarizer** | Research | Condenses long-form documents, papers, or transcripts into concise summaries, bullet points, or executive briefs. |
| 48 | **Travel Planner** | Productivity | Builds complete travel itineraries from flights, hotels, and activities; accounts for budget, preferences, and transit times. |
| 49 | **Weather Forecaster** | Productivity | Retrieves current conditions and multi-day forecasts for any location, formatted for human or downstream agent consumption. |
| 50 | **Web Scraper** | Research | Extracts structured data from websites, handling pagination, JavaScript rendering, and rate limiting. |

### 🎆 Featured 3D Visualizer Skills (51–60)

| # | Skill | Description |
|---|-------|-------------|
| 51 | **Biefeld-Brown Electrogravitics Visualizer** | Real-time 3D visualization of asymmetric high-voltage capacitor thrust, ionic wind flow, and electrogravitics lift vectors. |
| 52 | **Hutchison Effect Visualizer** | Volumetric 3D rendering of overlapping RF, microwave, and Tesla coil interference fields producing anomalous material-behavior zones. |
| 53 | **Leedskalnin Magnetic Current Visualizer** | Dual counter-streaming helical North/South magnetic particle flows through conductors, based on Ed Leedskalnin's theory. |
| 54 | **Repulsine Aerodynamics Visualizer** | Viktor Schauberger's vortex implosion disc — dual counter-rotating vortex structure, centripetal dynamics, and toroidal pressure fields. |
| 55 | **Rife Resonance Visualizer** | Plasma tube resonance system with MOR frequency standing waves, spectral emission lines, and cellular resonance targets. |
| 56 | **Russell Cosmogony Visualizer** | Walter Russell's wave universe — dual opposed vortex cone matter formation, cube-sphere pressure geometry, and nine-octave periodic table. |
| 57 | **Schappeller Magnetism Visualizer** | Karl Schappeller's glowing magnetism sphere — etheric plasma core, self-organizing magnetic field lines, and luminous aether vortex. |
| 58 | **Schauberger Vortex Flow Visualizer** | Viktor Schauberger's "living water" implosion vortex — hyperbolic spiral flow, centripetal suction, and temperature-stratified laminar streams. |
| 59 | **Searl Effect Generator Visualizer** | John Searl's SEG — concentric magnetic rotor rings, self-accelerating roller cylinders, and an electron-spin plasma boundary layer. |
| 60 | **Tesla Standing Wave Visualizer** | Nikola Tesla's Wardenclyffe resonance system — Earth-resonance cavity modes, radial electric field pulses, and toroidal magnifying transmitter fields. |

### ▲ Vercel Platform Skills (61–68)

| # | Skill | Description |
|---|-------|-------------|
| 61 | **Vercel AI SDK** | Unified TypeScript toolkit for OpenAI, Anthropic, Google and other LLM providers — text generation, streaming, tool calling, structured output. |
| 62 | **Vercel AI Gateway** | Centralized AI gateway for routing, rate-limiting, caching, and cost controls across multiple LLM providers. |
| 63 | **Vercel AI Elements** | Pre-built UI components for building AI-powered chat interfaces and generative experiences with the Vercel AI SDK. |
| 64 | **Vercel Flags SDK** | Feature flagging SDK for gradual rollouts, A/B testing, and personalization — integrates with Vercel Edge Config. |
| 65 | **Vercel Platform** | Cloud platform for Next.js — Git-integrated deployments, preview environments, edge functions, and global CDN. |
| 66 | **Vercel Chat SDK** | Official chat template and SDK for building production-grade AI chat apps with multi-modal support. |
| 67 | **Vercel Workflow SDK** | Durable, serverless workflow orchestration for long-running AI pipelines and multi-step agentic tasks. |
| 68 | **Vercel Streamdown** | Streaming markdown renderer for AI-generated content with real-time progressive disclosure. |

### ☁️ Cloudflare Edge Skills (69–76)

| # | Skill | Description |
|---|-------|-------------|
| 69 | **Cloudflare Workers** | Deploy serverless JavaScript/TypeScript at the edge — Wrangler CLI, bindings, and edge-native patterns. |
| 70 | **Cloudflare AI** | Run inference at the edge with Workers AI — text generation, embeddings, image classification, and speech recognition. |
| 71 | **Cloudflare Pages** | Deploy JAMstack and full-stack apps to Cloudflare's global network with Git-integrated previews. |
| 72 | **Cloudflare D1** | Serverless SQLite-compatible relational database at the edge — schema migrations, query optimization, and replication. |
| 73 | **Cloudflare KV** | Global key-value store for edge-caching session data, configuration, and feature flags. |
| 74 | **Cloudflare R2** | S3-compatible object storage with zero egress fees — large asset hosting, backups, and media storage. |
| 75 | **Cloudflare Zero Trust** | Zero Trust network access — secure remote access, identity-aware proxies, and ZTNA policies. |
| 76 | **Cloudflare WAF** | Web Application Firewall — managed rulesets, rate limiting, bot management, and DDoS mitigation. |

### 🌐 Browser Automation Skills (77–80)

| # | Skill | Description |
|---|-------|-------------|
| 77 | **Browser Use** | AI-native browser automation for web scraping, form filling, and multi-step web tasks using LLM-driven control. |
| 78 | **Vercel Agent Browser** | Vercel's agent-controlled browser for web research, screenshot capture, and page interaction workflows. |
| 79 | **Playwright CLI** | Microsoft Playwright CLI skill for cross-browser automated testing, UI automation, and visual regression. |
| 80 | **OpenAI Playwright** | OpenAI's Playwright integration for AI-driven browser testing and web agent tasks. |

### 🛠️ Developer Tools Skills (81–84)

| # | Skill | Description |
|---|-------|-------------|
| 81 | **Agent Tools** | Core agent tooling primitives — file I/O, shell execution, HTTP requests, and structured output helpers. |
| 82 | **AI Code Review** | AI-powered code review skill that provides detailed inline feedback, flags anti-patterns, and suggests refactors. |
| 83 | **Capability Evolver** | Evolves and improves agent capabilities over time by analyzing usage patterns and suggesting skill enhancements. |
| 84 | **Skill Vetter** | Validates SKILL.md files against the Agent Skills specification — checks format, metadata, and quality. |

### 🔍 Search & Research Skills (85–89)

| # | Skill | Description |
|---|-------|-------------|
| 85 | **Tavily Search** | AI-optimized web search API returning structured, relevant results for agentic research tasks. |
| 86 | **Tavily Research** | Deep research workflow using Tavily — multi-query synthesis, citation tracking, and structured report generation. |
| 87 | **Exa Research Paper Search** | Semantic search over academic papers and preprints — finds relevant research, abstracts, and citations. |
| 88 | **Web Search (Inference.sh)** | Lightweight web search skill via Inference.sh — fast, structured results for factual queries. |
| 89 | **Exa Company Search** | Searches and profiles companies using Exa's neural search — funding, team, products, and recent news. |

### 📄 Document Processing Skills (90–93)

| # | Skill | Description |
|---|-------|-------------|
| 90 | **PDF Processor** | Extracts text, tables, and structured data from PDF documents; supports multi-page parsing and OCR. |
| 91 | **DOCX Processor** | Reads and writes Microsoft Word documents — extracts content, applies styles, and merges templates. |
| 92 | **PPTX Processor** | Parses and generates PowerPoint presentations — slide extraction, layout manipulation, and content injection. |
| 93 | **XLSX Processor** | Reads and writes Excel spreadsheets — cell extraction, formula evaluation, and multi-sheet operations. |

### 🔐 Security Skills (94)

| # | Skill | Description |
|---|-------|-------------|
| 94 | **Prompt Guard** | Detects and blocks prompt injection attacks, jailbreak attempts, and adversarial inputs in agent pipelines. |

### ⛓️ Blockchain & Crypto Skills (95–100)

| # | Skill | Description |
|---|-------|-------------|
| 95 | **Coinbase Wallet Auth** | Authenticates and manages Coinbase developer wallets for on-chain agent operations. |
| 96 | **Coinbase Wallet Fund** | Funds wallets with ETH or USDC from Coinbase for gas and on-chain transactions. |
| 97 | **Coinbase Send USDC** | Sends USDC stablecoin transfers on Base network — single recipient or batch payments. |
| 98 | **Coinbase Trade** | Executes token swaps and trades via Coinbase's agentic wallet and DEX integrations. |
| 99 | **On-Chain Data Query** | Queries blockchain state, transaction history, token balances, and contract data across EVM chains. |
| 100 | **Monetize Service** | Deploys x402 payment-gated API endpoints to charge per-call using Coinbase's stablecoin infrastructure. |

---

## 🤝 Contributing

Have a skill you'd like to add? We'd love to include it! Please see [`docs/contributing.md`](docs/contributing.md) for guidelines on how to structure and submit a new skill.

A few ground rules:
- Each skill should have a **clear, single responsibility**
- Include a description, example inputs/outputs, and any dependencies
- Skills should be broadly useful, not narrowly specific to one use-case

---

## 📄 License

This repository is open source. See [LICENSE](LICENSE) for details.

---

<p align="center">Made with 🎸 by the skill-jam community</p>
