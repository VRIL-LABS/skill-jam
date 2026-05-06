---
name: codebase-recon
description: >
  Ultra-dense, full-spectrum codebase reconnaissance skill exclusively by VRIL LABS. Chains every
  major and obscure code repository platform and cross-repository search engine—leveraging free
  APIs wherever available—to systematically discover, evaluate, and document high-signal reference
  codebases in a dedicated REFERENCE_REPOS.md file, saving development time and elevating output
  quality on any current task. Invoke when asked to find reference implementations, build a
  reference corpus, scout existing solutions, discover similar projects, or research how a
  technology is used across the open-source ecosystem.
---

# Codebase Recon

*Exclusively by VRIL LABS*

Ultra-dense, full-spectrum codebase reconnaissance that chains together every major and emerging code repository platform. Systematically discovers, evaluates, and documents the highest-signal reference codebases into a dedicated `REFERENCE_REPOS.md` corpus—accelerating development by surfacing battle-tested patterns, canonical implementations, and edge-case solutions before a single line of new code is written.

## When to Use

- User needs reference implementations before beginning a complex feature or system
- Current task involves a technology, pattern, or API the agent is less familiar with
- User asks to "find examples of", "look up how others have done", or "research existing codebases"
- Building a new module and canonical open-source patterns would accelerate or de-risk the work
- User asks to "build a reference corpus", "scout similar projects", or "document reference repos"
- Starting a new project where analogous open-source projects serve as architectural north stars
- Security review where studying hardened implementations improves assurance
- Debugging a subtle issue that may already have known solutions in the wild

## Process

### Phase 1 — Define Reconnaissance Scope

1. **Extract the reconnaissance brief** from the current task context:
   - Primary technology/language/framework
   - Feature or pattern category (e.g., "rate limiter", "OAuth flow", "distributed lock")
   - Quality signals required (stars, recency, test coverage, production use)
   - Output fidelity needed (a handful of targeted repos vs. a broad corpus)

2. **Decompose into 3–5 search axes**:
   - Canonical implementations (official libraries, reference impls)
   - Production examples (large deployed codebases using the pattern)
   - Edge-case or advanced usage (unusual combinations, performance-critical variants)
   - Alternative approaches (different stacks, languages, paradigms)
   - Emerging or cutting-edge implementations (recent repositories, research prototypes)

### Phase 2 — Primary Repository Platforms (Tier 1)

Search all Tier-1 platforms in parallel. Use free API endpoints where available.

#### 2a. GitHub (github.com)
- **Code Search API**: `GET https://api.github.com/search/code?q=<query>+language:<lang>`
- **Repository Search**: `GET https://api.github.com/search/repositories?q=<topic>&sort=stars`
- **Advanced operators**: `in:file`, `filename:`, `path:`, `repo:`, `org:`, `topic:`, `language:`, `stars:>N`, `pushed:>YYYY-MM-DD`
- **Semantic code search**: `https://github.com/search?type=code` (web UI, supports natural language)
- **Rate limit**: 10 unauthenticated req/min; 30 with token. Cache results between axes.

#### 2b. GitLab (gitlab.com)
- **Repository Search**: `GET https://gitlab.com/api/v4/search?scope=projects&search=<query>`
- **Code/Blob Search**: `GET https://gitlab.com/api/v4/search?scope=blobs&search=<query>`
- **Group Search**: `GET https://gitlab.com/api/v4/groups/<id>/search?scope=blobs&search=<query>`
- Especially valuable for DevSecOps patterns, CI/CD configs, and self-hosted infrastructure.

#### 2c. Bitbucket (bitbucket.org)
- **Repository Search**: `GET https://api.bitbucket.org/2.0/repositories?q=name~"<query>"`
- Strong for Atlassian-ecosystem integrations (Jira, Confluence, Bamboo).

#### 2d. Codeberg (codeberg.org) — Forgejo/Gitea API
- **Repository Search**: `GET https://codeberg.org/api/v1/repos/search?q=<query>&limit=20`
- **Code Search**: `GET https://codeberg.org/api/v1/repos/search?topic=true&q=<topic>`
- Privacy-first, FOSS-only hosting; valuable for permissively licensed reference implementations.

### Phase 3 — Cross-Repository Search Engines (Tier 1 Amplifiers)

