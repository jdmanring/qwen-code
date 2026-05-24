# Provider Network & OmniRoute Strategy

## The Resilient Agent Network

The AI-OS does not rely on a single LLM provider. Instead, it treats all integrated providers as members of a **Resilient Agent Network**. This network is designed to provide continuous, high-availability, and high-performance intelligence through automated redundancy and intelligent routing.

By decoupling the **Intent** (what we want to do) from the **Inference** (which model does it), we ensure that the system remains operational even during provider outages, rate-limiting events, or capacity fluctuations.

---

## Redundancy Tiers

To optimize the trade-off between reasoning capability, latency, and cost, providers and models are categorized into three distinct tiers:

| Tier | Classification | Description | Typical Use Case |
| :--- | :--- | :--- | :--- |
| **Tier 1** | **Primary / High-Reasoning** | The gold standard. Highest reasoning, largest context, and most reliable performance. | Complex architectural design, deep debugging, large-scale refactoring, and critical decision-making. |
| **Tier 2** | **Fallback / Mid-Range** | Fast, reliable, and cost-effective. Excellent for standard tasks with high availability. | Routine code generation, unit test writing, documentation, and general-purpose assistance. |
| **Tier 3** | **Utility / Edge Cases** | Specialized, lightweight, or extremely low-cost models. | Simple formatting, text extraction, lightweight orchestration, and experimental/sandbox tasks. |

---

## OmniRoute Orchestration

**OmniRoute** is the central intelligence engine that manages this network. It serves as the **Routing Plane** of the AI-OS, performing the following critical functions:

1.  **Dynamic Model Selection**: Based on the `Job`'s `policy` and `intent`, OmniRoute selects the optimal model from the appropriate tier.
2.  **Automated Fallback Chains**: If a Tier 1 provider fails (e.g., `429 Too Many Requests` or `500 Internal Server Error`), OmniRoute automatically detects the failure and reroutes the task to a pre-configured Tier 2 fallback model.
3.  **Load & Latency Balancing**: OmniRoute monitors provider health and response times to dynamically shift traffic away from degraded endpoints.
4.  **Secret Management**: OmniRoute acts as the secure gateway for all API credentials, ensuring that sensitive keys are never exposed to the Control or Execution planes.

---

## Integration with Provider Files

Each file in the `docs/providers/` directory provides detailed metadata and configuration for a specific provider.

**To optimize AI consumption, each provider file follows a standardized structure:**
1.  **Network Metadata Header**: A machine-readable summary of the provider's role in the network.
2.  **Resource Links**: URLs for official documentation, dashboards, and API endpoints.
3.  **Capabilities & Constraints**: Analysis of the provider's strengths, weaknesses, and best use cases.
4.  **Capabilities & Tooling**: A dedicated section for non-inference capabilities, such as:
    - **Embeddings**: Models and configurations for vectorization.
    - **Fine-tuning**: Options for training custom weights.
    - **Specialized Tooling**: Access to unique features like real-time web search, vision APIs, or code interpreters.
5.  **Model Configuration Data**: A detailed JSON-structured list of specific models available through the provider, including their unique capabilities and `generationConfig`.
