from pathlib import Path
from typer.testing import CliRunner
from enity.main import app


def test_suggest_layout_only_smart_grouping(tmp_path, monkeypatch):
    # Arrange: create .env.example with variables for smart grouping
    content = "\n".join(
        [
            "DATABASE_URL=postgres://",
            "DATABASE_USER=admin",
            "REDIS_HOST=localhost",
            "REDIS_PORT=6379",
            "API_KEY=secret",
        ]
    )
    p = tmp_path
    (p / ".env.example").write_text(content, encoding="utf-8")
    # Ensure config loader looks at tmp_path for .enity.toml
    monkeypatch.chdir(p)

    runner = CliRunner()
    # Act
    result = runner.invoke(app, ["suggest-layout"])

    # Assert
    assert result.exit_code == 0
    out = result.output
    assert "# ===== DATABASE =====" in out
    assert "DATABASE_URL" in out and "DATABASE_USER" in out
    assert "# ===== REDIS =====" in out
    assert "REDIS_HOST" in out and "REDIS_PORT" in out
    # API_KEY is stop-word based and should go to Miscellaneous
    assert "# ===== Miscellaneous =====" in out
    assert "API_KEY" in out


def test_suggest_layout_with_custom_rules(tmp_path, monkeypatch):
    # Arrange: create .env.example and .enity.toml with a custom rule
    content = "\n".join(
        [
            "DB_URL=postgres://",
            "DB_USER=admin",
            "OTHER=val",
        ]
    )
    p = tmp_path
    (p / ".env.example").write_text(content, encoding="utf-8")
    toml = """
[grouping_rules.db]
name = "DatabaseCustom"
prefixes = ["DB_"]
keywords = []
"""
    (p / ".enity.toml").write_text(toml.lstrip(), encoding="utf-8")
    monkeypatch.chdir(p)

    runner = CliRunner()
    # Act
    result = runner.invoke(app, ["suggest-layout"])

    # Assert
    assert result.exit_code == 0
    out = result.output
    # Custom group name must appear and include DB_* variables
    assert "# ===== DatabaseCustom =====" in out
    assert "DB_URL" in out and "DB_USER" in out
    # OTHER should still be grouped (likely Miscellaneous)
    assert "OTHER" in out


def test_suggest_layout_mixed_custom_and_smart(tmp_path, monkeypatch):
    # Arrange: custom rule covers only one variable; others grouped by smart grouper
    content = "\n".join(
        [
            "DB_URL=postgres://",
            "DATABASE_USER=admin",
            "DATABASE_PORT=5432",
            "REDIS_HOST=localhost",
        ]
    )
    p = tmp_path
    (p / ".env.example").write_text(content, encoding="utf-8")
    toml = """
[grouping_rules.custom]
name = "DBPrefix"
prefixes = ["DB_"]
keywords = []
"""
    (p / ".enity.toml").write_text(toml.lstrip(), encoding="utf-8")
    monkeypatch.chdir(p)

    runner = CliRunner()
    # Act
    result = runner.invoke(app, ["suggest-layout"])

    # Assert
    assert result.exit_code == 0
    out = result.output
    # DB_URL should be in custom group
    assert "# ===== DBPrefix =====" in out
    assert "DB_URL" in out
    # Remaining DATABASE_* should be grouped by smart grouper under DATABASE
    assert "# ===== DATABASE =====" in out
    assert "DATABASE_USER" in out and "DATABASE_PORT" in out
    # REDIS group should also exist
    assert "# ===== REDIS =====" in out
    assert "REDIS_HOST" in out


def test_suggest_layout_file_missing_exits_nonzero(tmp_path, monkeypatch):
    # Arrange: no files created, switch to empty tmp_path
    monkeypatch.chdir(tmp_path)

    runner = CliRunner()
    # Act
    result = runner.invoke(app, ["suggest-layout"])

    # Assert: read should fail and command should exit with non-zero and show error message
    assert result.exit_code != 0
    assert "Error: Failed to read env file" in result.output