These engines index millions of repos and dramatically increase throughput.

#### 3a. Sourcegraph (sourcegraph.com)
- **GraphQL API**: `POST https://sourcegraph.com/.api/graphql`
- Query syntax: `<pattern> lang:<language> repo:github.com/<org>/.*`
- Structural search: `comby:...` patterns for AST-aware matching
- Cross-repo intelligence: symbol definitions, references, call graphs
- Free for public code. No API key required for read-only public search.

#### 3b. searchcode.com
- **Search API**: `GET https://searchcode.com/api/search/?q=<query>&lan=<language_id>`
- **Code Result API**: `GET https://searchcode.com/api/result/<result_id>/`
- Indexes 90B+ lines of code across GitHub, GitLab, Bitbucket, Google Code, Codeplex.
- Explicitly designed for LLM/agent consumption. Free for public code.

#### 3c. grep.app
- **Web**: `https://grep.app/search?q=<query>&filter[lang][0]=<Language>`
- Searches 1M+ public GitHub repos with instant regex and string matching.
- No official API; use as a verification and discovery web interface.

#### 3d. Libraries.io
- **Search API**: `GET https://libraries.io/api/search?q=<query>&platforms=<platform>&api_key=<key>`
- **Project API**: `GET https://libraries.io/api/<platform>/<package>?api_key=<key>`
- Indexes 11M+ packages across 30+ ecosystems. Free tier: 60 req/min.
- Use to discover the most-depended-upon packages for a given domain.

### Phase 4 — Niche and Specialized Platforms (Tier 2)

Search selectively based on task context.

#### 4a. SourceForge (sourceforge.net)
- **Project Search API**: `GET https://sourceforge.net/api/project/get/?q=<query>&limit=20&api_key=<key>`
- Legacy but valuable: enormous catalog of C/C++, Java, and Python projects predating GitHub.
- Ideal for: embedded systems, audio DSP, scientific computing, legacy protocol implementations.

#### 4b. Gitea (gitea.com / gitea.io)
- **API**: `GET https://gitea.com/api/v1/repos/search?q=<query>&limit=20`
- Growing ecosystem of self-hosted instances with public APIs at their own domains.

#### 4c. SourceHut / sr.ht (sr.ht)
- **API**: `https://meta.sr.ht/api/` with per-service endpoints (git.sr.ht, builds.sr.ht)
- Preferred by hacker/minimalist community; email-patch workflow; unique Mercurial repos.

#### 4d. Pagure (pagure.io)
- **API**: `GET https://pagure.io/api/0/projects?pattern=<query>`
- Fedora ecosystem: RPM packaging, kernel modules, system software.

#### 4e. Gitee (gitee.com)
- **API**: `GET https://gitee.com/api/v5/search/repositories?q=<query>&access_token=<token>`
- Essential for Chinese open-source ecosystem, large-scale system software, and Go/Java projects.

#### 4f. Phorge / Phabricator instances
- **Conduit API**: `POST https://<instance>/api/diffusion.repository.search`
- Used by large organizations (Mozilla, Wikimedia, Facebook legacy). High-quality codebases.

#### 4g. Gerrit instances (android.googlesource.com, chromium.googlesource.com)
- **REST API**: `GET https://<gerrit-host>/r/projects/?d&type=CODE`
- **Code Search**: `GET https://cs.android.com/` (Android code search)
- Authoritative for Android/Chrome/AOSP patterns.

#### 4h. Apache Allura (forge-allura.apache.org)
- **REST API**: `GET https://forge-allura.apache.org/rest/p/<project>/`
- Apache Software Foundation projects. Authoritative for Java middleware, distributed systems.

#### 4i. GNU Savannah (savannah.gnu.org)
- **Browse**: `https://savannah.gnu.org/search/?type_of_search=soft&Search=<query>`
- GNU/FSF canonical implementations. Especially valuable for C, POSIX, and system libraries.

#### 4j. Notabug (notabug.org) — Gogs API
- `GET https://notabug.org/api/v1/repos/search?q=<query>`
- Privacy-focused FOSS projects.

#### 4k. Launchpad (launchpad.net)
- **API**: `GET https://api.launchpad.net/1.0/projects?ws.op=searchProjects&text=<query>`
- Ubuntu/Canonical ecosystem: daemons, packaging, snap packages, system init.

