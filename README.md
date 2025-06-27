# ReCodEx Client

A command-line interface for the [ReCodEx](https://recodex.mff.cuni.cz/) system. This tool allows users to interact with ReCodEx from their terminal, streamlining workflows and enabling scripting possibilities.

## What is ReCodEx?

ReCodEx (Reusable Community-developed Exercises) is a system for dynamic analysis and evaluation of programming exercises. It allows supervisors to assign programming problems to students, who can then submit their solutions through a web interface. ReCodEx automatically evaluates these solutions by compiling and executing them in a safe environment, providing quick feedback to students.

## Key Features

* **Authentication:** Securely log in to your ReCodEx account.
* **Execute Requests:** Send requests and view responses from the command line.
* **Interactive mode:** You can use the interactive mode to browse and use existing endpoints.
* **Plugins:** Use existing or write your own plugins to streamline work.

## Installation

You can install the ReCodEx CLI using `pip`. It is recommended to use Python 11:

```bash
PIP_EXTRA_INDEX_URL="https://test.pypi.org/simple/" pip install recodex_cli_eceltov
```
