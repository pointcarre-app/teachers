# Changelog

All notable changes to the PCA Teachers project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.2] - 2025-01-29

### Fixed
- **GitHub Pages Deployment Issues**
  - Fixed missing source files (`src/`, `tests/`) in GitHub Pages deployment
  - Updated GitHub Actions workflow to copy all necessary files for demo
  - Fixed hardcoded localhost URLs in scenery demo
  - Added smart environment detection (GitHub Pages vs localhost)
  - Resolved favicon 404 errors on GitHub Pages
  - Fixed file loading paths for Pyodide integration

### Added
- **Enhanced Deployment**
  - Environment detection for GitHub Pages vs local development
  - Automatic base URL switching for file loading
  - Comprehensive file copying in deployment workflow
  - Better error handling for missing resources

### Changed
- **Scenery Demo Improvements**
  - Dynamic URL generation based on environment
  - Relative path support for GitHub Pages
  - Improved file loading reliability

## [0.0.1] - 2025-01-29

### Added
- Python 3.13.5 and Pyodide 0.27.7 compatibility information in README

## [0.0.1] - 2025-01-29

### Added
- **Core Mathematical Framework**
  - Complete set of mathematical objects with SymPy integration
  - Support for integers, decimals, fractions, symbols, and infinity
  - Binary operations: addition, multiplication, powers, fractions
  - Mathematical relations: equality, inequalities
  - Set operations and intervals
  - Collections and mathematical expressions

- **LaTeX Generation**
  - Beautiful LaTeX output for all mathematical objects
  - French mathematical formatting conventions
  - Customizable rendering options
  - Integration with educational standards

- **Correction System**
  - Automated student response validation
  - Flexible tolerance settings for numerical comparisons
  - Multiple input format support
  - Detailed feedback generation
  - Pattern matching for mathematical expressions

- **Content Generation**
  - Dynamic mathematical problem generation
  - Template-based exercise creation
  - Configurable difficulty levels
  - Bulk content creation utilities

- **Interactive Web Demo**
  - Live mathematical computation with Pyodide
  - Real-time LaTeX rendering
  - Interactive test suite execution
  - Browser-based mathematical framework demonstration

- **Testing & Quality Assurance**
  - Comprehensive test suite with 122 tests
  - Coverage for all mathematical objects and operations
  - Validation tests for LaTeX output
  - Correction system verification
  - Cross-platform compatibility tests

- **Development Infrastructure**
  - Modern Python packaging with pyproject.toml
  - Automated GitHub Pages deployment
  - GitHub Actions CI/CD pipeline
  - Comprehensive documentation
  - MIT license for open source usage

### Technical Details
- **Python Requirements**: >= 3.13
- **Core Dependencies**:
  - SymPy 1.14.0 for symbolic mathematics
  - Pydantic 2.11.7 for data validation
  - ANTLR4 4.11.0 for LaTeX parsing
  - Jinja2 3.1.6 for templating
- **Web Technologies**: Pyodide 0.27.7 for browser execution
- **Architecture**: Source layout with comprehensive type hints

### Documentation
- Complete README with usage examples
- API documentation with code samples
- Installation and setup instructions
- Contributing guidelines
- Live demo deployment guide

### Deployment
- **GitHub Repository**: https://github.com/pointcarre-app/teachers
- **Live Demo**: https://pointcarre-app.github.io/teachers/
- **Package Distribution**: Ready for PyPI publication
- **Automated Deployment**: GitHub Actions workflow for Pages

[Unreleased]: https://github.com/pointcarre-app/teachers/compare/0.0.2...HEAD
[0.0.2]: https://github.com/pointcarre-app/teachers/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/pointcarre-app/teachers/releases/tag/0.0.1 