#### 4l. Radicle (radicle.xyz)
- **HTTP API**: `GET https://seed.radicle.xyz/api/v1/repos`
- Decentralized/P2P code. Leading edge of sovereign, censorship-resistant development.

### Phase 5 — Package Registry Code Discovery (Tier 2 Amplifiers)

Pivot from repositories to packages for implementation-level discovery.

| Registry | Search Endpoint | Ecosystem |
|----------|----------------|-----------|
| **npm** | `https://registry.npmjs.org/-/v1/search?text=<query>` | JavaScript/TypeScript |
| **npms.io** | `https://api.npms.io/v2/search?q=<query>` | JS quality scoring |
| **PyPI** | `https://pypi.org/pypi/<pkg>/json` | Python |
| **crates.io** | `https://crates.io/api/v1/crates?q=<query>` | Rust |
| **Maven Central** | `https://search.maven.org/solrsearch/select?q=<query>&wt=json` | JVM |
| **Hex.pm** | `https://hex.pm/api/packages?search=<query>` | Elixir/Erlang |
| **Pub.dev** | `https://pub.dev/api/search?q=<query>` | Dart/Flutter |
| **Packagist** | `https://packagist.org/search.json?q=<query>` | PHP/Composer |
| **RubyGems** | `https://rubygems.org/api/v1/search.json?query=<query>` | Ruby |
| **NuGet** | `https://azuresearch-usnc.nuget.org/query?q=<query>` | .NET |
| **Go Modules** | `https://pkg.go.dev/search?q=<query>` | Go |

For each top-scoring package: fetch source link → pivot to GitHub/GitLab to inspect full repo.

### Phase 6 — Specialized Domain Sources (Tier 3)

Use selectively for niche, academic, or archival tasks.

- **Hugging Face Hub**: `GET https://huggingface.co/api/models?search=<query>` — ML model repos with code
- **Papers with Code**: `https://paperswithcode.com/api/v1/papers/?q=<query>` — Academic implementations
- **Software Heritage**: `https://archive.softwareheritage.org/api/1/origin/search/<query>/` — Universal source archive
- **Zenodo**: `GET https://zenodo.org/api/records?q=<query>&type=software` — Citable research software
- **OpenHub / Open Hub**: `GET https://www.openhub.net/projects.xml?query=<query>&api_key=<key>` — OSS project analytics
- **OSS Insight**: `https://ossinsight.io/` — GitHub analytics, trending repos, language stats

### Phase 7 — Distro & Ecosystem Forges (Tier 3)

- **Debian / Salsa**: `https://salsa.debian.org/api/v4/projects?search=<query>` — Debian packaging
- **Fedora / dist-git**: `https://src.fedoraproject.org/api/0/projects?pattern=<query>` — Fedora packages
- **GNOME GitLab**: `https://gitlab.gnome.org/api/v4/projects?search=<query>` — GNOME ecosystem
- **KDE Invent**: `https://invent.kde.org/api/v4/projects?search=<query>` — KDE/Qt ecosystem
- **freedesktop.org**: `https://gitlab.freedesktop.org/api/v4/projects?search=<query>` — X11, Wayland, Mesa
- **Android AOSP**: `https://android.googlesource.com/?format=JSON` — Android source tree
- **Chromium**: `https://chromium.googlesource.com/?format=JSON` — Chrome/Chromium

### Phase 8 — Evaluate and Triage

For every discovered repository, score it on these signals:

| Signal | Weight | Notes |
|--------|--------|-------|
| Stars / forks | High | Proxy for community validation |
| Last commit date | High | Staleness kills relevance |
| Test coverage | High | Quality indicator |
| Issue/PR activity | Medium | Health of community |
| README quality | Medium | Documentation density |
| License | Medium | Must match project constraints |
| Dependency count | Low | Simpler = more portable patterns |
| CI/CD presence | Low | Indicates production readiness |

**Triage tiers**:
- 🟢 **Tier 1 Reference** — High stars, recent activity, tests, good docs; study in depth
- 🟡 **Tier 2 Reference** — Moderate signals; scan for specific patterns
- 🔵 **Tier 3 Awareness** — Notable but dated or narrow; link only
- ⬛ **Exclude** — Abandoned, toy projects, or redundant with a Tier 1 entry

