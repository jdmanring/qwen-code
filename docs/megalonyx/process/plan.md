# Project Implementation Plan: Agentic Stack

This document tracks the phased rollout of the specialized agent roster and the RAG infrastructure.

## Phase 1: The Core Loop (Essential Workers)
*Goal: Establish a stable, zero-waste foundation for basic coding tasks.*

- [ ] **Implement `Scout`**: Create `.qwen/agents/scout.md` with Llama 4 Scout and Local RAG focus.
- [ ] **Implement `Developer`**: Create `.qwen/agents/developer.md` with Codestral and Implementation-First Bias.
- [ ] **Implement `Researcher`**: Create `.qwen/agents/researcher.md` with Gemini 2.5 Flash and Remote RAG focus.
- [ ] **Verify Core Loop**: Test the flow: Primary $\rightarrow$ Scout $\rightarrow$ Researcher $\rightarrow$ Developer.

## Phase 2: The Quality Gate (Professionalism Layer)
*Goal: Introduce adversarial review and strategic planning to eliminate bugs.*

- [ ] **Implement `Architect`**: Create `.qwen/agents/architect.md` with Qwen3-480B for strategic design.
- [ ] **Implement `Reviewer`**: Create `.qwen/agents/reviewer.md` with GPT-OSS-120B for adversarial audit.
- [ ] **Implement `QA Lead`**: Create `.qwen/agents/qa-lead.md` with GPT-OSS-120B for final certification.
- [ ] **Verify Quality Gate**: Test the flow: Architect $\rightarrow$ Developer $\rightarrow$ Reviewer $\rightarrow$ QA Lead.

## Phase 3: The Elite Layer (Hardening & Meta)
*Goal: Maximize security and optimize the system's own behavior.*

- [ ] **Implement `Security Auditor`**: Create `.qwen/agents/security-auditor.md` with Qwen3-480B.
- [ ] **Implement `System Optimizer`**: Create `.qwen/agents/system-optimizer.md` with Qwen3-480B.
- [ ] **Implement `Doc Expert`**: Create `.qwen/agents/doc-expert.md` with Qwen3-32B.
- [ ] **Final Audit**: Verify all 12 agents are loaded and adhering to the Zero-Waste Workflow.

## Phase 4: RAG Infrastructure Hardening
- [ ] **Tavily Integration**: Complete Phase 2 of `docs/RAG_STACK.md`.
- [ ] **Code-Index Integration**: Complete Phase 4 of `docs/RAG_STACK.md`.
- [ ] **Symmetry Verification**: Ensure all agents follow the "Search $\rightarrow$ Fetch $\rightarrow$ Synthesize" rule.

## Phase 5: Bleeding Edge Research (Experimental)
*Goal: Move from highly capable tools to autonomous, structural intelligence.*

- [ ] **Implement GraphRAG**: Integrate Knowledge Graph mapping for structural code understanding.
- [ ] **Implement CRAG (Self-Correcting RAG)**: Build the agentic feedback loop for retrieval verification.
- [ ] **Implement Multi-Agent Swarms**: Transition from a single orchestrator to a decentralized agent ecosystem.
- [ ] **Implement Multimodal Memory**: Integrate visual (screenshot) and audio indexing into the semantic memory.
- [ ] **Review Roadmap**: Periodically reassess the research directions in `docs/research/roadmap.md`.
