# enity

`enity` is a command-line tool for project maintenance and standardization.

---

## Features

-   `--version`: Display the current version number.
-   `check`: Check project configurations, such as automatically adding `.env` rules to `.gitignore`.
-   `generate`: Generate `.env.example` from an `.env` file.
-   `sync`: Synchronize variables from `.env.example` to `.env`.
-   `tidy`: Tidy up the `.env` file by sorting its keys.
-   `load`: Bulk inject configurations from a file or standard input, and automatically trigger `tidy` and `generate`.
-   `suggest-layout`: Intelligently suggest a functional grouping for `.env` files to improve readability.

## Installation

### From Git Repository

To install `enity` directly from the Git repository, use the following command:

```bash
pip install git+https://github.com/MLGBJDLW/enity.git
```

### For Local Development

1.  Clone the repository:
    ```bash
    git clone https://github.com/MLGBJDLW/enity.git
    cd enity
    ```
2.  Install dependencies using Poetry:
    ```bash
    poetry install
    ```

## Usage

**Display Version**
```bash
enity --version
```

**Check Project Configuration**
```bash
enity check
```

**Generate .env.example**
```bash
enity generate
```

**Synchronize .env File**
```bash
enity sync
```

**Tidy .env File**
```bash
enity tidy
```

**Load Configurations**

The `load` command allows you to bulk inject configurations from a file or standard input. It supports various formats and automatically chains `tidy` and `generate` commands for a seamless workflow.

*   **From standard input (e.g., clipboard):**
    ```bash
    pbpaste | enity load --format json
    ```

*   **From a file:**
    ```bash
    enity load --from-file secrets.env --format env
    ```

---

**Suggest a Grouped Layout for .env Files**

The `suggest-layout` command intelligently suggests a grouped layout for your `.env` file, making it more readable and organized.

-   **Basic Usage:**
    ```bash
    enity suggest-layout [FILE_PATH]
    ```
    If `FILE_PATH` is not provided, it defaults to `.env.example`.

-   **Custom Grouping with `.enity.toml`:**
    You can define custom grouping rules by creating an `.enity.toml` file in your project's root directory.

    *Example `.enity.toml`:*
    ```toml
    # .enity.toml

    [grouping_rules]
    # Defines a group named "Clerk Authentication"
    clerk = { name = "Clerk Authentication", keywords = ["CLERK"] }

    # Defines a group named "Database"
    database = { name = "Database", prefixes = ["DB_"], keywords = ["DATABASE"] }
    ```

-   **Intelligent Fallback:**
    If `.enity.toml` does not exist or fails to cover all variables, the command automatically uses a keyword-based smart grouping algorithm as a fallback.

---

# enity (中文)

`enity` 是一个用于项目维护和规范化的命令行工具。

---

## 功能

-   `--version`：显示当前版本号。
-   `check`：检查项目配置，例如自动为 `.gitignore` 添加 `.env` 规则。
-   `generate`：从 `.env` 文件生成 `.env.example`。
-   `sync`：将变量从 `.env.example` 同步到 `.env`。
-   `tidy`：通过对键进行排序来整理 `.env` 文件。
-   `load`：从文件或标准输入批量注入配置，并自动触发 `tidy` 和 `generate`。
-   `suggest-layout`：为 `.env` 文件智能建议一个按功能分组的布局，以提高可读性。

## 安装说明

### 从 Git 仓库安装

要直接从 Git 仓库安装 `enity`，请使用以下命令。

```bash
pip install git+https://github.com/MLGBJDLW/enity.git
```

### 本地开发安装

1.  克隆仓库：
    ```bash
    git clone https://github.com/MLGBJDLW/enity.gi
    cd enity
    ```
2.  使用 Poetry 安装依赖：
    ```bash
    poetry install
    ```

## 使用方法

**显示版本号**
```bash
enity --version
```

**检查项目配置**
```bash
enity check
```

**生成 .env.example**
```bash
enity generate
```

**同步 .env 文件**
```bash
enity sync
```

**整理 .env 文件**
```bash
enity tidy
```

**为 .env 文件建议分组布局**

`suggest-layout` 命令会智能地为您的 `.env` 文件建议一个分组布局，使其更具可读性和组织性。

-   **基本用法：**
    ```bash
    enity suggest-layout [FILE_PATH]
    ```
    如果未提供 `FILE_PATH`，则默认为 `.env.example`。

-   **使用 `.enity.toml` 自定义分组：**
    您可以通过在项目根目录中创建一个 `.enity.toml` 文件来定义自定义分组规则。

    *`.enity.toml` 示例：*
    ```toml
    # .enity.toml

    [grouping_rules]
    # 定义一个名为 "Clerk Authentication" 的分组
    clerk = { name = "Clerk Authentication", keywords = ["CLERK"] }

    # 定义一个名为 "Database" 的分组
    database = { name = "Database", prefixes = ["DB_"], keywords = ["DATABASE"] }
    ```

-   **智能回退机制：**
    如果 `.enity.toml` 文件不存在或未能覆盖所有变量，该命令会自动使用基于关键字的智能分组算法作为备用方案。
