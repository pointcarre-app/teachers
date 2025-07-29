# Changelog

All notable changes to the PCA Teachers project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.5] - 2025-01-09

### Added
- **Interactive Code Playground**: New `playground.html` page with CodeMirror editor for real-time testing
  - Full-featured Python code editor with syntax highlighting and Monokai theme
  - Real-time execution of PCA Teachers framework code using Pyodide
  - Six comprehensive example categories covering all major framework features:
    - Basic mathematical objects and operations
    - Fractions and LaTeX generation
    - Equations and mathematical relations
    - Correction system testing
    - Complex expression building and simplification
    - Unit test execution from the test suite
  - Professional UI with status indicators, keyboard shortcuts (Ctrl+Enter), and error handling
  - Cross-platform compatibility for both GitHub Pages and local development

### Enhanced
- **Navigation System**: Added navigation bar to both demo pages
  - Cross-page navigation between Test Suite and Code Playground
  - Consistent styling and user experience across demo pages
  - Easy discovery of interactive features for GitHub Pages visitors

### Fixed
- **TOML Configuration**: Improved `pyproject.toml` structure for better compatibility
  - Moved project URLs to proper `[project.urls]` section
  - Enhanced project metadata organization

### Technical
- **CodeMirror Integration**: Added CodeMirror 6.65.7 for professional code editing experience
- **Example Library**: Comprehensive collection of predefined scripts demonstrating framework capabilities
- **Enhanced UI/UX**: Modern responsive design with improved visual feedback and interactions

## [0.0.4] - 2025-01-09

### Changed
- **License Update**: Changed from MIT to AGPL-3.0-or-later (GNU Affero General Public License v3+)
- **Documentation**: Enhanced README with comprehensive GitHub Pages URLs section
- **URLs**: Added clear live demo URLs, interactive demo links, and repository access points

### Added
- **Live Demo URLs Section**: Added dedicated section in README with:
  - Main GitHub Pages site URL
  - Direct interactive demo link
  - Repository and development URLs
- **Better Navigation**: Improved user experience for finding and accessing live demo

### Technical
- Updated `pyproject.toml` license classifier to match AGPL-3.0-or-later
- Enhanced README structure for better discoverability of live resources

## [0.0.3] - 2025-01-29

### Fixed
- **Critical GitHub Pages Deployment Fix**
  - Simplified deployment workflow to copy entire repository
  - Fixed incorrect base URL generation causing 404 errors
  - Corrected file paths for Pyodide file loading
  - Files now properly accessible at correct GitHub Pages URLs
  - Resolved scenery demo loading issues completely

### Changed
- **Deployment Strategy**
  - Switched from selective file copying to full repository deployment
  - Much simpler and more reliable deployment process
  - Better error handling and path resolution

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

[Unreleased]: https://github.com/pointcarre-app/teachers/compare/0.0.5...HEAD
[0.0.5]: https://github.com/pointcarre-app/teachers/compare/0.0.4...0.0.5
[0.0.4]: https://github.com/pointcarre-app/teachers/compare/0.0.3...0.0.4
[0.0.3]: https://github.com/pointcarre-app/teachers/compare/0.0.2...0.0.3
[0.0.2]: https://github.com/pointcarre-app/teachers/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/pointcarre-app/teachers/releases/tag/0.0.1 