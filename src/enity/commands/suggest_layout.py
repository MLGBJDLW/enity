import typer
from pathlib import Path
from enity.core.config import load_config
from enity.core.grouper import group_variables_by_keyword
from enity.core.io import read_text as read_env_file


def suggest_layout(env_file: str = "./.env.example"):
    """
    Suggest layout command:
    - Read and parse the given .env file (default: ./.env.example).
    - Apply custom grouping rules from .enity.toml.
    - Group remaining variables using the smart grouper.
    - Print suggested layout to stdout.
    """
    # Read env file
    try:
        content = read_env_file(Path(env_file))
    except Exception as e:
        print(f"Error: Failed to read env file '{env_file}': {e}")
        raise typer.Exit(code=1)

    # Extract variable names (ignore comments / blank lines)
    variables = []
    for raw in content.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key = line.split("=", 1)[0].strip()
        if key:
            variables.append(key)

    # Load custom rules
    cfg = load_config()
    rules = cfg.grouping_rules or {}

    final_groups = {}
    assigned_variables = set()

    # First pass: apply custom rules (prefixes and keywords)
    for rule in rules.values():
        name = rule.name
        prefixes = [p.upper() for p in (rule.prefixes or [])]
        keywords = [k.upper() for k in (rule.keywords or [])]
        matches = []
        for var in variables:
            if var in assigned_variables:
                continue
            u = var.upper()
            matched = False
            if prefixes and any(u.startswith(pref) for pref in prefixes):
                matched = True
            if not matched and keywords and any(kw in u for kw in keywords):
                matched = True
            if matched:
                matches.append(var)
        if matches:
            final_groups.setdefault(name, []).extend(sorted(matches))
            assigned_variables.update(matches)

    # Second pass: smart grouping for remaining variables
    remaining = [v for v in variables if v not in assigned_variables]
    smart_groups = group_variables_by_keyword(remaining)
    for k, vs in smart_groups.items():
        final_groups.setdefault(k, []).extend(sorted(vs))

    # Pretty-print result
    if not final_groups:
        print("No variable groups found.")
        raise typer.Exit(code=0)

    for group_name, vars_list in final_groups.items():
        print(f"# ===== {group_name} =====")
        for v in vars_list:
            print(v)
        print("")