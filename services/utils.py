import os
from string import Template

def load_prompt(prompt_name: str) -> str:
    base_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
    file_path = os.path.join(base_dir, f"{prompt_name}.txt")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Prompt not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def format_prompt(template: str, **kwargs) -> str:
    """
    Safe prompt formatter using string.Template.
    - Supports $placeholder syntax
    - Ignores {json braces} completely
    - Impossible to raise KeyError or ValueError
    """
    t = Template(template)
    safe_kwargs = {k: (v if v is not None else "") for k, v in kwargs.items()}
    return t.safe_substitute(safe_kwargs)
