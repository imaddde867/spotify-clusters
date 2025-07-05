# Development Guide

This document provides information for developers working on the Spotify AI Music Recommendation System.

## 🚀 Quick Start for Developers

### 1. Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/imaddde867/spotify-clusters.git
cd spotify-clusters

# Install dependencies (including development tools)
pip install -r requirements.txt
pip install -e .[dev]  # Install development dependencies from pyproject.toml

# Or install development dependencies manually
pip install black isort flake8 mypy pytest pytest-cov pytest-flask psutil
```

### 2. Development Server

Use the enhanced development server with monitoring and debug features:

```bash
# Start development server with enhanced features
python scripts/dev/dev_server.py

# Custom port and debug settings
python scripts/dev/dev_server.py --port 8000 --no-debug
```

Features of the development server:
- ✅ Auto-reload on file changes
- ✅ Performance monitoring and system metrics
- ✅ Enhanced logging with file output
- ✅ Health checks and debug endpoints
- ✅ Dependency and model file validation

### 3. Code Quality Tools

Run all quality checks with a single command:

```bash
# Run all quality checks
python scripts/dev/quality_check.py

# Auto-fix formatting issues
python scripts/dev/quality_check.py --fix

# Fast mode (skip slower checks)
python scripts/dev/quality_check.py --fast
```

Individual tools:
```bash
# Code formatting
black src/ tests/

# Import sorting
isort src/ tests/

# Linting
flake8 src/ tests/

# Type checking
mypy src/

# Testing
pytest tests/ -v
```

## 📁 Enhanced Project Structure

```
spotify-clusters/
├── 🎯 Core Application
│   └── src/
│       ├── recommendation_engine.py    # Core ML recommendation engine
│       ├── utils/                      # NEW: Utility modules
│       │   ├── __init__.py
│       │   ├── logging_config.py       # Centralized logging configuration
│       │   └── performance.py          # Performance monitoring tools
│       ├── models/                     # Trained ML models and scalers
│       └── web/                        # Web application
│           ├── app.py                  # Flask web server (enhanced)
│           ├── templates/              # HTML templates
│           └── static/                 # Frontend assets
├── 🧪 Testing Infrastructure           # NEW: Comprehensive testing
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py                 # Test configuration and fixtures
│       ├── test_basic_functionality.py # Basic functionality tests
│       ├── test_recommendation_engine.py # Core engine tests
│       └── test_web_app.py            # Web application tests
├── 🔧 Development Scripts             # NEW: Development utilities
│   └── scripts/
│       └── dev/
│           ├── dev_server.py          # Enhanced development server
│           └── quality_check.py       # Code quality automation
├── ⚙️ Configuration                   # ENHANCED: Better configuration
│   ├── .flake8                       # NEW: Linting configuration
│   ├── pyproject.toml                 # NEW: Modern Python project config
│   ├── requirements.txt               # ENHANCED: Updated dependencies
│   └── .gitignore                     # Improved Git ignore rules
└── 📚 Documentation
    ├── docs/
    └── README.md                      # ENHANCED: Better documentation
```

## 🛠️ Development Features Added

### Code Quality & Standards
- ✅ **Black** for consistent code formatting
- ✅ **isort** for import organization  
- ✅ **flake8** for code linting and style checks
- ✅ **mypy** for static type checking
- ✅ **pyproject.toml** for modern Python project configuration

### Testing Infrastructure
- ✅ **pytest** as the testing framework
- ✅ **pytest-cov** for code coverage reporting
- ✅ **pytest-flask** for Flask application testing
- ✅ Comprehensive test suite with unit and integration tests
- ✅ Test fixtures and mocking utilities

### Logging & Monitoring
- ✅ **Centralized logging configuration** with rotating file handlers
- ✅ **Performance monitoring** with context managers and decorators
- ✅ **System metrics collection** (CPU, memory, disk usage)
- ✅ **Request tracking** and analytics logging

### Security & Validation
- ✅ **Enhanced input validation** with length limits and sanitization
- ✅ **Type checking** for request parameters
- ✅ **Error handling improvements** with detailed logging
- ✅ **Rate limiting considerations** in API design

### Development Experience
- ✅ **Development server** with enhanced features and monitoring
- ✅ **Automated quality checks** with fix capabilities
- ✅ **Dependency validation** and health checks
- ✅ **Hot reloading** and debug tools

## 📊 Quality Metrics

After improvements, the codebase now features:

- **Code Coverage**: 30%+ with comprehensive test suite
- **Code Quality**: All files pass linting (flake8, black, isort)
- **Type Safety**: Type hints added for core functions
- **Documentation**: Enhanced docstrings and inline documentation
- **Security**: Input validation and error handling improvements
- **Performance**: Monitoring and optimization tools

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_basic_functionality.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run only fast tests
pytest tests/test_basic_functionality.py
```

### Test Categories

- **Unit Tests**: Individual function and class testing
- **Integration Tests**: Component interaction testing  
- **Web App Tests**: Flask route and API testing
- **Performance Tests**: Response time and resource usage

## 📈 Performance Monitoring

The application now includes comprehensive performance monitoring:

```python
# Using performance decorators
from utils.performance import monitor_ml_operation

@monitor_ml_operation
def my_ml_function():
    # Function is automatically monitored
    pass

# Using context manager
from utils.performance import monitor_operation

with monitor_operation("data_processing"):
    # Code block is monitored
    pass
```

## 🚨 Error Handling & Logging

Enhanced error handling and logging throughout:

```python
from utils.logging_config import get_logger

logger = get_logger("my_module")
logger.info("Operation started")
logger.error("Operation failed", exc_info=True)
```

## 🎯 Next Steps for Development

1. **Expand Test Coverage**: Add more integration tests and edge cases
2. **API Documentation**: Generate OpenAPI/Swagger documentation
3. **Container Support**: Add Docker configuration for deployment
4. **CI/CD Pipeline**: Set up automated testing and deployment
5. **Performance Optimization**: Profile and optimize bottlenecks
6. **Security Audit**: Comprehensive security review and hardening

## 💡 Development Tips

- Use the quality check script before committing changes
- Monitor performance with the built-in tools
- Check logs in the `logs/` directory for debugging
- Use the development server for enhanced debugging
- Run tests frequently during development
- Follow the existing code style and conventions

For more information, see the main [README.md](../README.md) and project documentation.