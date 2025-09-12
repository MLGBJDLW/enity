# enity

[![PyPI version](https://img.shields.io/pypi/v/enity.svg)](https://pypi.org/project/enity/)
[![CI](https://github.com/[YOUR_GITHUB_USERNAME]/[YOUR_REPO_NAME]/actions/workflows/ci.yml/badge.svg)](https://github.com/[YOUR_GITHUB_USERNAME]/[YOUR_REPO_NAME]/actions/workflows/ci.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/enity.svg)](https://pypi.org/project/enity/)
[![License](https://img.shields.io/pypi/l/enity.svg)](https://github.com/[YOUR_GITHUB_USERNAME]/[YOUR_REPO_NAME]/blob/main/LICENSE)

A simple tool to manage your .env files.

---

## Installation

```bash
pip install enity
```

## Quick Start

Check for discrepancies between `.env` and `.env.example`:

```bash
enity check --env .env --example .env.example
```

Generate `.env.example` from `.env`:
```bash
enity generate
```

Synchronize variables from `.env.example` to `.env`:
```bash
enity sync
```

Tidy up an `.env` file by sorting keys:
```bash
enity tidy
