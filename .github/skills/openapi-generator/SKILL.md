---
name: openapi-generator
description: Generates OpenAPI 3.x specifications from annotated code, existing routes, or natural-language descriptions, and vice versa. Invoke when asked to generate an OpenAPI spec, create API documentation, scaffold code from a spec, convert route definitions to OpenAPI, or produce a Swagger file.
---

# OpenAPI Generator

Generates complete, valid OpenAPI 3.x specifications from annotated source code, existing route definitions, or natural-language API descriptions — and conversely, generates server stubs, client SDKs, and typed models from existing OpenAPI specs.

## When to Use

- User asks to "generate an OpenAPI spec", "create a Swagger file", or "document this API"
- Existing API routes need to be formalized into a spec for consumers
- User wants to generate TypeScript types, Python models, or a client SDK from a spec
- A new API is being designed and needs a spec-first approach
- User asks to validate or lint an existing OpenAPI document
- Frontend and backend teams need a contract to develop against independently

## Process

### Path A: Code → OpenAPI Spec

1. **Detect the framework and routing conventions**:
   - Express.js/Fastify: scan route definitions (`router.get`, `app.post`, etc.)
   - FastAPI: read route decorators (`@app.get`, `@router.post`) and type annotations
   - Django REST Framework: extract from ViewSets, serializers, and URL patterns
   - Spring Boot: parse `@RestController`, `@RequestMapping`, `@GetMapping` annotations
   - Rails: parse `routes.rb` and controller actions

2. **Extract route information**:
   - HTTP method and path
   - Path parameters (`:id`, `{id}`) with types
   - Query parameters with types and required/optional status
   - Request body schema (from Pydantic model, Zod schema, TypeScript interface, etc.)
   - Response schemas (from return type annotations or JSDoc `@returns`)
   - Authentication requirements (from middleware or security annotations)
   - Error response codes (from exception handling)

3. **Build the OpenAPI document structure**:
   - `openapi: "3.1.0"` header
   - `info`: title, version, description, contact, license
   - `servers`: list of deployment environments
   - `paths`: organized by resource, then by HTTP method
   - `components/schemas`: reusable schema definitions (avoid inline repetition)
   - `components/securitySchemes`: auth definitions (BearerAuth, ApiKeyAuth, OAuth2)
   - `tags`: group endpoints by resource/domain

4. **Write detailed operation objects** for each endpoint:
   - `summary`: one-line description (verb + noun: "Create a new user")
   - `description`: longer explanation if needed
   - `operationId`: camelCase unique identifier (`createUser`, `listProducts`)
   - `parameters`: path, query, header params with schemas and descriptions
   - `requestBody`: required flag, content type, schema reference
   - `responses`: status codes with descriptions and schema references
   - `security`: which scheme applies to this operation
   - `tags`: which group this endpoint belongs to

### Path B: OpenAPI Spec → Code

5. **Validate the spec first**:
   - Check for missing `$ref` targets
   - Verify all operations have `operationId`
   - Confirm all referenced schemas are defined in `components/schemas`
   - Ensure all security schemes referenced in operations are defined

6. **Generate target artifacts** based on request:
   - **Server stub**: route handlers with proper request/response types, TODO implementations
   - **TypeScript types**: interfaces for all request/response schemas
   - **Python Pydantic models**: from schema definitions
   - **Client SDK**: typed fetch/axios wrapper for each operation

## Output Format

### OpenAPI 3.1 Spec (YAML)
```yaml
openapi: "3.1.0"
info:
  title: Products API
  version: "1.0.0"
  description: |
    API for managing products in the e-commerce catalog.

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging.api.example.com/v1
    description: Staging

security:
  - BearerAuth: []

tags:
  - name: products
    description: Product catalog management

paths:
  /products:
    get:
      tags: [products]
      summary: List products
      operationId: listProducts
      parameters:
        - name: page
          in: query
          schema: { type: integer, minimum: 1, default: 1 }
        - name: limit
          in: query
          schema: { type: integer, minimum: 1, maximum: 100, default: 20 }
        - name: category
          in: query
          schema: { type: string }
          description: Filter by product category
      responses:
        "200":
          description: Paginated list of products
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ProductListResponse' }
        "401":
          $ref: '#/components/responses/Unauthorized'

    post:
      tags: [products]
      summary: Create a product
      operationId: createProduct
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/CreateProductRequest' }
      responses:
        "201":
          description: Product created
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Product' }
        "422":
          $ref: '#/components/responses/ValidationError'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    Product:
      type: object
      required: [id, name, price, createdAt]
      properties:
        id: { type: string, format: uuid }
        name: { type: string, minLength: 1, maxLength: 200 }
        price: { type: number, format: float, minimum: 0, exclusiveMinimum: 0 }
        createdAt: { type: string, format: date-time }

  responses:
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            type: object
            properties:
              error: { type: string, example: "Invalid or missing token" }
```

## Examples

### Example Input (route → spec)
```python
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, db: Session = Depends(get_db)):
    """Fetch a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Example Output
```yaml
/users/{userId}:
  get:
    summary: Fetch a user by ID
    operationId: getUser
    tags: [users]
    parameters:
      - name: userId
        in: path
        required: true
        schema: { type: string, format: uuid }
    responses:
      "200":
        description: User found
        content:
          application/json:
            schema: { $ref: '#/components/schemas/UserResponse' }
      "404":
        description: User not found
        content:
          application/json:
            schema: { $ref: '#/components/schemas/ErrorResponse' }
```

## Boundaries

- Do NOT generate specs with `additionalProperties: true` on request body schemas — prefer explicit, strict schemas for API contracts.
- Do NOT use OpenAPI 2.0 (Swagger) format unless explicitly requested — default to OpenAPI 3.1.0.
- Do NOT include implementation details (database queries, service internals) in the spec — only the HTTP interface contract.
- When generating specs from code, note that the spec represents the current implementation and may not capture undocumented edge cases.
- Do NOT generate client SDKs for languages not clearly specified — ask before generating multi-language output.
- Validate the generated YAML is well-formed before outputting — pay attention to indentation and `$ref` paths.
- If a framework uses code-first doc generation (FastAPI auto-docs, NestJS Swagger), recommend using the built-in tooling rather than maintaining a separate spec file.
