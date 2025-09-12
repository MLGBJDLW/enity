<details open>
<summary>English</summary>

# enity (ENV Guardian)

A command-line tool for managing `.env` environment configuration files. It helps developers check, synchronize, and organize `.env` files against a `.env.example` template.

---

### What is this?

`enity` (also known as "ENV Guardian") is a CLI tool designed to maintain consistency between your local `.env` file and the `.env.example` template file in your project. It provides three main commands: `check`, `sync`, and `tidy`.

-   **`check`**: Verifies if `.env` is missing any keys from `.env.example` or contains extra keys that are not in the template.
-   **`sync`**: Adds missing keys from `.env.example` to your `.env` file, prompting for values or filling them with empty strings.
-   **`tidy`**: Reorganizes your `.env` file to match the key order and structure of `.env.example`, and can also remove keys that are not present in the template.

The tool supports configuration via the `[tool.enity]` section in your `pyproject.toml` file, allowing you to specify custom paths for your `.env` and `.env.example` files.

### Installation

You can install `enity` using pip:

```bash
pip install enity
```

### Usage

`enity` is run from the command line. Here are the available commands and their options.

#### `enity check`

Checks for discrepancies between the `.env` and `.env.example` files.

```bash
enity check [OPTIONS]
```

**Options**:

-   `--env-path TEXT`: Path to the `.env` file. (Default: `.env`)
-   `--example-path TEXT`: Path to the `.env.example` file. (Default: `.env.example`)
-   `--only [all|missing|extra]`: Check only for 'missing' keys, 'extra' keys, or 'all'. (Default: `all`)
-   `--strict-extra / --no-strict-extra`: Treat extra keys as errors (exit with a non-zero code). (Default: `true`)
-   `--format [text|json]`: Output format. (Default: `text`)

#### `enity sync`

Synchronizes the `.env` file by adding any keys that are missing from `.env.example`.

```bash
enity sync [OPTIONS]
```

**Options**:

-   `--env-path TEXT`: Path to the `.env` file. (Default: `.env`)
-   `--example-path TEXT`: Path to the `.env.example` file. (Default: `.env.example`)
-   `--assume-empty`: Do not prompt for values; fill all missing keys with empty strings.
-   `--dry-run`: Show what changes would be made without actually modifying the `.env` file.
-   `--backup / --no-backup`: Create a backup of the `.env` file before making changes. (Default: `true`)
-   `--format [text|json]`: Output format. (Default: `text`)

#### `enity tidy`

Tidies the `.env` file by sorting keys to match the order in `.env.example` and removing duplicates.

```bash
enity tidy [OPTIONS]
```

**Options**:

-   `--env-path TEXT`: Path to the `.env` file. (Default: `.env`)
-   `--example-path TEXT`: Path to the `.env.example` file. (Default: `.env.example`)
-   `--remove-ghosts / --no-remove-ghosts`: Remove keys from `.env` that are not present in `.env.example`. (Default: `true`)
-   `--append-ghosts-at-end`: If not removing ghosts, append them at the end of the file with a `# ghost` comment.
-   `--check`: Check-only mode. Exits with code 2 if any changes would be made, but does not write them.
-   `--dry-run`: Show a diff of the changes without modifying the `.env` file.
-   `--backup / --no-backup`: Create a timestamped backup before writing changes. (Default: `true`)
-   `--format [text|json]`: Output format. (Default: `text`)

### Configuration

You can configure the default paths for the `.env` and `.env.example` files in your `pyproject.toml` file. This is useful if your project stores environment files in a non-standard location.

Add a `[tool.enity]` section to your `pyproject.toml`:

```toml
# pyproject.toml

[tool.enity]
# Path to the .env file (string)
env_path = ".env"
# Path to the .env.example file (string)
example_path = ".env.example"
```

</details>

<details>
<summary>中文</summary>

### 这是什么？

