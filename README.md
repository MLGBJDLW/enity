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
