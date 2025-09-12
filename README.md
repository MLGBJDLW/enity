# enity

`enity` is a command-line tool for project maintenance and standardization.

---

## Features

-   `--version`: Display the current version number.
-   `check`: Check project configurations, such as automatically adding `.env` rules to `.gitignore`.
-   `generate`: Generate `.env.example` from an `.env` file.
-   `sync`: Synchronize variables from `.env.example` to `.env`.
-   `tidy`: Tidy up the `.env` file by sorting its keys.

## Installation

### From Git Repository

To install `enity` directly from the Git repository, use the following command. Please replace `<your-username>` and `<your-repo-name>` with the actual repository owner and name.

```bash
pip install git+https://github.com/<your-username>/<your-repo-name>.git
```

### For Local Development

1.  Clone the repository:
    ```bash
    git clone https://github.com/<your-username>/<your-repo-name>.git
    cd <your-repo-name>
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

## 安装说明

### 从 Git 仓库安装

要直接从 Git 仓库安装 `enity`，请使用以下命令。请将 `<your-username>` 和 `<your-repo-name>` 替换为实际的仓库所有者和名称。

```bash
pip install git+https://github.com/<your-username>/<your-repo-name>.git
```

### 本地开发安装

1.  克隆仓库：
    ```bash
    git clone https://github.com/<your-username>/<your-repo-name>.git
    cd <your-repo-name>
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
