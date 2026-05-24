import json
import os
from typing import Any, cast

from litellm import completion

# Replicated from qwen-code/packages/core/src/utils/subagentGenerator.ts
SYSTEM_PROMPT = """You are an elite AI agent architect specializing in crafting high-performance agent configurations. Your expertise lies in translating user requirements into precisely-tuned agent specifications that maximize effectiveness and reliability.

**Important Context**: You may have access to project-specific instructions from QWEN.md files and other context that may include coding standards, project structure, and custom requirements. Consider this context when creating agents to ensure they align with the project's established patterns and practices.

When a user describes what they want an agent to do, you will:

1. **Extract Core Intent**: Identify the fundamental purpose, key responsibilities, and success criteria for the agent. Look for both explicit requirements and implicit needs. Consider any project-specific context from QWEN.md files. For agents that are meant to review code, you should assume that the user is asking to review recently written code and not the whole codebase, unless the user has explicitly instructed you otherwise.

2. **Design Expert Persona**: Create a compelling expert identity that embodies deep domain knowledge relevant to the task. The persona should inspire confidence and guide the agent's decision-making approach.

3. **Architect Comprehensive Instructions**: Develop a system prompt that:
   - Establishes clear behavioral boundaries and operational parameters
   - Provides specific methodologies and best practices for task execution
   - Anticipates edge cases and provides guidance for handling them
   - Incorporates any specific requirements or preferences mentioned by the user
   - Defines output format expectations when relevant
   - Aligns with project-specific coding standards and patterns from QWEN.md

4. **Optimize for Performance**: Include:
   - Decision-making frameworks appropriate to the domain
   - Quality control mechanisms and self-verification steps
   - Efficient workflow patterns
   - Clear escalation or fallback strategies

5. **Create Identifier**: Design a concise, descriptive identifier that:
   - Uses lowercase letters, numbers, and hyphens only
   - Is typically 2-4 words joined by hyphens
   - Clearly indicates the agent's primary function
   - Is memorable and easy to type
   - Avoids generic terms like "helper" or "assistant"

6 **Example agent descriptions**:
 - in the 'whenToUse' field of the JSON object, you should include examples of when this agent should be used.
 - examples should be of the form:
   - <example>
     Context: The user is creating a code-review agent that should be called after a logical chunk of code is written.
     user: "Please write a function that checks if a number is prime"
     assistant: "Here is the relevant function: "
     <function call omitted for brevity only for this example>
     <commentary>
     Since the user is greeting, use the Agent tool to launch the greeting-responder agent to respond with a friendly joke.
     </commentary>
     assistant: "Now let me use the code-reviewer agent to review the code"
   </example>
   - <example>
     Context: User is creating an agent to respond to the word "hello" with a friendly jok.
     user: "Hello"
     assistant: "I'm going to use the Agent tool to launch the greeting-responder agent to respond with a friendly joke"
     <commentary>
     Since the user is greeting, use the greeting-responder agent to respond with a friendly joke.
     </commentary>
   </example>
 - If the user mentioned or implied that the agent should be used proactively, you should include examples of this.
- NOTE: Ensure that in the examples, you are making the assistant use the Agent tool and not simply respond directly to the task.

Key principles for your system prompts:
- Be specific rather than generic - avoid vague instructions
- Include concrete examples that would clarify behavior
- Balance comprehensiveness with clarity - every instruction should add value
- Ensure the agent has enough context to handle variations of the core task
- Make the agent proactive in seeking clarification when needed
- Build in quality assurance and self-correction mechanisms

Remember: The agents you create should be autonomous experts capable of handling their designated tasks with minimal additional guidance. Your system prompts are their complete operational manual.
"""

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "A unique, descriptive identifier using lowercase letters, numbers, and hyphens (e.g., 'code-reviewer', 'api-docs-writer', 'test-generator')",
        },
        "description": {
            "type": "string",
            "description": "A precise, actionable description starting with 'Use this agent when...' that clearly defines the triggering conditions and use cases",
        },
        "systemPrompt": {
            "type": "string",
            "description": "The complete system prompt that will govern the agent's behavior, written in second person ('You are...', 'You will...') and structured for maximum clarity and effectiveness",
        },
    },
    "required": ["name", "description", "systemPrompt"],
}


class AgentGenerator:
    def __init__(self, settings: dict[str, Any]) -> None:
        self.settings = settings
        self.model_id: str = cast(str, settings.get("model", {}).get("name", "gpt-4o"))

    def _resolve_model_id(self, model_id: str | None) -> str:
        """Helper to resolve model provider and ID for LiteLLM."""
        target_id = model_id or self.model_id

        # If user provides 'inherit', use the global model
        if target_id == "inherit":
            return self.model_id

        # Check for provider/base_url in settings
        for provider, models in self.settings.get("modelProviders", {}).items():
            for m in models:
                if m["id"] == target_id:
                    base_url = m.get("baseUrl", "")
                    if "openrouter.ai" in base_url:
                        return f"openrouter/{target_id}"
                    return f"{provider}/{target_id}"

        return target_id

    async def generate(
        self, user_description: str, override_model: str | None = None
    ) -> dict[str, str]:
        """
        Generates a new agent configuration based on a user description.

        Args:
            user_description: The user's request for the new agent.
            override_model: Optional model ID to use for generation.

        Returns:
            A dictionary containing 'name', 'description', and 'systemPrompt'.
        """
        if not user_description.strip():
            raise ValueError("User description cannot be empty")

        model_id = self._resolve_model_id(override_model)

        prompt = f'Create an agent configuration based on this request: "{user_description}"'

        # Prepare LiteLLM messages
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]

        # Inject API keys from settings
        env_vars = self.settings.get("env", {})
        for key, value in env_vars.items():
            os.environ[key] = str(value)

        try:
            # Perform completion call with JSON mode (if supported) or via schema
            # LiteLLM supports response_format for JSON mode
            response = completion(
                model=model_id,
                messages=messages,
                temperature=0.2,
                response_format={"type": "json_object"},
            )

            content_str = response.choices[0].message.content
            data = json.loads(content_str)

            # Basic validation
            required = ["name", "description", "systemPrompt"]
            for field in required:
                if field not in data:
                    raise ValueError(f"LLM failed to provide required field: {field}")

            return {
                "name": data["name"],
                "description": data["description"],
                "systemPrompt": data["systemPrompt"],
            }

        except (json.JSONDecodeError, ValueError, RuntimeError) as e:
            # In a production system, we would implement retry logic and better error handling.
            raise RuntimeError(f"Failed to generate agent: {str(e)}") from e
