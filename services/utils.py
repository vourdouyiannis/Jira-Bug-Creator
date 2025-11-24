import os
from string import Template


def load_prompt(prompt_name):
    """
    Load a prompt text file from the /prompts directory.

    @param prompt_name: str — name of the prompt file (without extension).

    @return: Full prompt text.
    @rtype: str
    @raises FileNotFoundError: If the prompt file does not exist.
    """
    base_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
    file_path = os.path.join(base_dir, f"{prompt_name}.txt")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Prompt not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def format_prompt(template, **kwargs):
    """
    Format prompt using string.Template.

    - Supports $placeholder syntax.
    - Does NOT parse Python .format() braces — prevents JSON conflict.
    - Never raises KeyError or ValueError.

    @param template: str — template text containing $placeholders.
    @param kwargs: dict — values to substitute.
    @return: Final formatted prompt.
    @rtype: str
    """
    t = Template(template)
    safe_kwargs = {k: (v if v is not None else "") for k, v in kwargs.items()}
    return t.safe_substitute(safe_kwargs)
