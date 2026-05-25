# Tool Developer Guide: Qwen Code

This guide provides the technical blueprint for implementing new built-in tools in Qwen Code. Tools are the primary mechanism by which the LLM interacts with the local environment, providing the "hands" for the agent's "brain."

---

## 1. Architecture: Validation vs. Execution

Qwen Code employs a strict separation between **Tool Definition (Validation)** and **Tool Execution**. This ensures that parameters are sanitized and validated before any side-effect-producing code is run.

### The Tool $\to$ Invocation Split
- **`DeclarativeTool`**: Defines the "What." It contains the tool's name, description, and the JSON Schema that the LLM uses to generate arguments. Its primary job is to `build()` a validated invocation.
- **`ToolInvocation`**: Defines the "How." It encapsulates a specific, validated call. It handles the actual execution logic, permission checks, and the generation of user-facing confirmation dialogs.

**Logic Flow:**  
`LLM Request` $\to$ `DeclarativeTool.build(params)` $\to$ `ToolInvocation.execute()` $\to$ `ToolResult`

---

## 2. Implementation Blueprint

To create a new tool, you must implement two classes: a `DeclarativeTool` and a `ToolInvocation`.

### Step 1: The Tool Definition (`DeclarativeTool`)
Extend `BaseDeclarativeTool<TParams, TResult>`.

| Property | Role | Requirement |
| :--- | :--- | :--- |
| `name` | Internal ID used by the LLM. | Required |
| `displayName` | User-friendly name for the UI. | Required |
| `description` | Detailed explanation of the tool's purpose. | Required |
| `kind` | Category (e.g., `Kind.Read`, `Kind.Execute`). | Required |
| `parameterSchema` | JSON Schema for input validation. | Required |
| `isOutputMarkdown` | Should the result be rendered as Markdown? | Optional (Default: `true`) |
| `canUpdateOutput` | Does the tool support streaming updates? | Optional (Default: `false`) |

**Key Method to Implement:**
- `createInvocation(params)`: Returns a new instance of your `ToolInvocation` class.

### Step 2: The Execution Logic (`ToolInvocation`)
Extend `BaseToolInvocation<TParams, TResult>`.

| Method | Role | Requirement |
| :--- | :--- | :--- |
| `getDescription()` | Returns a markdown summary of the specific action (e.g., "Read file `/etc/passwd`"). Used in confirmation dialogs. | Required |
| `execute()` | The actual implementation of the tool's logic. | Required |
| `getDefaultPermission()` | Returns `'allow'`, `'ask'`, or `'deny'`. | Optional (Default: `'allow'`) |
| `getConfirmationDetails()` | Defines the UI for the confirmation dialog (e.g., showing a diff). | Optional |
| `toolLocations()` | Returns a list of files affected by this call. | Optional |

---

## 3. Schema Definition

The `parameterSchema` must be a valid JSON Schema object. This is the only way the LLM knows how to call your tool.

**Best Practices for Tool Schemas:**
- **Be Explicit**: Use `description` fields for every property to guide the LLM.
- **Constrain Inputs**: Use `enum` for fields with a fixed set of valid values.
- **Require Essentials**: Use the `required` array to ensure the LLM provides critical arguments.

**Example Schema:**
```typescript
const schema = {
  type: 'object',
  properties: {
    path: { 
      type: 'string', 
      description: 'The absolute path to the target file.' 
    },
    lines: { 
      type: 'number', 
      description: 'Number of lines to read.' 
    }
  },
  required: ['path']
};
```

---

## 4. Permissions & Safety

Safety is integrated into the tool's identity via the `Kind` enum and the `PermissionManager`.

### Tool Kinds
Assign a `Kind` to your tool to define its baseline impact:
- `Kind.Read` / `Kind.Search` / `Kind.Fetch`: Inherently safe.
- `Kind.Edit` / `Kind.Delete` / `Kind.Move` / `Kind.Execute`: Mutators that typically require confirmation.
- `Kind.Think`: Internal cognitive tools.

### The Permission Flow
1. **Intrinsic Permission**: `ToolInvocation.getDefaultPermission()` provides the tool's own view of its safety.
2. **Global Override**: The `PermissionManager` evaluates the call against user settings and project rules.
3. **Final Decision**: If the result is `'ask'`, the `getConfirmationDetails()` method is called to render the UI.

---

## 5. Registration

Tools must be registered in the `ToolRegistry` to be discovered by the model.

### Eager Registration
Used for core tools that are always available.
```typescript
registry.registerTool(new MyCustomTool());
```

### Lazy Registration (Factories)
Used to reduce startup time and memory usage. The tool is only instantiated on first use.
```typescript
registry.registerFactory('my-tool', async () => new MyCustomTool());
```

---

## 6. Minimal Working Example

Here is a complete implementation of a simple `GreetingTool`.

```typescript
import { BaseDeclarativeTool, BaseToolInvocation, Kind, ToolResult } from './tools.js';

interface GreetingParams {
  name: string;
}

class GreetingInvocation extends BaseToolInvocation<GreetingParams, ToolResult> {
  getDescription() {
    return `Send a friendly greeting to ${this.params.name}.`;
  }

  async execute() {
    return {
      llmContent: `Hello, ${this.params.name}! I am Qwen Code.`,
      returnDisplay: `**Greeting sent to ${this.params.name}**`,
    };
  }
}

export class GreetingTool extends BaseDeclarativeTool<GreetingParams, ToolResult> {
  constructor() {
    super(
      'greet',
      'Greeting Tool',
      'Sends a friendly greeting to a specified person.',
      Kind.Other,
      {
        type: 'object',
        properties: {
          name: { type: 'string', description: 'The name of the person to greet.' }
        },
        required: ['name']
      }
    );
  }

  protected createInvocation(params: GreetingParams) {
    return new GreetingInvocation(params);
  }
}
```

---

## 7. Verification Checklist

- [ ] **Schema Accuracy**: Does the `parameterSchema` accurately reflect the `TParams` interface?
- [ ] **Description Clarity**: Is the tool's description clear enough for the LLM to know when to use it?
- [ ] **Permission Alignment**: Does the `Kind` match the actual side-effects of the `execute()` method?
- [ ] **Confirmation UI**: If the tool is a mutator, does `getDescription()` provide enough context for a user to safely approve the action?
- [ ] **Return Format**: Does `execute()` return both `llmContent` (factual) and `returnDisplay` (user-friendly)?
