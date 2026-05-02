---
name: widget-generate
description: Interactively generates SAC custom widget scaffold with widget.json and widget.js files based on user requirements
allowed-tools:
  - Write
  - Read
  - AskUserQuestion
argument-hint: [widget-name]
---

# SAC Custom Widget Generator Command

Interactively create a complete SAP Analytics Cloud custom widget scaffold including widget.json metadata and widget.js Web Component implementation.

## Usage

```
/widget-generate
/widget-generate my-chart-widget
/widget-generate --quick
```

## Interactive Mode (Default)

When invoked without `--quick`, ask the user these questions:

### Required Questions

1. **Widget Name**
   - Display name for SAC (e.g., "My Custom Chart")
   - Will generate tag from this (e.g., "my-custom-chart")

2. **Widget ID**
   - Reverse domain notation (e.g., "com.company.mychart")
   - Default: Generate from widget name

3. **Data Binding**
   - "Does your widget need to bind to SAC model data?"
   - Options: Yes (dimensions + measures), Yes (measures only), No

4. **Components**
   - "Which components do you need?"
   - Options: Main only, Main + Styling Panel, Main + Builder Panel, All three

### Optional Questions

5. **Third-Party Library**
   - "Will you integrate a charting library?"
   - Options: ECharts, D3.js, Chart.js, None

6. **Initial Properties**
   - "What properties should be configurable?"
   - Default: title (string), color (Color)

## Quick Mode (--quick)

Generate minimal widget with defaults:
- Main component only
- No data binding
- Basic title property
- No third-party libraries

## Generated Files

### 1. widget.json

Full metadata file with:
- All required root fields
- webcomponents array based on selection
- properties object with selected properties
- methods object (if applicable)
- events object (if applicable)
- dataBindings object (if data binding selected)

### 2. widget.js

Complete Web Component with:
- Shadow DOM setup
- Template with basic structure
- All lifecycle functions
- Property getters/setters
- propertiesChanged event dispatch
- Placeholder render function
- Third-party library initialization (if selected)

### 3. Additional Files (if applicable)

- `styling-panel.js` - If styling panel selected
- `builder-panel.js` - If builder panel selected

## Output Structure

```
widget-name/
├── widget.json
├── widget.js
├── styling-panel.js    (if selected)
└── builder-panel.js    (if selected)
```

## Generation Templates

### Basic widget.json Template
```json
{
  "id": "com.company.widgetname",
  "version": "1.0.0",
  "name": "Widget Name",
  "description": "A custom widget for SAP Analytics Cloud",
  "vendor": "Company Name",
  "license": "MIT",
  "icon": "",
  "webcomponents": [
    {
      "kind": "main",
      "tag": "widget-name",
      "url": "widget.js",
      "integrity": "",
      "ignoreIntegrity": true
    }
  ],
  "properties": {
    "title": {
      "type": "string",
      "default": "Widget Title"
    }
  },
  "methods": {},
  "events": {}
}
```

### Data Binding Template Addition
```json
{
  "dataBindings": {
    "myData": {
      "feeds": [
        {
          "id": "dimensions",
          "description": "Dimensions",
          "type": "dimension"
        },
        {
          "id": "measures",
          "description": "Measures",
          "type": "mainStructureMember"
        }
      ]
    }
  }
}
```

### Basic widget.js Template
```javascript
(function() {
  const template = document.createElement("template");
  template.innerHTML = `
    <style>
      :host {
        display: block;
        width: 100%;
        height: 100%;
        font-family: var(--sapFontFamily, Arial, sans-serif);
      }
      .container {
        width: 100%;
        height: 100%;
        padding: 16px;
        box-sizing: border-box;
      }
      .title {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 12px;
        color: var(--sapTextColor, #333);
      }
      .content {
        width: 100%;
        height: calc(100% - 40px);
      }
    </style>
    <div class="container">
      <div class="title" id="title"></div>
      <div class="content" id="content"></div>
    </div>
  `;

  class WidgetName extends HTMLElement {
    constructor() {
      super();
      this._shadowRoot = this.attachShadow({ mode: "open" });
      this._shadowRoot.appendChild(template.content.cloneNode(true));
      this._props = {};
    }

    // SAC Lifecycle Functions
    onCustomWidgetBeforeUpdate(changedProperties) {
      this._props = { ...this._props, ...changedProperties };
    }

    onCustomWidgetAfterUpdate(changedProperties) {
      this._render();
    }

    onCustomWidgetResize() {
      this._render();
    }

    onCustomWidgetDestroy() {
      // Cleanup resources here
    }

    // Property getter/setter
    get title() {
      return this._props.title;
    }

    set title(value) {
      this._props.title = value;
      this.dispatchEvent(new CustomEvent("propertiesChanged", {
        detail: { properties: { title: value } }
      }));
    }

    // Render function
    _render() {
      const titleEl = this._shadowRoot.getElementById("title");
      if (titleEl && this._props.title) {
        titleEl.textContent = this._props.title;
      }

      // Add your rendering logic here
    }
  }

  customElements.define("widget-name", WidgetName);
})();
```

## Post-Generation Instructions

After files are generated, provide:

1. **Next Steps**
   - How to add to SAC
   - How to set up hosting
   - How to generate integrity hash

2. **Development Tips**
   - Local development setup
   - Browser DevTools debugging
   - SAC debug mode

3. **Customization Pointers**
   - Where to add visualization logic
   - How to add more properties
   - How to implement events

## Implementation Instructions

When this command is invoked:

1. If widget name provided, use it; otherwise ask
2. Ask interactive questions based on mode
3. Generate widget.json with all selections
4. Generate widget.js with matching implementation
5. Generate additional component files if selected
6. Write all files to specified or current directory
7. Provide post-generation instructions
8. Suggest running `/widget-validate` to verify
