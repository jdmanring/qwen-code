---
name: handle-type-breaking-changes
description: Resolve widespread typecheck errors introduced by dependency upgrades using utility helpers and type narrowing.
source: auto-skill
extracted_at: '2026-06-14T23:45:00.000Z'
---

# Handling Widespread Type Breaking Changes

When a dependency upgrade (e.g., `@types/node` v25) introduces widespread type mismatches—such as changing a return type from `string` to `string | string[]`—follow this systematic approach to resolve them without introducing runtime regressions.

## Procedure

### 1. Identify the Pattern

Run the typecheck for the affected workspace and analyze the errors to find the common pattern.

```bash
npm run typecheck --workspace=packages/<pkg>
```

Look for errors like:
`Argument of type 'string | string[]' is not assignable to parameter of type 'string'.`

### 2. Implement Resolution Helpers

Instead of fixing every instance with inline casts (`as string`), create utility helpers that encapsulate the resolution logic. This ensures consistency and makes future changes easier.

For Express `req.params` and `req.query` mismatches:

```typescript
/**
 * Safely extracts a string parameter from the request.
 * Handles cases where the value might be a string, an array of strings, or undefined.
 */
function getStringParam(req: Request, param: string): string | undefined {
  const value = req.params[param];
  return typeof value === 'string'
    ? value
    : Array.isArray(value)
      ? value[0]
      : undefined;
}

/**
 * Safely extracts a string query parameter from the request.
 * Handles cases where the value might be a string, an array of strings, or undefined.
 */
function getStringQuery(req: Request, query: string): string | undefined {
  const value = req.query[query];
  if (typeof value === 'string') return value;
  if (Array.isArray(value) && typeof value[0] === 'string') return value[0];
  return undefined;
}
```

### 3. Apply Helpers and Implement Type Narrowing

Replace direct access to `req.params` or `req.query` with the helpers. Because the helpers return `string | undefined`, you MUST implement type narrowing immediately after the call to satisfy the TypeScript compiler.

**Incorrect (causes TS error):**

```typescript
const sessionId = getStringParam(req, 'id');
await bridge.closeSession(sessionId); // Error: string | undefined not assignable to string
```

**Correct (type narrowing):**

```typescript
const sessionId = getStringParam(req, 'id');
if (!sessionId) {
  res.status(400).json({ error: '`sessionId` route parameter is required' });
  return;
}
await bridge.closeSession(sessionId); // Now narrowed to string
```

### 4. Verify and Iterate

Run the typecheck again to ensure all instances are resolved and no new errors were introduced.

```bash
npm run typecheck --workspace=packages/<pkg>
```

## Key Principles

- **No Inline Casts**: Avoid `as string` or `(value as string[])[0]`. Use helpers to ensure runtime safety.
- **Fail Fast**: Use the `if (!value) return;` pattern to reject malformed requests at the boundary.
- **Consistency**: Use the same helper for all similar access patterns across the project.
- **Runtime Safety**: Ensure the helper handles all possible types returned by the library (e.g., `ParsedQs` in Express).
