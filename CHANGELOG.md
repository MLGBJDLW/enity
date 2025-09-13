# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - YYYY-MM-DD

### Added

- Initial release of `enity`.
- `check` command to find discrepancies between `.env` and `.env.example`.
- `sync` command to add missing keys from `.env.example` to `.env`.
- `tidy` command to sort keys in `.env` files.
- `generate` command to create `.env.example` from `.env`.
- `load` command to bulk inject configurations from a file or standard input.
- `suggest-layout` command to intelligently suggest a functional grouping for .env files based on custom rules and keyword analysis.