# enity

`enity` 是一个用于项目维护和规范化的命令行工具。

---

## 功能

-   `--version`：显示当前版本号。
-   `check`：检查项目配置，例如自动为 `.gitignore` 添加 `.env` 规则。
-   `generate`：从 `.env` 文件生成 `.env.example`。
-   `sync`：将变量从 `.env.example` 同步到 `.env`。
-   `tidy`：通过对键进行排序来整理 `.env` 文件。

## 使用方法

**显示版本号**
```bash
enity --version
```

**检查项目配置**
```bash
enity check
```

**生成 .env.example**```bash
enity generate
```

**同步 .env 文件**
```bash
enity sync
```

**整理 .env 文件**
```bash
enity tidy
