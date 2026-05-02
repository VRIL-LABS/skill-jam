# Marketplace Infrastructure

Technical documentation for the SAP Skills marketplace system.

**For implementation guidance**, see the [Contributor Guide](../contributor-guide/README.md).

---

## Overview

The SAP skills repository uses a **marketplace system** to manage 33+ production skills with:
- Coordinated versioning (all at v2.1.1)
- Cross-references between related skills
- Central registry (.claude-plugin/marketplace.json)
- Dual-level manifest architecture

**Scale**: 33 plugins across 5 categories (Tooling, BTP, UI, Data & Analytics, Core Technologies)

---

## Multi-Skill Portfolio Management

### Skill Families

**Tooling & Development** (4 skills):
- skill-review, sap-api-style, sap-hana-cli, sapui5-linter

**SAP BTP Platform** (14 skills):
- sap-btp-best-practices, sap-btp-build-work-zone-advanced, sap-btp-business-application-studio,
  sap-btp-cias, sap-btp-cloud-logging, sap-btp-cloud-platform, sap-btp-cloud-transport-management,
  sap-btp-connectivity, sap-btp-developer-guide, sap-btp-integration-suite,
  sap-btp-intelligent-situation-automation, sap-btp-job-scheduling, sap-btp-master-data-integration,
  sap-btp-service-manager

**UI Development** (4 skills):
- sap-fiori-tools, sapui5, sapui5-cli, sapui5-linter

**Data & Analytics** (5 skills):
- sap-datasphere, sap-sac-custom-widget, sap-sac-planning, sap-sac-scripting,
  sap-hana-cloud-data-intelligence

**Core Technologies** (6 skills):
- sap-abap, sap-abap-cds, sap-cap-capire, sap-sqlscript, sap-ai-core, sap-cloud-sdk-ai, sap-hana-ml

### Cross-Reference Pattern

Related skills should reference each other in their `Related Skills` section:

```markdown
## Related Skills

- **sap-fiori-tools**: Use for UI layer development with Fiori Elements
- **sap-btp-cloud-platform**: Use for BTP deployment and services
- **sap-hana-cli**: Use for database operations
```

This enables Claude to:
- Discover complementary skills automatically
- Suggest related skills when appropriate
- Understand the SAP technology ecosystem

### Coordinated Versioning Strategy

**Single Source of Truth**: `marketplace.json` metadata.version field

**Version Sync Workflow**:
1. Update version in `.claude-plugin/marketplace.json`
2. Run `./scripts/sync-plugins.sh`
3. Script propagates version to all plugin.json files
4. Commit all changes together

**Current Version**: 2.1.1
**Last Updated**: 2026-02-06

---

## Dual-Level Manifest Architecture

SAP skills use a **nested structure** with manifests at two levels:

```
plugins/sap-cap-capire/
├── .claude-plugin/plugin.json          # Plugin-level (root)
├── .mcp.json                           # Optional MCP config
├── agents/                             # Optional specialized agents
├── commands/                           # Optional slash commands
├── hooks/hooks.json                    # Optional hooks
└── skills/sap-cap-capire/              # Skill directory
    ├── .claude-plugin/plugin.json      # Skill-level
    ├── SKILL.md                        # Main skill content
    ├── README.md                       # Keywords for discovery
    ├── references/                     # Documentation
    ├── templates/                      # Code templates
    └── scripts/                        # Executable scripts
```

**Why Two Levels?**

- **Plugin-level** (`plugins/sap-cap-capire/.claude-plugin/plugin.json`):
  - References the entire plugin (skills + agents + commands + hooks)

- **Skill-level** (`plugins/sap-cap-capire/skills/sap-cap-capire/.claude-plugin/plugin.json`):
  - References just the skill content
  - Used by marketplace.json for skill discovery

**Auto-Generation**: Both are generated from SKILL.md YAML frontmatter by `generate-plugin-manifests.sh`

---

## Central Registry System

### marketplace.json Structure

**Location**: `.claude-plugin/marketplace.json`
**Size**: ~48KB (33 plugins)
**Auto-Generated**: By `generate-marketplace.sh`

**Structure**:
```json
{
  "name": "sap-skills",
  "version": "2.1.1",
  "metadata": {
    "version": "2.1.1",
    "last_updated": "2026-02-06",
    "total_skills": 33,
    "categories": [
      "abap", "ai", "btp", "cap",
      "data-analytics", "hana",
      "tooling", "ui-development"
    ]
  },
  "plugins": [
    {
      "name": "sap-cap-capire",
      "description": "...",
      "version": "2.1.1",
      "source": "plugins/sap-cap-capire",
      "license": "GPL-3.0",
      "keywords": [...],
      "category": "cap"
    }
  ]
}
```

**Critical Detail**: `source` field must point to individual plugin directory (e.g., `"plugins/sap-cap-capire"`)
NOT `"./"` to avoid cache duplication (18× bloat).

### Discovery and Installation

**Skill Discovery**:
- Claude reads marketplace.json metadata (name + description)
- Matches keywords to trigger skill loading
- Loads SKILL.md content when triggered

**Manual Installation** (if needed):
```bash
git clone https://github.com/secondsky/sap-skills.git
cd sap-skills
# Skills are auto-discovered by Claude Code
```

### Cross-References Between Skills

**13 skills** have marketplace cross-references via keywords:

Example from sap-cap-capire:
```yaml
keywords:
  - cap
  - cds
  - sap-fiori-tools    # Cross-reference
  - sap-btp-cloud-platform  # Cross-reference
```

This enables portfolio-wide skill discovery.

---

## Related Documentation

- **[Contributor Guide](../contributor-guide/README.md)** - Implementation guidance
- **[Automation Scripts](../contributor-guide/README.md#automation-scripts)** - Script usage
- **[Project Structure](project-structure.md)** - Repository architecture

---

**Last Updated**: 2026-02-06
**Maintainer**: SAP Skills Repository Team
