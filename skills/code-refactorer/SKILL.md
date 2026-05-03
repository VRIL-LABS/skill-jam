---
name: code-refactorer
description: Detects code smells (duplication, long methods, god classes) and applies safe, behavior-preserving refactors. Invoke when asked to refactor, clean up, simplify, reduce complexity, or improve the structure of existing code without changing its behavior.
---

# Code Refactorer

Identifies code smells and applies safe, systematic refactoring transformations that improve readability, maintainability, and structure without altering observable behavior.

## When to Use

- User asks to "refactor this", "clean up", "simplify", or "reduce complexity"
- Code review flagged high complexity, duplication, or poor structure
- A function exceeds 40–50 lines or has many nested conditionals
- A class has too many responsibilities (god class)
- Duplicated logic exists across multiple files
- Code fails maintainability or complexity static analysis rules
- User wants to prepare code for adding new features safely

## Process

1. **Identify code smells** by scanning the provided code:
   - **Long Method**: function > ~40 lines; extract smaller focused functions
   - **Duplicate Code**: identical or near-identical blocks; extract to shared helper
   - **Long Parameter List**: >4 parameters; group into a config/options object
   - **God Class**: class with >10 public methods or mixed concerns; split by responsibility
   - **Feature Envy**: method accesses another object's data more than its own; move it
   - **Data Clumps**: same 3+ variables always appear together; create a value object
   - **Switch Statements**: large switch/if-else chains on type; consider polymorphism
   - **Magic Numbers/Strings**: unexplained literals; extract as named constants
   - **Deep Nesting**: >3 levels of nesting; apply early return / guard clauses
   - **Dead Code**: unreachable or unused code; remove it

2. **Prioritize refactors** by impact and safety:
   - Start with renames and constant extraction (zero behavior risk)
   - Then extract methods/functions (low risk)
   - Then restructure classes or move code between modules (higher risk, needs tests)

3. **Verify tests exist** before structural refactors — if not, note the risk and suggest generating tests first using the `test-generator` skill.

4. **Apply refactors one at a time**, explaining each transformation:
   - Name the refactoring pattern (Extract Method, Replace Magic Number, Introduce Guard Clause, etc.)
   - Show before/after code
   - Explain what improved and why the behavior is preserved

5. **Preserve all public interfaces** — do not rename public functions, change parameter order, or alter return types unless explicitly requested.

6. **Update call sites** if a helper is extracted or a parameter is consolidated.

7. **Ensure naming is improved** in the process — refactoring is also an opportunity to rename cryptic variables to expressive ones.

## Output Format

For each refactoring applied:

```
### Refactor 1: Extract Method — `validateUserInput`

**Smell:** Long Method — `registerUser` was 67 lines and mixed validation,
hashing, and persistence logic.

**Before:**
```ts
async function registerUser(data: any) {
  if (!data.email || !data.email.includes('@')) {
    throw new Error('Invalid email');
  }
  if (!data.password || data.password.length < 8) {
    throw new Error('Password too short');
  }
  // ... 50 more lines of hashing + DB logic
}
```

**After:**
```ts
function validateUserInput(data: UserInput): void {
  if (!data.email || !data.email.includes('@')) {
    throw new ValidationError('Invalid email');
  }
  if (!data.password || data.password.length < 8) {
    throw new ValidationError('Password must be at least 8 characters');
  }
}

async function registerUser(data: UserInput) {
  validateUserInput(data);
  // ... hashing + DB logic only
}
```

**Why it's safe:** `validateUserInput` is a pure extraction — same conditions,
same exceptions, same outcomes. All existing callers of `registerUser` are unaffected.
```

## Examples

### Example Input
```python
def process(data):
    if data is not None:
        if isinstance(data, list):
            if len(data) > 0:
                result = []
                for item in data:
                    if item > 0:
                        result.append(item * 2)
                return result
    return []
```

### Example Output
```python
# Refactor 1: Introduce Guard Clauses (eliminates deep nesting)
# Refactor 2: Replace loop with list comprehension (idiomatic Python)

def process(data: list | None) -> list:
    if not data:
        return []
    return [item * 2 for item in data if item > 0]
```

**Changes:**
- Guard clause replaces nested `if not None / isinstance / len > 0` checks
- List comprehension replaces the manual loop (functionally identical)
- Type hints added for clarity
- Behavior preserved: returns `[]` for None, empty list, or all-negative input

## Boundaries

- Do NOT change behavior, return types, or exception semantics during refactoring.
- Do NOT rename public API symbols (exported functions, public class methods) unless the user explicitly requests it.
- Do NOT refactor auto-generated code (migrations, protobuf, gRPC stubs, etc.).
- Do NOT apply refactors that require language features not available in the current target version (e.g., no walrus operator if Python < 3.8).
- Always warn if structural refactors are proposed without an existing test suite.
- Do NOT introduce new dependencies as part of a refactor.
- Limit changes to the provided code scope — do not speculatively refactor other files not shown.
- If a refactor requires understanding cross-file dependencies, request those files before proceeding.
