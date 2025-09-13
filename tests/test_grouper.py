from enity.core.grouper import group_variables_by_keyword


def test_group_variables_by_keyword_basic():
    variables = [
        "DATABASE_URL",
        "DATABASE_USER",
        "REDIS_HOST",
        "REDIS_PORT",
        "API_KEY",
    ]
    expected = {
        "DATABASE": ["DATABASE_URL", "DATABASE_USER"],
        "REDIS": ["REDIS_HOST", "REDIS_PORT"],
        "Miscellaneous": ["API_KEY"],
    }
    assert group_variables_by_keyword(variables) == expected


def test_group_variables_by_keyword_longest_match_first():
    variables = [
        "DATABASE_URL",
        "DATABASE_POOL_SIZE",
        "REDIS_HOST",
    ]
    expected = {
        "DATABASE": ["DATABASE_URL", "DATABASE_POOL_SIZE"],
        "REDIS": ["REDIS_HOST"],
    }
    assert group_variables_by_keyword(variables) == expected


def test_group_variables_by_keyword_miscellaneous():
    variables = [
        "APP_NAME",
        "DEBUG",
        "SECRET_KEY",
    ]
    expected = {
        "Miscellaneous": ["APP_NAME", "DEBUG", "SECRET_KEY"],
    }
    assert group_variables_by_keyword(variables) == expected