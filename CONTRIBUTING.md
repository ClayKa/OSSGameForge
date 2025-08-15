# Contributing to OSSGameForge

First off, thank you for considering contributing to OSSGameForge! It's people like you that make OSSGameForge such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and explain which behavior you expected to see instead**
* **Explain why this enhancement would be useful**

### Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Process

1. **Set up your development environment**
   ```bash
   git clone https://github.com/ClayKa/oss-game-forge.git
   cd oss-game-forge
   make install
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

4. **Run tests and linting**
   ```bash
   make test
   make lint
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

   We follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `style:` Code style changes (formatting, etc)
   - `refactor:` Code refactoring
   - `test:` Test changes
   - `chore:` Build process or auxiliary tool changes

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**

## Style Guidelines

### Python Style Guide

We use:
- [Black](https://github.com/psf/black) for code formatting
- [Ruff](https://github.com/charliermarsh/ruff) for linting
- [MyPy](http://mypy-lang.org/) for type checking

Run `make format` to automatically format your code.

### JavaScript/TypeScript Style Guide

We use:
- [ESLint](https://eslint.org/) for linting
- [Prettier](https://prettier.io/) for formatting

Run `npm run format` in the frontend directory.

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

## Testing

* Write unit tests for all new functionality
* Ensure all tests pass before submitting PR
* Aim for >80% code coverage
* Include integration tests for API endpoints
* Add E2E tests for critical user workflows

## Documentation

* Update the README.md with details of changes to the interface
* Update the API documentation for new endpoints
* Add docstrings to all functions and classes
* Include inline comments for complex logic

## Project Structure

```
oss-game-forge/
├── backend/          # FastAPI backend
│   ├── app/         # Application code
│   └── tests/       # Backend tests
├── frontend/         # React frontend
│   ├── src/         # Source code
│   └── tests/       # Frontend tests
├── devops/          # Infrastructure
└── docs/            # Documentation
```

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing! 🎉