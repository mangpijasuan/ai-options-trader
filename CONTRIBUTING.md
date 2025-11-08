# Contributing to AI Options Trader

Thank you for your interest in contributing to AI Options Trader! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/ai-options-trader.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit with clear messages: `git commit -m "Add feature: description"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run setup
python setup.py

# Train model
python models/train_model.py

# Run tests (if available)
python -m pytest
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose
- Add comments for complex logic

## Testing

- Test your changes before submitting
- Add tests for new features
- Ensure existing tests still pass
- Test with paper trading account, never with live money during development

## Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Ensure code passes all tests
- Update documentation if needed
- Keep PRs focused on a single feature or fix

## Areas for Contribution

- **Features**: New trading strategies, risk management tools, analytics
- **Testing**: Unit tests, integration tests, backtesting improvements
- **Documentation**: Tutorials, examples, API documentation
- **Bug Fixes**: Report and fix bugs
- **Performance**: Optimization, code improvements
- **Data**: Additional data sources, feature engineering

## Reporting Issues

When reporting issues, please include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and environment details
- Relevant logs or error messages

## Code Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged
4. Your contribution will be credited

## Security

- Never commit API keys, passwords, or sensitive data
- Use environment variables for configuration
- Report security vulnerabilities privately to maintainers

## Community Guidelines

- Be respectful and constructive
- Help others learn and improve
- Welcome newcomers
- Focus on the code, not the person

## Questions?

Feel free to open an issue for questions or discussions.

Thank you for contributing! 🎉
