 
#  User Guide: Creating Elite Agents

This guide explains how to design and deploy specialized agents using the Mega Code **Elite Agent Blueprint**. By following this process, you ensure your agents are not just "prompts," but cognitive modules integrated with the project's semantic memory and skill library.

---

## 1. The Agent Creation Workflow

To create a new agent, follow this four-step lifecycle:

**Define $\rightarrow$ Configure $\rightarrow$ Validate $\rightarrow$ Optimize**

### Step 1: Define the Cognitive Boundary
Before writing a prompt, answer these three questions:
1. **Persona**: What is the agent's authority? (e.g., "Adversarial Security Auditor").
2. **Knowledge**: What does it need to know? (e.g., "OWASP Top 10", "Project API Specs").
3. **Success**: What does a "Perfect Response" look like? (e.g., "A list of vulnerabilities with PoC and Fixes").

### Step 2: Configure using the Template
Copy the `config/agents/template.md` and fill in the sections. 

**Critical Focus Areas:**
- **Memory Access Profile**: Don't just say "use memory." Specify: *"Use `reflect` to understand the project architecture, then `search` for specific implementation details in the local tier."*
- **Tool-Chains**: Define the exact sequence of tools. Instead of "Search the code," use: `Glob` $\rightarrow$ `Grep` $\rightarrow$ `ReadFile`.
- **Guardrails**: Add "Hard Constraints" to prevent hallucinations (e.g., *"Never suggest a library that is not already in package.json"*).

### Step 3: Validate the Loop
Test your agent by ensuring it follows the **Cognitive Interaction Loop**:
1. **Recall**: Does it start by searching semantic memory?
2. **Analyze**: Does it synthesize the memory before acting?
3. **Act**: Does it use the correct tool-chain?
4. **Ingest**: Does it store new architectural decisions back into the Cloud tier?

### Step 4: Optimize via the System Optimizer
If the agent fails a task, do not just "tweak the prompt." Use the `system_optimizer` skill to analyze the failure and update the agent's **Guardrails** or **Tool-Chains**.

---

## 2. Advanced Techniques

### Leveraging the Skill Bridge
Your agent can delegate complex tasks to specialized skills using the `call_skill` tool.

**Example**: Instead of having a `Developer` agent try to map the entire codebase, instruct it to:
`call_skill(skill_name="codebase-mapper", arguments={"target": "auth-module"})`

This allows you to build "Manager Agents" who orchestrate "Specialist Skills."

### Optimizing Memory Interaction
To maximize RAG performance, instruct your agent to:
- **Anchor to Cloud**: Use the Cloud tier for "Laws" and "Policies."
- **Ground in Local**: Use the Local tier for "Implementation Facts."
- **Prune Noise**: Remind the agent to only `ingest` high-value technical decisions, not conversational updates.

---

## 3. Deployment Checklist

Before adding your agent to `config/agents_library/`, verify the following:
- [ ] Does it have a clear **Persona** and **Authority**?
- [ ] Is the **Memory Access Profile** explicitly defined?
- [ ] Are there at least two **Tool-Chain Recipes**?
- [ ] Are there **Hard Constraints** to prevent common failures?
- [ ] Does it follow the **Output Standard** for reporting?