### Phase 9 — Build REFERENCE_REPOS.md

Create or update a `REFERENCE_REPOS.md` file at the project root (or in the relevant module directory if scoped). Structure:

```markdown
# Reference Repositories

> Generated by the Codebase Recon skill — VRIL LABS
> Task context: <brief description>
> Generated: <YYYY-MM-DD>

## Tier 1 — Primary References

### <Repo Name>
- **URL**: https://github.com/org/repo
- **Platform**: GitHub
- **Stars**: 12,400 | **Last Commit**: 2025-03-14
- **Language**: TypeScript | **License**: MIT
- **Why relevant**: <1–2 sentence rationale tied to the current task>
- **Key files/patterns to study**:
  - `src/core/ratelimiter.ts` — token bucket implementation
  - `tests/integration/ratelimiter.test.ts` — edge-case coverage

...

## Tier 2 — Supporting References
...

## Tier 3 — Awareness
...

## Search Queries Used
- GitHub: `rate limiter language:typescript stars:>500`
- Sourcegraph: `TokenBucket lang:typescript repo:github.com/.*`
- searchcode: `token_bucket_rate_limiter language:4`
```

### Phase 10 — Synthesis Note

After building `REFERENCE_REPOS.md`, write a concise synthesis block at the top of the file (or return inline) covering:
- Dominant implementation approaches observed across repos
- Consensus patterns vs. areas of divergence
- Critical edge cases seen in multiple codebases
- Any surprising or counter-conventional patterns worth noting

## Output Format

```
## Codebase Recon Complete

**Platforms searched:** 8 of 28 applicable
**Repositories evaluated:** 34
**REFERENCE_REPOS.md:** Created / Updated at `./REFERENCE_REPOS.md`

### Synthesis
[3–5 sentences covering dominant patterns, notable divergences, and recommended study order]

### Top 3 Tier-1 References
1. **org/repo** — [one-line rationale]
2. **org/repo** — [one-line rationale]
3. **org/repo** — [one-line rationale]

Full corpus documented in REFERENCE_REPOS.md.
```

## Examples

### Example Input
```
Before I implement a distributed rate limiter for our Node.js API gateway, research how this
has been done across the open-source ecosystem. Build a REFERENCE_REPOS.md for me.
```

### Example Output
```
## Codebase Recon Complete

**Platforms searched:** 6 (GitHub, GitLab, Sourcegraph, searchcode.com, npm, Libraries.io)
**Repositories evaluated:** 27
**REFERENCE_REPOS.md:** Created at ./REFERENCE_REPOS.md

### Synthesis
Token bucket and sliding window log are the dominant approaches; Redis-backed implementations
account for 70% of production-grade examples. Key divergence: some repos use Lua scripts
for atomic Redis operations while others rely on distributed locking. The `node-rate-limiter-flexible`
library is the clear Tier-1 reference with 40+ strategies, Redis/Memcached support, and
1,700+ tests. Study `rate-limiter-flexible` and Cloudflare's `itty-router-extras` for edge
deployment patterns.

### Top 3 Tier-1 References
1. animir/node-rate-limiter-flexible — most comprehensive Node.js rate limiting library, 40+ strategies
2. tj/node-ratelimiter — minimal, Redis-backed; study for simplicity of the core algorithm
3. microlinkhq/limit-it — in-memory, token bucket; excellent test coverage for edge cases
```

## Boundaries

- Always document what was searched (platforms, queries) in the output and in `REFERENCE_REPOS.md` for reproducibility.
- Do NOT include repositories with licenses incompatible with the user's project constraints without an explicit warning.
- Do NOT blindly copy code from references — use them to inform design, understand trade-offs, and recognize patterns.
- Do NOT include toy "hello world" or tutorial repos unless the task is explicitly instructional.
- Respect rate limits across all APIs — add delays between bulk requests and cache results within a session.
- If an API requires a key that is unavailable, fall back to the web UI search interface and note the limitation.
- For REFERENCE_REPOS.md: if the file already exists, append a new dated section rather than overwriting.
- Limit `REFERENCE_REPOS.md` to ≤30 repos by default; surface the highest-signal subset unless the user requests exhaustive coverage.