`enity` (又名 "ENV Guardian") 是一个命令行工具，旨在帮助开发者管理 `.env` 环境配置文件，确保本地的 `.env` 文件与项目中的 `.env.example` 模板文件保持一致。它提供三个核心命令：`check`、`sync` 和 `tidy`。

-   **`check`**: 检查 `.env` 文件是否缺少 `.env.example` 中的某些键，或者是否包含了模板中不存在的额外键。
-   **`sync`**: 将 `.env.example` 中缺失的键同步添加到 `.env` 文件中，并允许用户输入键值或自动填充为空值。
-   **`tidy`**: 根据 `.env.example` 的键顺序和结构来整理 `.env` 文件，并可以选择性地移除模板中不存在的键。

该工具支持通过 `pyproject.toml` 文件中的 `[tool.enity]` 配置段来自定义 `.env` 和 `.env.example` 文件的路径。

### 安装

你可以使用 pip 来安装 `enity`：

```bash
pip install enity
```

### 使用方法

`enity` 通过命令行运行。以下是可用的命令及其选项。

#### `enity check`

检查 `.env` 和 `.env.example` 文件之间的差异。

```bash
enity check [OPTIONS]
```

**选项**:

-   `--env-path TEXT`: `.env` 文件的路径。(默认: `.env`)
-   `--example-path TEXT`: `.env.example` 文件的路径。(默认: `.env.example`)
-   `--only [all|missing|extra]`: 检查范围，可以是 'missing' (仅缺失), 'extra' (仅多余), 或 'all' (全部)。(默认: `all`)
-   `--strict-extra / --no-strict-extra`: 将多余的键视为错误（以非零状态码退出）。(默认: `true`)
-   `--format [text|json]`: 输出格式。(默认: `text`)

#### `enity sync`

通过从 `.env.example` 添加缺失的键来同步 `.env` 文件。

```bash
enity sync [OPTIONS]
```

**选项**:

-   `--env-path TEXT`: `.env` 文件的路径。(默认: `.env`)
-   `--example-path TEXT`: `.env.example` 文件的路径。(默认: `.env.example`)
-   `--assume-empty`: 不提示输入值，自动将所有缺失的键填充为空字符串。
-   `--dry-run`: 显示将要进行的更改，但不会实际修改 `.env` 文件。
-   `--backup / --no-backup`: 在修改前创建 `.env` 文件的备份。(默认: `true`)
-   `--format [text|json]`: 输出格式。(默认: `text`)

#### `enity tidy`

通过对键进行排序和删除重复项来整理 `.env` 文件。

```bash
enity tidy [OPTIONS]
```

**选项**:

-   `--env-path TEXT`: `.env` 文件的路径。(默认: `.env`)
-   `--example-path TEXT`: `.env.example` 文件的路径。(默认: `.env.example`)
-   `--remove-ghosts / --no-remove-ghosts`: 从 `.env` 文件中移除在 `.env.example` 中不存在的键。(默认: `true`)
-   `--append-ghosts-at-end`: 如果不移除多余的键，则将它们附加到文件末尾，并附带 `# ghost` 注释。
-   `--check`: 仅检查模式。如果文件需要更改，则以状态码 2 退出，但不会写入更改。
-   `--dry-run`: 显示更改的差异（diff），但不会实际修改 `.env` 文件。
-   `--backup / --no-backup`: 在写入更改前创建一个带时间戳的备份。(默认: `true`)
-   `--format [text|json]`: 输出格式。(默认: `text`)

### 配置

你可以在 `pyproject.toml` 文件中配置 `.env` 和 `.env.example` 的默认路径。如果你的项目将环境文件存储在非标准位置，这个功能会非常有用。

在你的 `pyproject.toml` 文件中添加 `[tool.enity]` 配置段：

```toml
# pyproject.toml

[tool.enity]
# .env 文件的路径 (字符串)
env_path = ".env"
# .env.example 文件的路径 (字符串)
example_path = ".env.example"
```

</details>
