# Changelog

All notable changes to the PCA Teachers project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.0.8] - 2025-01-16

### Fixed
- **Critical Mul Simplification Bug**: Fixed NotImplementedError when simplifying nested multiplication operations
  - `Mul.simplified()` now correctly handles `Integer * Mul(Integer, Symbol)` combinations in both orders
  - Added support for `Mul(Integer, Symbol) * Integer` combinations  
  - Added distributive property handling for nested Mul objects
  - Resolved the original bug where polynomial expansions like `(ax + b)^2` would fail during simplification
  - Added zero multiplication simplification (`0 * anything = 0`)

### Added
- **Comprehensive Mul Simplification Tests**: New `test_mul_simplification.py` test suite
  - 9 comprehensive test cases covering all nested Mul operation combinations
  - Tests for Integer*Mul, Mul*Integer, and polynomial expansion scenarios
  - Validates zero and identity multiplication edge cases
  - Tests nested multiplication flattening and associativity
  - Validates the complete fix for the original problematic scenario

### Enhanced
- **Scenery Interface** (`scenery/index.html`, `scenery/app.js`)
  - Added new test row for "Mul simplification: Integer*Mul nested operations, polynomial expansion"
  - Updated test execution logic to include the new Mul simplification validation
  - Enhanced error handling for multiplication edge cases
  - Added comprehensive test coverage for polynomial expansion scenarios

- **Test Suite Integration** (`tests/__main__.py`)
  - Added import for new `test_mul_simplification` module
  - Ensures comprehensive test coverage for the Mul simplification fix

### Technical Details
- **File Changes**:
  - `src/teachers/maths.py`: Core fix for Mul simplification with nested Mul objects (lines 531-577)
  - `tests/test_mul_simplification.py`: New comprehensive test suite (196 lines)
  - `tests/__main__.py`: Added test import for integration
  - `scenery/app.js`: Updated test execution and error handling
  - `scenery/index.html`: Added UI row for Mul simplification tests

### Known Issues Resolved
- **Mul Simplification**: Previously reported NotImplementedError for Integer * Mul combinations is now fully resolved
- **Polynomial Expansion**: Complex polynomial expressions like `(ax + b)^2` now expand correctly without errors

## [0.0.7] - 2025-01-16

### Fixed
- **Critical Add Simplification Bug**: Fixed NotImplementedError when simplifying mixed numeric type additions
  - `Add.simplified()` now correctly handles `Integer + Decimal` combinations in both orders
  - Added support for `Decimal + Fraction` combinations in both orders  
  - Added support for `Decimal + Decimal` combinations
  - Resolved the original bug where expressions like `10^4 + Decimal(0.0001) + Fraction(1/10)` would fail
  - All combinations now return appropriate `Decimal` objects with computed results

### Added
- **Comprehensive Add Simplification Tests**: New `test_add_simplification.py` test suite
  - 12 comprehensive test cases covering all mixed numeric type combinations
  - Tests for Integer+Decimal, Decimal+Fraction, and Decimal+Decimal operations
  - Validates both p/q and x forms of Decimal objects
  - Tests edge cases including zero values, large numbers, and nested expressions
  - Validates the complete fix for the original problematic scenario

### Enhanced
- **Scenery Interface** (`scenery/index.html`, `scenery/app.js`)
  - Added new test row for "Add simplification: Integer+Decimal, Decimal+Fraction combinations"
  - Updated test execution logic to include the new Add simplification validation
  - Enhanced UI styling with improved font family (Segoe UI)
  - Fixed width layout for better consistency

- **Test Suite Integration** (`tests/__main__.py`)
  - Added import for new `test_add_simplification` module
  - Ensures comprehensive test coverage for the Add simplification fix

### Technical Details
- **File Changes**:
  - `src/teachers/maths.py`: Core fix for Add simplification with mixed numeric types (lines 412-436)
  - `tests/test_add_simplification.py`: New comprehensive test suite (203 lines)
  - `tests/__main__.py`: Added test import for integration
  - `scenery/app.js`: Updated test execution and error handling
  - `scenery/index.html`: Added UI row and improved styling

