<div align="center">
  <img src="header.svg" alt="SKILL JAM v1.1 by VRIL LABS" width="100%"/>
</div>

<div align="center">

![Version](https://img.shields.io/badge/version-v1.1-blueviolet?style=flat-square)
![Skills](https://img.shields.io/badge/skills-50-ff69b4?style=flat-square)
![Featured Skills](https://img.shields.io/badge/featured%20skills-10-cyan?style=flat-square&color=00bfff)
![License](https://img.shields.io/badge/license-open%20source-green?style=flat-square)
![Stack](https://img.shields.io/badge/stack-Three.js%20%7C%20React%20Three%20Fiber%20%7C%20TSL-orange?style=flat-square)

</div>

# 🎸 skill-jam

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
├── header.svg             ← Animated banner (v1.1)
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

The `featured-skills/` directory showcases **10 hand-picked, production-quality 3D visualizer skills** built on [Three.js r182+](https://threejs.org/), [React Three Fiber v9](https://docs.pmnd.rs/react-three-fiber), TSL/GLSL shaders, and GPU particle systems. Each visualizer brings a fringe or alternative-physics concept to life with interactive real-time 3D rendering.

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

## 🗂️ All Skills

A complete list of all 50 agent skills in this repository, spanning engineering, data, productivity, research, commerce, and creative domains.

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
