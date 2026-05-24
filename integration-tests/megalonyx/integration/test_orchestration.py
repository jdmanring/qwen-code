import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.qwen/skills"))
)

import pytest
from config.system.skill_selector import SkillOrchestrator

# Mocking the skills directory for testing
TEST_SKILLS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "mock_skills")
)


@pytest.fixture(scope="module", autouse=True)
def setup_mock_skills():
    os.makedirs(TEST_SKILLS_DIR, exist_ok=True)

    # 1. Valid skill with keywords and extensions
    with open(f"{TEST_SKILLS_DIR}/dev.yaml", "w") as f:
        f.write(
            "---\nname: developer\ntriggers:\n  keywords: [implement]\n  file_extensions: [.py]"
        )

    # 2. Valid skill with only extensions (like the old Scout)
    with open(f"{TEST_SKILLS_DIR}/scout.yaml", "w") as f:
        f.write("---\nname: scout\ntriggers:\n  file_extensions: [.py]")

    # 3. Invalid YAML file (trailing dashes)
    with open(f"{TEST_SKILLS_DIR}/broken.yaml", "w") as f:
        f.write("---\nname: broken\ntriggers: {}\n---\n---")

    yield
    # Cleanup would go here in a real scenario


def test_skill_loading():
    orch = SkillOrchestrator(skills_dir=TEST_SKILLS_DIR)
    # Should load dev and scout. Broken should be skipped (currently suppressed)
    assert "developer" in orch.skills
    assert "scout" in orch.skills
    assert "broken" not in orch.skills


def test_keyword_priority():
    orch = SkillOrchestrator(skills_dir=TEST_SKILLS_DIR)
    # Prompt "implement" should trigger developer, even if file is .py (which also triggers scout)
    active = orch.get_active_skills(
        current_file_path="test.py", prompt_text="implement this"
    )
    assert active[0]["name"] == "developer"


def test_fallback_to_extension():
    orch = SkillOrchestrator(skills_dir=TEST_SKILLS_DIR)
    # No keyword, just .py file -> should trigger scout (or developer, depending on load order)
    active = orch.get_active_skills(current_file_path="test.py", prompt_text="hello")
    assert len(active) > 0
    assert any(s["name"] in ["developer", "scout"] for s in active)


def test_no_trigger():
    orch = SkillOrchestrator(skills_dir=TEST_SKILLS_DIR)
    # Set phase to something that doesn't boost any of the mock agents
    orch.state_manager.set("active_phase", "NONE")
    active = orch.get_active_skills(current_file_path="test.txt", prompt_text="hello")
    assert len(active) == 0


class TestE2EScenarios:
    """
    End-to-End Scenario Tests: Verifies that real-world user prompts
    trigger the correct specialized agents.
    """

    def setup_method(self):
        # Use the actual project skills for E2E tests
        self.orch = SkillOrchestrator()

    def test_scenario_architecture_request(self):
        # Scenario: User wants a high-level design
        prompt = "I need a technical architecture for the new auth system"
        active = self.orch.get_active_skills(prompt_text=prompt)
        assert any(s["name"] == "architect" for s in active), (
            "Architecture request should trigger Architect"
        )

    def test_scenario_implementation_request(self):
        # Scenario: User wants to add a feature
        prompt = "Implement the login function in auth.py"
        active = self.orch.get_active_skills(prompt_text=prompt)
        assert any(s["name"] == "developer" for s in active), (
            "Implementation request should trigger Developer"
        )

    def test_scenario_research_request(self):
        # Scenario: User wants to research an external API
        prompt = "Research the latest Stripe API for subscription billing"
        active = self.orch.get_active_skills(prompt_text=prompt)
        assert any(s["name"] == "researcher" for s in active), (
            "Research request should trigger Researcher"
        )

    def test_scenario_failure_analysis(self):
        # Scenario: User reports a loop/crash
        prompt = "The agent is looping and repeating the same mistake"
        active = self.orch.get_active_skills(prompt_text=prompt)
        assert any(s["name"] == "system_optimizer" for s in active), (
            "Failure report should trigger System Optimizer"
        )

    def test_scenario_doc_request(self):
        # Scenario: User wants documentation
        prompt = "Can you write a readme for this project?"
        active = self.orch.get_active_skills(prompt_text=prompt)
        assert any(s["name"] == "doc_expert" for s in active), (
            "Doc request should trigger Doc Expert"
        )
