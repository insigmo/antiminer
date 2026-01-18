# AntiMiner

AntiMiner is a system analysis and threat remediation tool built with Python, Flet, and uvloop.

## Features
- **Dynamic Concurrency**: Automatically selects between `asyncio` for IO-bound tasks and `ProcessPoolExecutor` for CPU-bound tasks.
- **Python 3.14 Ready**: Designed for free-threaded Python compatibility by avoiding GIL-dependent patterns.
- **Modern UI**: Built with Flet for a responsive, cross-platform experience.
- **Strict Architecture**: Follows a formal specification for state management and task scheduling.

## Installation
Requires `uv` for dependency management.

```bash
uv pip install .
```

## Usage
Launch the application via the CLI:
```bash
antiminer
```

## Testing
Run the test suite using `pytest`:
```bash
pytest
```
