# Third-Party Dependencies

## License Compatibility Matrix
| Dependency | License | Usage Type | Compatibility with AGPL v3.0 |
|------------|---------|------------|------------------------------|
| **antlr4-python3-runtime** | BSD 3-Clause | Runtime | ✅ Compatible |
| **Pydantic** | MIT License | Runtime | ✅ Compatible |
| **SymPy** | BSD 3-Clause | Runtime | ✅ Compatible |




<!-- We'll see later if we need to add more dependencies -->
<!-- | **Jinja2** | BSD 3-Clause | Runtime | ✅ Compatible | -->

## Usage Model

**Important**: PCA Teachers distributes dependencies through standard PyPI mechanisms under AGPL v3.0 licensing - we do not modify, fork, or bundle any third-party source code with our package.

### AGPL Distribution Implications
- **No source code modification**: All dependencies used as-is from PyPI
- **No redistribution**: Dependencies installed independently by end users
- **Strong copyleft obligations**: AGPL requires source availability for all users
- **Network service coverage**: AGPL extends to network-based usage of the software

## License Requirements

### antlr4-python3-runtime (BSD 3-Clause)
- **Project**: ANTLR Project / antlr/antlr4
- **Usage**: Runtime library for ANTLR4 generated parsers (required by SymPy)
- **Integration**: Critical dependency for LaTeX parsing functionality
- **Compliance Requirements**:
  - ✅ Permissive license fully compatible with AGPL distribution
  - ✅ Attribution satisfied through PyPI package metadata
  - ✅ Version locked to 4.11.0 for SymPy compatibility

<!-- ### Jinja2 (BSD 3-Clause)
- **Project**: Pallets/Jinja
- **Usage**: Template engine for mathematical content generation
- **Integration**: Handles templating for educational content creation
- **Compliance Requirements**:
  - ✅ Permissive license fully compatible with AGPL
  - ✅ Attribution satisfied through PyPI package metadata
  - ✅ BSD allows incorporation into copyleft projects -->

### Pydantic (MIT License)
- **Project**: pydantic/pydantic
- **Usage**: Data validation and settings management
- **Integration**: Provides type validation for mathematical objects and configurations
- **Compliance Requirements**:
  - ✅ Permissive license fully compatible with AGPL distribution
  - ✅ No additional obligations beyond copyright notice
  - ✅ MIT allows incorporation into AGPL projects

### SymPy (BSD 3-Clause)
- **Project**: sympy/sympy
- **Usage**: Symbolic mathematics library and computational engine
- **Integration**: Core dependency for mathematical object manipulation and LaTeX parsing
- **Compliance Requirements**:
  - ✅ Permissive license fully compatible with AGPL
  - ✅ Attribution satisfied through PyPI package metadata
  - ✅ **Critical dependency** - drives antlr4 version requirement

## License Compatibility Analysis

### AGPL v3.0 Distribution
All dependencies use permissive licenses fully compatible with AGPL v3.0:
- **No copyleft conflicts**: All dependencies use BSD 3-Clause or MIT licenses
- **Permissive incorporation**: All licenses explicitly allow use in copyleft projects
- **Standard PyPI distribution**: Well-established legal framework for AGPL packages
- **Network service obligations**: AGPL requirements apply to any network deployment

## PCA Teachers AGPL v3.0 Licensing

### ✅ **AGPL v3.0 Distribution**
- No license conflicts with any runtime dependencies
- All permissive licenses allow incorporation into AGPL projects
- Users receive standard PyPI installation experience with AGPL obligations
- Source code availability requirements satisfied for entire package
- Network use provisions clearly documented and enforceable

## Compliance Checklist
- [x] **License Compatibility**: All dependencies compatible with AGPL v3.0
- [x] **No Redistribution**: Dependencies obtained through standard PyPI channels
- [x] **No Modification**: Using all dependencies as officially distributed
- [x] **Attribution**: Satisfied through PyPI package metadata system
- [x] **AGPL Distribution**: Full source code available under AGPL v3.0
- [x] **Network Use Provisions**: AGPL network service obligations documented
- [x] **Version Compatibility**: antlr4 version locked for SymPy compatibility

## Full License References
For complete license texts:
- **AGPL v3.0**: https://www.gnu.org/licenses/agpl-3.0.html
- **MIT License**: https://opensource.org/licenses/MIT
- **BSD 3-Clause**: https://opensource.org/licenses/BSD-3-Clause

## Legal Disclaimer
This analysis is based on our understanding of the licenses and standard PyPI distribution practices. AGPL v3.0 imposes strong copyleft obligations including network service provisions. For critical applications, consult with qualified legal counsel to ensure compliance with all applicable licenses and regulations.