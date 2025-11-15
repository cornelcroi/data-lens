# Contributing to Data Lens

Thank you for your interest in contributing to Data Lens!

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature or fix
4. Make your changes
5. Run tests to ensure everything works
6. Submit a pull request

## Development Setup

```bash
git clone https://github.com/yourusername/data-lens
cd data-lens
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest tests/ -v
```

## Code Quality

- Write clean, readable code
- Add tests for new functionality
- Keep imports organized at the top of files
- Avoid unnecessary comments
- Follow existing code style

## Pull Request Process

1. Ensure all tests pass
2. Update README.md if needed
3. Add a clear description of your changes
4. Reference any related issues

## Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

## Questions?

Open an issue for questions or join discussions in the repository.

Thank you for contributing!
