---
name: api-scaffolder
description: Generates REST or GraphQL API boilerplate — controllers, routes, models, and validation — from an OpenAPI spec or description. Invoke when asked to scaffold an API, generate CRUD endpoints, create route handlers, or bootstrap a new API service.
---

# API Scaffolder

Generates production-ready REST or GraphQL API boilerplate from an OpenAPI specification or a natural-language description of resources and operations. Output includes routes, controllers, models, validation schemas, and error handling.

## When to Use

- User provides an OpenAPI 3.x spec and wants implementation scaffolded
- User describes API resources ("I need CRUD endpoints for users and posts")
- Starting a new microservice and need a consistent structure
- User asks to add a new resource to an existing API following current conventions
- Generating client SDKs or server stubs from a spec

## Process

1. **Identify the target framework** from context or ask:
   - Node.js: Express, Fastify, NestJS, Hono
   - Python: FastAPI, Flask, Django REST Framework
   - Go: net/http, Gin, Echo, Chi
   - Java: Spring Boot
   - Ruby: Rails API mode, Sinatra

2. **Parse the input** — OpenAPI spec or natural-language description:
   - For OpenAPI: extract paths, methods, request/response schemas, security schemes
   - For descriptions: infer resources, standard CRUD operations, and field types

3. **Design the file structure** following the detected or standard project layout:
   ```
   src/
     routes/          # route definitions
     controllers/     # request handlers
     services/        # business logic
     models/          # DB models / entities
     validators/      # request validation schemas
     middleware/       # auth, logging, error handling
   ```

4. **Generate each layer**:

   **Routes** — map HTTP methods + paths to controller functions:
   ```
   GET    /users         → UserController.list
   POST   /users         → UserController.create
   GET    /users/:id     → UserController.getById
   PUT    /users/:id     → UserController.update
   DELETE /users/:id     → UserController.delete
   ```

   **Controllers** — thin handlers: validate input → call service → return response:
   - Extract and validate path/query params and request body
   - Call the appropriate service method
   - Map service result to HTTP response (201 for create, 204 for delete, etc.)
   - Catch and forward errors to the error middleware

   **Services** — business logic, decoupled from HTTP:
   - Implement actual CRUD operations against the model
   - Throw typed errors (NotFoundError, ConflictError) rather than HTTP status codes

   **Models** — database schema/entity definitions:
   - Include all fields with types, constraints, and defaults
   - Add timestamps (`createdAt`, `updatedAt`) by default
   - Define associations/relations if described

   **Validators** — request body/param schemas:
   - Use Zod, Joi, Pydantic, class-validator, or idiomatic framework validation
   - Validate types, required fields, string lengths, enum values, formats

5. **Generate error handling middleware** that maps typed errors to HTTP status codes.

6. **Add basic authentication middleware** placeholder (or full implementation if auth type is specified).

7. **Include a router index** that mounts all generated routes with appropriate prefixes.

## Output Format

Produce a set of files with clear filenames. For each file, show the complete content:

```
### src/routes/users.routes.ts
```ts
import { Router } from 'express';
import { UserController } from '../controllers/users.controller';
import { validateBody } from '../middleware/validate';
import { CreateUserSchema, UpdateUserSchema } from '../validators/users.schema';

const router = Router();

router.get('/', UserController.list);
router.post('/', validateBody(CreateUserSchema), UserController.create);
router.get('/:id', UserController.getById);
router.put('/:id', validateBody(UpdateUserSchema), UserController.update);
router.delete('/:id', UserController.delete);

export default router;
```

### src/controllers/users.controller.ts
```ts
import { Request, Response, NextFunction } from 'express';
import { UserService } from '../services/users.service';

export class UserController {
  static async list(req: Request, res: Response, next: NextFunction) {
    try {
      const users = await UserService.findAll();
      res.json(users);
    } catch (err) { next(err); }
  }
  // ... create, getById, update, delete
}
```
```

## Examples

### Example Input
```
Scaffold a REST API for a blog platform. Resources:
- Post: title (string, required), body (text, required), authorId (uuid), published (bool, default false)
- Comment: postId (uuid), authorId (uuid), content (string, 1-500 chars)
Framework: FastAPI (Python)
```

### Example Output (summary)
```
Files generated:
- app/routes/posts.py       — GET /posts, POST /posts, GET/PUT/DELETE /posts/{id}
- app/routes/comments.py    — GET /posts/{id}/comments, POST /posts/{id}/comments
- app/controllers/posts.py  — list_posts, create_post, get_post, update_post, delete_post
- app/services/posts.py     — business logic + DB queries
- app/models/post.py        — SQLAlchemy model with id, title, body, author_id, published, created_at
- app/schemas/post.py       — Pydantic: PostCreate, PostUpdate, PostResponse
- app/main.py               — FastAPI app with routers mounted at /api/v1
```

## Boundaries

- Do NOT generate database migration files — note that migrations must be created separately using the ORM CLI.
- Do NOT hardcode database credentials or secrets — use environment variables with `.env` placeholders.
- Do NOT implement authentication logic unless explicitly requested — add a middleware stub with a TODO comment.
- Do NOT generate frontend code from this skill — use the appropriate frontend scaffolding approach.
- If the OpenAPI spec contains conflicting schemas, flag the conflict and use the most restrictive interpretation.
- Generate only the layers explicitly requested; do not add layers the user did not ask for unless they are minimal and required for the code to function.
