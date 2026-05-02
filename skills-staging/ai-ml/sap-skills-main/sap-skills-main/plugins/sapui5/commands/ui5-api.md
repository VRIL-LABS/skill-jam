---
name: ui5-api
description: Quick API reference lookup for UI5 controls, methods, events, and properties
args:
  - name: control
    description: Control name (e.g., sap.m.Table, Button, List)
    required: true
  - name: member
    description: Optional method, event, or property name
    required: false
---

# UI5 API Reference: {{control}}{{#if member}}.{{member}}{{/if}}

Looking up API documentation for `{{control}}`{{#if member}} member `{{member}}`{{/if}}...

## Quick Reference Lookup

I'll search for API documentation using the ui5-api-explorer agent, which will:

1. **Check MCP availability**: Try official @ui5/mcp-server first
2. **Determine version**: Use your project's UI5 version or latest
3. **Fetch documentation**: Get complete API reference
4. **Generate examples**: Show working code examples
5. **Suggest related**: Recommend related APIs

This provides faster access than visiting ui5.sap.com manually.

---

**Invoking ui5-api-explorer agent...**

*Agent will provide:*
- Full control documentation (if no member specified)
- Specific method/event/property documentation (if member specified)
- Code examples
- Version compatibility
- Common patterns
- Related APIs

---

## Fallback (If Agent Unavailable)

If the agent cannot be invoked, here's manual lookup information:

### Online Documentation

**API Reference**:
```
https://ui5.sap.com/1.120.0/#/api/{{control}}
```

**Samples**:
```
https://ui5.sap.com/1.120.0/#/entity/{{control}}
```

### Local Search

Search your project for existing usage:
```bash
grep -r "{{control}}" webapp/ --include="*.xml" --include="*.js"
```

### Common Controls Quick Reference

**sap.m Library** (Mobile/Responsive):
- `sap.m.Table` - Responsive table for mobile/desktop
- `sap.m.List` - Simple vertical list
- `sap.m.Button` - Standard button
- `sap.m.Input` - Text input field
- `sap.m.Page` - Page container with header/footer
- `sap.m.Dialog` - Modal dialog
- `sap.m.MessageBox` - Alert/confirm dialogs

**sap.ui.table Library** (Desktop Tables):
- `sap.ui.table.Table` - Virtualized table for large datasets
- `sap.ui.table.TreeTable` - Hierarchical tree table

**sap.ui.layout Library**:
- `sap.ui.layout.Grid` - Responsive grid layout
- `sap.ui.layout.Splitter` - Resizable split panes
- `sap.ui.layout.VerticalLayout` - Vertical container

**sap.ui.core Library**:
- `sap.ui.core.mvc.Controller` - MVC controller base
- `sap.ui.core.mvc.View` - MVC view base
- `sap.ui.core.UIComponent` - Component base class

For detailed API documentation, the ui5-api-explorer agent provides comprehensive information with examples.
