from typer.testing import CliRunner
from enity.main import app
import pytest

runner = CliRunner()

def test_check_command_missing_and_extra_keys(tmp_path):
    """
    Tests the 'check' command for reporting missing and extra keys.
    """
    env_content = "KEY1=VAL1\nEXTRA_KEY=VAL_EXTRA"
    example_content = "KEY1=\nMISSING_KEY="

    env_file = tmp_path / ".env"
    example_file = tmp_path / ".env.example"

    env_file.write_text(env_content)
    example_file.write_text(example_content)

    result = runner.invoke(
        app, ["check", "--env", str(env_file), "--example", str(example_file)]
    )

    assert result.exit_code == 1
    assert "Missing keys in .env: {'MISSING_KEY'}" in result.stdout
    assert "Extra keys in .env: {'EXTRA_KEY'}" in result.stdout

def test_check_command_success(tmp_path):
    """
    Tests the 'check' command for a successful sync.
    """
    env_content = "KEY1=VAL1\nKEY2=VAL2"
    example_content = "KEY1=\nKEY2="

    env_file = tmp_path / ".env"
    example_file = tmp_path / ".env.example"

    env_file.write_text(env_content)
    example_file.write_text(example_content)

    result = runner.invoke(
        app, ["check", "--env", str(env_file), "--example", str(example_file)]
    )

    assert result.exit_code == 0
    assert "OK" in result.stdout