### Known Issues Resolved
- **Add Simplification**: Previously reported NotImplementedError for Integer + Decimal combinations is now fully resolved

## [0.0.6] - 2025-01-16

### Fixed
- **Critical Negative Exponent Bug**: Fixed ValidationError when simplifying negative integer exponents
  - `Pow.simplified()` now correctly converts `Integer(n)^Integer(-m)` to `Fraction(1, n^m)` instead of attempting to create `Integer(n=float)`
  - Added field validators to `Pow` class for automatic type conversion of base and exp parameters
  - Resolved the original bug where `10^(-2)` would fail with "Input should be a valid integer, got a number with a fractional part"
  
- **Pyodide Test Runner**: Fixed JSON parsing issue in antlr4 test execution
  - Added proper JSON parsing for missive results in `app.js`
  - Test was passing but incorrectly showing as failed due to string/object type mismatch

### Added
- **Comprehensive Negative Exponent Tests**: New `test_negative_exponents.py` test suite
  - 10 test cases covering various negative exponent scenarios
  - Tests for conversion to Decimal, addition operations, and edge cases
  - Validates the complete fix for the original problematic scenario

- **Micropip Installation Test**: New `test_antlr4.py` for package installation verification
  - Tests successful import of `antlr4-python3-runtime` via micropip
  - Verifies presence of expected module attributes (InputStream, CommonTokenStream)
  - Integrated into web test suite as "micropip install antlr4-python3-runtime"

### Enhanced
- **Web Test Infrastructure** (`scenery/app.js`)
  - Refactored to use separate Nagini managers for different test groups
  - Isolated micropip test in minimal manager for better performance
  - Fixed CORS issues with dynamic `window.location.origin` usage
  - Improved error handling and JSON parsing for test results
  - Updated to Nagini v0.0.21 for better compatibility

- **Server Configuration** (`serve.py`)
  - Added cache-busting headers to prevent stale file loading
  - Implemented `allow_reuse_port` for better port management
  - Enhanced CORS headers with no-cache directives

- **Test Suite Display** (`scenery/index.html`)
  - Added visual indicators for negative exponent tests
  - Reorganized test categories with clearer grouping
  - Updated test status display for better visibility

- **Code Playground** (`scenery/playground.html`)
  - Added "Negative Exponents" example demonstrating the bug fix
  - Enhanced error output to display Python stderr content
  - Fixed CORS issues with dynamic base URL configuration
  - Improved debugging capabilities with detailed error messages

### Technical Details
- **File Changes**:
  - `src/teachers/maths.py`: Core fix for negative exponent handling in Pow class
  - `tests/test_negative_exponents.py`: New comprehensive test suite (161 lines)
  - `tests/test_antlr4.py`: New micropip installation test (36 lines)
  - `scenery/app.js`: Major refactoring for test isolation (487 lines)
  - `scenery/index.html`: Updated test display structure
  - `scenery/playground.html`: Enhanced with new examples and error handling
  - `serve.py`: Added cache control and port reuse configuration

### Known Issues
- **Corrector Tests**: Currently failing (5/12 passed) - investigation needed
- **Add Simplification**: NotImplementedError for Integer + Decimal combinations

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

[Unreleased]: https://github.com/pointcarre-app/teachers/compare/0.0.8...HEAD
[0.0.8]: https://github.com/pointcarre-app/teachers/compare/0.0.7...0.0.8
[0.0.7]: https://github.com/pointcarre-app/teachers/compare/0.0.6...0.0.7
[0.0.6]: https://github.com/pointcarre-app/teachers/compare/0.0.5...0.0.6
[0.0.5]: https://github.com/pointcarre-app/teachers/compare/0.0.4...0.0.5
[0.0.4]: https://github.com/pointcarre-app/teachers/compare/0.0.3...0.0.4
[0.0.3]: https://github.com/pointcarre-app/teachers/compare/0.0.2...0.0.3
[0.0.2]: https://github.com/pointcarre-app/teachers/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/pointcarre-app/teachers/releases/tag/0.0.1 