import os
import shutil

import yaml

SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config", "skills"))


def transform_skills() -> None:
    # Get all yaml files
    yaml_files = [f for f in os.listdir(SKILLS_DIR) if f.endswith(".yaml")]

    if not yaml_files:
        print("No YAML files found in config/skills/")
        return
    for yaml_file in yaml_files:
        skill_name = yaml_file.replace(".yaml", "")
        skill_dir = os.path.join(SKILLS_DIR, skill_name)

        # Create skill directory
        os.makedirs(skill_dir, exist_ok=True)

        # Read YAML
        with open(os.path.join(SKILLS_DIR, yaml_file)) as f:
            data = yaml.safe_load(f)

        # Generate SKILL.md
        with open(os.path.join(skill_dir, "SKILL.md"), "w") as f:
            f.write(f"# Skill: {data.get('name', skill_name)}\n\n")
            f.write(f"**Description**: {data.get('description', 'No description provided.')}\n\n")
            f.write(f"**Type**: {data.get('type', 'sub-agent')}\n\n")
            f.write(f"**Model**: `{data.get('model', 'N/A')}`\n\n")

            f.write("### Tools\n")
            for tool in data.get("tools", []):
                f.write(f"- {tool}\n")
            f.write("\n")

            if "triggers" in data and "keywords" in data["triggers"]:
                f.write("### Triggers\n")
                for kw in data["triggers"]["keywords"]:
                    f.write(f"- `{kw}`\n")
                f.write("\n")

            if "system_prompt" in data:
                f.write("### System Prompt\n")
                f.write("```text\n")
                f.write(data["system_prompt"].strip())
                f.write("\n```\n")

        # Move original yaml into the directory
        shutil.move(os.path.join(SKILLS_DIR, yaml_file), os.path.join(skill_dir, yaml_file))
        print(f"Transformed: {yaml_file} -> {skill_name}/")


if __name__ == "__main__":
    transform_skills()
