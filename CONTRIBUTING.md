# Contributing Guidelines

Thank you for considering contributing to the MCP Server Replicate project! This document outlines our contribution process and commit message conventions.

## Conventional Commits

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages. This leads to more readable messages that are easy to follow when looking through the project history.

### Commit Message Format
Each commit message consists of a **header**, a **body** and a **footer**. The header has a special format that includes a **type**, a **scope** and a **subject**:

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

The **header** is mandatory and the **scope** of the header is optional.

### Types
Must be one of the following:

* **feat**: A new feature
* **fix**: A bug fix
* **docs**: Documentation only changes
* **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc)
* **refactor**: A code change that neither fixes a bug nor adds a feature
* **perf**: A code change that improves performance
* **test**: Adding missing tests or correcting existing tests
* **build**: Changes that affect the build system or external dependencies
* **ci**: Changes to our CI configuration files and scripts
* **chore**: Other changes that don't modify src or test files
* **revert**: Reverts a previous commit

### Scope
The scope should be the name of the module affected (as perceived by the person reading the changelog generated from commit messages).

### Subject
The subject contains a succinct description of the change:

* use the imperative, present tense: "change" not "changed" nor "changes"
* don't capitalize the first letter
* no dot (.) at the end

### Body
The body should include the motivation for the change and contrast this with previous behavior.

### Footer
The footer should contain any information about **Breaking Changes** and is also the place to reference GitHub issues that this commit **Closes**.

### Examples

```
feat(server): add ability to specify prediction timeout

Add new timeout parameter to prediction tool that allows setting a custom
timeout value for model inference requests.

Closes #123
```

```
fix(client): handle API rate limiting errors

Add exponential backoff retry logic when encountering rate limit responses
from Replicate API.
```

```
docs(readme): update installation instructions

Update README with new UV-based installation steps and environment setup.
```

```
refactor(tools): simplify prediction response handling

Extract response parsing logic into separate function for better reusability
and testing.
```

## Development Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Make your changes
4. Write or update tests as needed
5. Update documentation as needed
6. Commit your changes following conventional commits format
7. Push to your fork
8. Open a Pull Request

## Pull Request Process

1. Ensure your PR includes a clear description of the changes
2. Update relevant documentation
3. Add/update tests as needed
4. Ensure all tests pass
5. Request review from maintainers
6. Address any review feedback

## Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to all public functions/methods
- Keep functions/methods focused and concise
- Use meaningful variable names

## Testing

- Write tests for all new features
- Update tests when modifying existing features
- Ensure all tests pass before submitting PR
- Maintain or improve code coverage

## Questions?

If you have questions about the contribution process or need help getting started, please open a discussion in the GitHub repository.
