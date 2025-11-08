import os

def load_prompt(prompt_name: str) -> str:
    """Loads a prompt file from the /prompts directory."""
    base_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
    file_path = os.path.join(base_dir, f"{prompt_name}.txt")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Prompt not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()
