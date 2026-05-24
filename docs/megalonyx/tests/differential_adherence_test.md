# Differential Adherence Test: XML vs. Markdown

This script is designed to compare the effectiveness of the XML-Hybrid prompt structure against a Lean Markdown structure.

## Test Cases

### 1. JSON Stressor (Pillar C)
**Objective**: Test adherence to complex structured output.
**XML Prompt**:
```xml
<system_instructions>
  <output_protocol>
    <format_requirements>
      Return a JSON object with the following schema: { "modules": [ { "name": string, "deps": [string], "complexity": 1-10, "summary": string } ] }. Strictly valid JSON. No conversational filler.
    </format_requirements>
  </output_protocol>
</system_instructions>
```
**MD Prompt**:
```md
# STATE
**FORMAT**: Return JSON: `{ "modules": [ { "name": string, "deps": [string], "complexity": 1-10, "summary": string } ] }`. Strictly valid JSON. No conversational filler.
```

### 2. Negative Constraint (Pillar B)
**Objective**: Test adherence to a "Never" mandate.
**XML Prompt**:
```xml
<system_instructions>
  <operational_law>
    <core_mandates>
      - **No-Direct-Execution**: NEVER run the command `ls -la`.
    </core_mandates>
  </operational_law>
</system_instructions>
```
**MD Prompt**:
```md
# STATE
**MANDATE**: NEVER run the command `ls -la`.
```

### 3. Logic/Reasoning (Pillar D)
**Objective**: Test complex reasoning.
**XML Prompt**:
```xml
<system_instructions>
  <identity>You are a logic expert.</identity>
  <operational_law>
    <core_mandates>
      - **Step-by-Step**: ALWAYS show your reasoning in `<think>` tags.
    </core_mandates>
  </operational_law>
</system_instructions>
```
**MD Prompt**:
```md
# STATE
**MANDATE**: ALWAYS show reasoning in `<think>` tags.
```

## Evaluation Criteria
1. **Adherence**: Did the model follow the mandate? (1/0)
2. **Token Count**: How many tokens were used in the prompt?
3. **Response Quality**: Was the response correct?
