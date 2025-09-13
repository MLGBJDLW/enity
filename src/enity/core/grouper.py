from typing import List, Dict, Set

def group_variables_by_keyword(variables: List[str]) -> Dict[str, List[str]]:
    """
    Group environment variable names by inferred core keywords.

    Algorithm:
    - Tokenize variable names by '_' and uppercase tokens.
    - Ignore stop words.
    - A token is a core keyword if it appears in at least two different variables.
    - Assign each variable to the longest core keyword it contains (tiebreaker: alphabetical).
    - Variables with no matching core keyword go to "Miscellaneous".
    """
    if not variables:
        return {}

    stop_words = {
        "API",
        "KEY",
        "SECRET",
        "TOKEN",
        "URL",
        "PUBLIC",
        "PRIVATE",
        "ID",
        "ENV",
        "APP",
    }

    # Map token -> set of variable names that contain it
    token_to_vars: Dict[str, Set[str]] = {}
    # Map var -> set of tokens in that var
    var_to_tokens: Dict[str, Set[str]] = {}

    for var in variables:
        parts = [p for p in var.split("_") if p]
        tokens = {p.upper() for p in parts}
        var_to_tokens[var] = tokens
        for tok in tokens:
            token_to_vars.setdefault(tok, set()).add(var)

    core_keywords = [tok for tok, vars_set in token_to_vars.items() if len(vars_set) >= 2 and tok not in stop_words]

    groups: Dict[str, List[str]] = {}
    misc: List[str] = []

    for var in variables:
        tokens = var_to_tokens.get(var, set())
        matched = [tok for tok in core_keywords if tok in tokens]
        if not matched:
            misc.append(var)
            continue
        # choose longest token, tiebreaker alphabetical
        matched.sort(key=lambda t: (-len(t), t))
        chosen = matched[0]
        groups.setdefault(chosen, []).append(var)

    if misc:
        groups.setdefault("Miscellaneous", []).extend(misc)

    return groups