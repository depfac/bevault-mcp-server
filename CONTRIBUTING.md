## Contributing to bevault-mcp

Thank you for your interest in contributing to `bevault-mcp`, the MCP (Model Context Protocol) server for [beVault](https://www.bevault.io/).

Contributions of all kinds are welcome: bug reports, feature requests, documentation improvements, and pull requests.

---

## Development setup

1. **Clone the repository**

   ```bash
   git clone <your-fork-url>
   cd bevault-mcp-server
   ```

2. **Install Python**

   This project targets **Python 3.13+**. Make sure you have a compatible version installed.

3. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux / macOS
   source .venv/bin/activate
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the MCP server locally**

   ```bash
   python -m bevault_mcp.main
   ```

---

## Pre-commit hooks

This project uses [pre-commit](https://pre-commit.com/) to run linters and formatters before each commit. It is highly recommended to enable it locally.

### Install pre-commit

You can install `pre-commit` using either `pip` or your system package manager.

**Pip (Windows or Linux)**

You will need to have Python/pip installed on your computer.

```bash
pip install pre-commit
```

**APT (Debian & Ubuntu)**

```bash
sudo apt install -y pre-commit
```

### Enable pre-commit in this repository

From the root of the project, run:

```bash
pre-commit install
```

This will configure `git` so that the pre-commit hooks run automatically on every commit.

You can also run the hooks manually on all files:

```bash
pre-commit run --all-files
```

The configured hooks (see `.pre-commit-config.yaml`) include:

- `ruff` and `ruff-format` for linting and formatting
- `mypy` for static type checking
- `gitleaks` to detect secrets in the codebase
- Several sanity checks from `pre-commit-hooks` (trailing whitespace, JSON validity, large files, etc.)

---

## Code style

Code style and linting are enforced by **ruff**.

- Lint the code:

  ```bash
  ruff check .
  ```

- Format the code:

  ```bash
  ruff format .
  ```

Please ensure your changes pass ruff checks and formatting (either via pre-commit or by running the commands above) before opening a pull request.

Type checking is done with **mypy** (also run via pre-commit):

```bash
mypy .
```

---

## Submitting changes

1. **Fork** the repository and create your feature/bugfix branch:

   ```bash
   git checkout -b feature/my-change
   ```

2. **Make your changes**, keeping commits focused and logically grouped.

3. **Run pre-commit hooks** (if not installed globally):

   ```bash
   pre-commit run --all-files
   ```

4. **Push** your branch to your fork:

   ```bash
   git push origin feature/my-change
   ```

5. **Open a Pull Request**:

   - Clearly describe the problem you are solving or the feature you are adding.
   - Reference any related issues if applicable.
   - Mention any breaking changes or migration steps, if relevant.

Basic guidelines:

- Use **Conventional Commits** for commit messages.
- Keep PRs as small and focused as possible.

### Conventional Commits

We follow the [Conventional Commits](https://www.conventionalcommits.org/) convention. A commit message should look like:

```text
type(scope): short description
```

Common types:

- `feat`: a new feature
- `fix`: a bug fix
- `docs`: documentation only changes
- `refactor`: code refactoring that does not change behavior
- `test`: adding or updating tests
- `chore`: tooling or maintenance changes

Examples:

- `feat(client): add tool to search information marts`
- `fix(api): handle request timeout errors`
- `docs: clarify authentication via Authorization header`

If you are unsure which type to use, `chore` is acceptable, but prefer a more specific type when possible.

---

## Licensing

By contributing to this project, you agree that your contributions will be licensed under the same MIT license that covers this repository. See the [`LICENSE`](LICENSE) file for details.

---

## Questions or clarifications

If something is unclear in this guide or you are unsure how best to contribute:

- Open an issue describing your question or proposal, or
- Add a comment in your pull request explaining any open points.

If you think additional information should be added to this `CONTRIBUTING.md` file (e.g., more detailed workflows, release process, or testing strategy), please let us know in an issue or PR.

