# Quick Reference: 6-Step Workflow

Fast-track guide for creating and publishing SAP skills.

**For detailed information**, see the [Contributor Guide](../contributor-guide/README.md).

---

## Step 1: Use plugin-dev for Basics

Run: `/use plugin-dev:skill-development`

**This covers**:
- YAML frontmatter creation
- Plugin directory structure
- Resource organization (scripts/, references/, assets/)
- Progressive disclosure patterns

**See**: [plugin-dev documentation](https://github.com/anthropics/skills/tree/main/plugin-dev) for complete guidance

---

## Step 2: Add SAP-Specific Elements

See [Contributor Guide](../contributor-guide/README.md) for detailed patterns.

### SDK Version Tracking
```yaml
metadata:
  version: "2.1.1"
  cap_version: "@sap/cds 9.4.x"
  last_verified: "2025-12-28"
```

### Marketplace Cross-References
```markdown
## Related Skills
- **sap-fiori-tools**: Use for UI layer development
- **sap-btp-cloud-platform**: Use for deployment
```

### Production Testing Requirements
- Test with real SAP BTP account
- Verify templates in production
- Document error catalog with SAP Notes

### Error Catalog Pattern
```markdown
| Error Code | Message | Solution | Source |
|------------|---------|----------|--------|
| D1_ERROR 1105 | Database error | Use batch API | SAP Note 3456789 |
```

---

## Step 3: Generate Manifests

```bash
./scripts/sync-plugins.sh
```

This auto-generates:
- plugin.json files (plugin-level + skill-level)
- Updates marketplace.json
- Validates all 33 skills

---

## Step 4: Quality Review

```bash
/review-skill <skill-name>
```

14-phase comprehensive audit covering:
- YAML validation
- Official docs verification
- Version accuracy
- Template testing
- Error catalog validation

**See**: [quality-assurance.md](../contributor-guide/quality-assurance.md) for detailed review process

---

## Step 5: Verify with Checklist

Use the [Workflow Checklist](../contributor-guide/workflow-checklist.md) for SAP-specific quality checks.

**Key verification points**:
- [ ] SAP SDK versions documented
- [ ] Production testing complete
- [ ] Cross-references added
- [ ] Error catalog validated
- [ ] skill-review passed (all critical issues resolved)

---

## Step 6: Commit

```bash
git add plugins/<skill-name> .claude-plugin/marketplace.json
git commit -m "Add <skill-name> for [SAP technology]

- Provides [key features]
- SAP SDK version: <version>
- Production tested: [evidence]
"
```

**See**: [Git Commit Checklist](../contributor-guide/workflow-checklist.md#git-commit)

---

## Navigation

- **Detailed Guide**: [Contributor Guide](../contributor-guide/README.md)
- **Quality Checklist**: [Workflow Checklist](../contributor-guide/workflow-checklist.md)
- **Installation**: [Installation Guide](installation.md)

---

**Last Updated**: 2026-02-06
