---
name: data-validator
description: Generates JSON Schema, Pydantic models, or Zod schemas from sample data or descriptions to enforce data contracts. Invoke when asked to validate data, create a schema, define a data model, generate Pydantic or Zod types, or enforce a data contract.
---

# Data Validator

Generates precise validation schemas — JSON Schema, Pydantic models, Zod schemas, TypeScript types, or database constraints — from sample data, descriptions, or existing types to enforce data contracts at API boundaries, configuration files, and service interfaces.

## When to Use

- User provides sample JSON/YAML and asks to "create a schema for this"
- API endpoints accept unvalidated request bodies
- User asks to generate Pydantic models, Zod schemas, or JSON Schema
- TypeScript types exist but need runtime validation added
- Configuration files need validation before the app starts
- Data pipelines need input/output contracts enforced
- User asks to convert between schema formats (JSON Schema → Zod, etc.)

## Process

1. **Identify the target schema format** from context or ask:
   - **JSON Schema (draft-07 / 2020-12)** — language-agnostic, OpenAPI, configs
   - **Pydantic v2** — Python, FastAPI, data validation + serialization
   - **Zod** — TypeScript/JavaScript, runtime type-safe validation
   - **Yup** — JavaScript, form validation, React integrations
   - **Joi** — Node.js, server-side validation
   - **TypeBox** — TypeScript, JSON Schema + TypeScript types in sync
   - **class-validator + class-transformer** — NestJS, decorators
   - **OpenAPI requestBody schema** — API spec validation

2. **Analyze the input** (sample data, description, or existing type):
   - Identify all fields and their data types
   - Infer required vs. optional fields from multiple samples or description
   - Determine string formats: email, UUID, URL, date-time, ISO 8601
   - Determine numeric constraints: min, max, integer vs. float
   - Identify array item types and length constraints
   - Identify enum/union types from repeated patterns
   - Note nullable vs. undefined vs. missing field semantics

3. **Design the schema**:
   - Use the most precise constraints possible (don't use `string` when `email` or `uuid` is more accurate)
   - Mark required fields explicitly; make optional fields clear
   - Add minimum/maximum for numbers where semantics imply bounds (age: 0–150, port: 1–65535)
   - Use `minLength`/`maxLength` for strings with natural bounds
   - Use `additionalProperties: false` in JSON Schema for strict objects
   - Use discriminated unions for polymorphic types

4. **Add validation messages** where the framework supports it (Zod, Yup, Pydantic):
   - Provide human-readable error messages for each constraint
   - Include field name and the constraint that failed

5. **Generate the schema with documentation**:
   - Add inline comments or field-level descriptions
   - Include example values where supported

6. **If converting between formats**, ensure semantic equivalence and note any features not supported in the target format.

## Output Format

### Pydantic v2 (Python)
```python
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    viewer = "viewer"
    editor = "editor"

class CreateUserRequest(BaseModel):
    model_config = {"str_strip_whitespace": True}

    name: str = Field(min_length=1, max_length=100, description="Full display name")
    email: EmailStr = Field(description="Primary email address")
    role: UserRole = Field(default=UserRole.viewer)
    age: Optional[int] = Field(default=None, ge=0, le=150)

    @field_validator('name')
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Name must not be blank or whitespace only')
        return v
```

### Zod (TypeScript)
```ts
import { z } from 'zod';

const UserRole = z.enum(['admin', 'viewer', 'editor']);

export const CreateUserSchema = z.object({
  name: z.string().min(1, 'Name is required').max(100, 'Name too long').trim(),
  email: z.string().email('Invalid email address'),
  role: UserRole.default('viewer'),
  age: z.number().int().min(0).max(150).optional(),
});

export type CreateUserRequest = z.infer<typeof CreateUserSchema>;
```

## Examples

### Example Input
```json
{
  "orderId": "ord_abc123",
  "customerId": "cus_xyz456",
  "items": [
    { "productId": "prod_001", "quantity": 2, "unitPrice": 29.99 }
  ],
  "shippingAddress": {
    "street": "123 Main St",
    "city": "Springfield",
    "country": "US",
    "postalCode": "62701"
  },
  "createdAt": "2024-03-15T10:30:00Z"
}
```

### Example Output (JSON Schema)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["orderId", "customerId", "items", "shippingAddress", "createdAt"],
  "additionalProperties": false,
  "properties": {
    "orderId": { "type": "string", "pattern": "^ord_[a-z0-9]+$" },
    "customerId": { "type": "string", "pattern": "^cus_[a-z0-9]+$" },
    "items": {
      "type": "array", "minItems": 1,
      "items": {
        "type": "object",
        "required": ["productId", "quantity", "unitPrice"],
        "additionalProperties": false,
        "properties": {
          "productId": { "type": "string" },
          "quantity": { "type": "integer", "minimum": 1 },
          "unitPrice": { "type": "number", "minimum": 0, "exclusiveMinimum": 0 }
        }
      }
    },
    "shippingAddress": {
      "type": "object",
      "required": ["street", "city", "country", "postalCode"],
      "properties": {
        "street": { "type": "string", "minLength": 1 },
        "city": { "type": "string", "minLength": 1 },
        "country": { "type": "string", "pattern": "^[A-Z]{2}$" },
        "postalCode": { "type": "string" }
      }
    },
    "createdAt": { "type": "string", "format": "date-time" }
  }
}
```

## Boundaries

- Do NOT infer required fields from a single sample — ask for multiple examples or an authoritative description to distinguish required from optional.
- Do NOT use `any` / `object` / `unknown` types without noting that they weaken the contract.
- Do NOT generate validation that strips or transforms data unless the user explicitly requests coercion (i.e., prefer strict validation over silent mutation).
- If converting between schema formats, note any expressiveness gaps (e.g., JSON Schema `contentMediaType` has no direct Zod equivalent).
- Do NOT generate schemas that accept user-controlled data without length constraints — always bound strings and arrays.
- Pydantic v2 syntax differs significantly from v1 — confirm the version before generating code.
