import pytest
from enity.core.parser import keys_set_from_text

@pytest.mark.parametrize(
    "text, expected_keys",
    [
        ("KEY1=VALUE1\nKEY2=VALUE2", {"KEY1", "KEY2"}),
        ("# Comment\nKEY1=VALUE\n\nKEY2=VALUE", {"KEY1", "KEY2"}),
        ("DUPLICATE=1\nDUPLICATE=2", {"DUPLICATE"}),
        ("", set()),
        ("\n# Only comments and blank lines\n", set()),
    ],
)
def test_keys_set_from_text(text, expected_keys):
    """
    Tests that keys are correctly parsed from a given text,
    handling comments, blank lines, and duplicates.
    """
    assert keys_set_from_text(text) == expected_keys