# 🧮 PCA Teachers - Mathematical Framework

Tested with Python 3.13.5 and Pyodide 0.27.7

A comprehensive Python framework for educational mathematical content creation, built on SymPy with robust validation, LaTeX generation, and correction workflows.

## 📋 Table of Contents

- [Overview](#overview)
- [Live Demo](#live-demo)
- [Architecture](#architecture)
- [Installation](#installation)
- [Core Components](#core-components)
- [Mathematical Objects](#mathematical-objects)
- [Usage Examples](#usage-examples)
- [LaTeX Generation](#latex-generation)
- [Correction System](#correction-system)
- [Testing](#testing)
- [Contributing](#contributing)

## 🎯 Overview

PCA Teachers is designed for educational platforms that need to:
- Generate mathematical expressions programmatically
- Validate student mathematical input
- Provide automated correction and feedback
- Render mathematical content as LaTeX
- Handle complex symbolic computation workflows

### Key Features

- **🔢 Rich Mathematical Objects**: Comprehensive set of mathematical primitives
- **✅ Robust Validation**: Pydantic-based validation with SymPy integration
- **📝 LaTeX Generation**: Clean, properly formatted mathematical notation
- **🎯 Correction Engine**: Automated student response validation
- **🔧 Educational Tools**: Specialized formatting for French mathematical education
- **🧪 100% Test Coverage**: Comprehensive test suite with 140+ tests
- **🆕 Decimal × Function Support**: NEW! Seamless multiplication of decimal coefficients with function applications  
- **🆕 Pi (π) Mathematical Constant**: NEW! Complete Pi support for geometric formulas and calculations

## 🚀 Live Demo

Experience PCA Teachers in action: **[https://pointcarre-app.github.io/teachers/](https://pointcarre-app.github.io/teachers/)**

### 🌐 **Live Demo URLs:**
- **Main Site**: https://pointcarre-app.github.io/teachers/
- **Interactive Demo**: https://pointcarre-app.github.io/teachers/scenery/
- **Repository**: https://github.com/pointcarre-app/teachers

The interactive demo showcases:
- Live mathematical computation with Pyodide
- Real-time LaTeX rendering  
- Unit test execution in the browser
- Framework capabilities demonstration

## 🏗️ Architecture

```
src/teachers/
├── maths.py          # Core mathematical objects and operations
├── corrector.py      # Student response correction pipeline
├── generator.py      # Mathematical content generation utilities  
├── formatting.py     # Educational formatting guidelines (French)
├── defaults.py       # System constants and defaults
└── __init__.py       # Package initialization
```

### Technology Stack

- **SymPy 1.14.0**: Symbolic mathematics foundation
- **Pydantic 2.11.7**: Data validation and serialization
- **ANTLR4 4.11.0**: LaTeX parsing (SymPy integration)
- **Python 3.13+**: Modern Python features and type hints

## 🚀 Installation

### Prerequisites

```bash
# Python 3.13 or higher required
python --version
```

### Setup

```bash
# Clone and setup virtual environment
git clone <repository-url>
cd pca-teachers
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -e .
```

### Dependencies

```toml
dependencies = [
    "antlr4-python3-runtime==4.11.0",
    "jinja2==3.1.6", 
    "pydantic==2.11.7",
    "sympy==1.14.0"
]
```

## 🧮 Core Components

### 1. Mathematical Objects (`maths.py`)

The heart of the framework - a complete set of mathematical primitives with SymPy integration.

#### Base Architecture

```python
class MathsObject(BaseModel):
    """Base class for all mathematical objects"""
    sympy_expr: sp.Basic
    
    def latex(self) -> str: ...        # LaTeX representation
    def simplified(self) -> 'MathsObject': ...  # Mathematical simplification  
    def eval(self) -> float: ...       # Numerical evaluation
```

#### Object Hierarchy

```
MathsObject
├── Atomic Objects
│   ├── Integer(n: int)
│   ├── Symbol(s: str)  
│   ├── Decimal(x: float | p: int, q: int)
│   ├── Inf()
│   └── Pi() 🆕
├── Binary Operators
│   ├── Add(l: MathsObject, r: MathsObject)
│   ├── Mul(l: MathsObject, r: MathsObject)
│   ├── Fraction(p: MathsObject, q: MathsObject)
│   └── Pow(base: MathsObject, exp: MathsObject)
├── Relations
│   ├── Equality(l: MathsObject, r: MathsObject)
│   └── StrictGreaterThan(l: MathsObject, r: MathsObject)
├── Sets
│   └── Interval(l: MathsObject, r: MathsObject, left_open: bool, right_open: bool)
├── Collections
│   └── MathsCollection(elements: List[MathsObject])
└── Functions
    ├── Function(name: str)
    └── Image(f: Function, pre: MathsObject | MathsCollection)
```

### 2. Parser System (`maths.py`)

Bidirectional conversion between representations:

```python
class MathsObjectParser:
    @staticmethod
    def from_repr(repr_str: str) -> MathsObject:
        """Parse string representation back to objects"""
    
    @staticmethod  
    def from_sympy(sympy_expr: sp.Basic) -> MathsObject:
        """Convert SymPy expressions to MathsObject"""
        
    def from_latex(self, latex: str) -> MathsObject:
        """Parse LaTeX strings to mathematical objects"""
```

### 3. Correction Engine (`corrector.py`)

Automated student response validation:

```python
def correct(user_input: str, teacher_answer: MathsObject) -> CorrectionResult:
    """
    Complete correction workflow:
    1. Clean MathLive input formatting
    2. Parse LaTeX to MathsObject  
    3. Simplify both expressions
    4. Compare mathematical equivalence
    5. Generate feedback
    """
```

### 4. Educational Formatting (`formatting.py`)

French educational system compliance:

```python
class Formatting(Enum):
    DECIMAL_OR_INTEGER = "DECIMAL_OR_INTEGER"
    PERCENT = "PERCENT" 
    FRACTION_OR_INTEGER = "FRACTION_OR_INTEGER"
    # ... specialized educational formats
```

## 🔢 Mathematical Objects

### Atomic Objects

#### Integer
```python
# Basic integer representation
num = tm.Integer(n=42)
print(num.latex())  # "42"
print(num.eval())   # 42

# Negative numbers
neg = tm.Integer(n=-17)
print(neg.latex())  # "-17"

# as_decimal property for clean decimal conversion
integer = tm.Integer(n=5)
decimal = integer.as_decimal
print(decimal.latex())  # "5" (clean, no decimal point)

# as_percent property for percentage conversion
integer = tm.Integer(n=4)
percent = integer.as_percent
print(percent.latex())  # "400" (4 * 100)

# Useful for expressions that may result in Integer or Fraction
result = (some_fraction * some_integer).simplified()
clean_decimal = result.as_decimal  # Works for both Integer and Fraction results
clean_percent = result.as_percent   # Works for both Integer and Fraction results
print(clean_decimal.latex())  # Always clean decimal formatting
print(clean_percent.latex())   # Always clean percentage formatting
```

#### Symbol
```python
# Mathematical variables
x = tm.Symbol(s="x")
y = tm.Symbol(s="y") 
print(x.latex())  # "x"

# Greek letters supported
alpha = tm.Symbol(s="α")
print(alpha.latex())  # "α"
```

#### Decimal
```python
# Clean decimal formatting (period separator, no unnecessary decimals)
d1 = tm.Decimal(x=3.14)
print(d1.latex())  # "3.14"

# Whole numbers without decimal points
d2 = tm.Decimal(x=5.0)
print(d2.latex())  # "5" (not "5.0")

# Fraction-based decimals
d3 = tm.Decimal(p=5, q=2)  # 5/2 = 2.5
print(d3.latex())  # "2.5"
```

#### Infinity
```python
inf = tm.Inf()
print(inf.latex())  # "\\infty"
print(inf.sympy_expr.is_infinite)  # True
```

#### Pi (π) - NEW in v0.0.12!
```python
# Mathematical constant pi
pi = tm.Pi()
print(pi.latex())  # "\\pi"
print(pi.eval())   # 3.141592653589793

# Integer coefficients
two_pi = tm.Integer(n=2) * pi
print(two_pi.simplified().latex())  # "2\\pi"

# Fractional coefficients  
half_pi = tm.Fraction(p=1, q=2) * pi
print(half_pi.simplified().latex())  # "\\dfrac{1}{2}\\pi"

# Decimal coefficients
decimal_pi = tm.Decimal(x=0.75) * pi
print(decimal_pi.simplified().latex())  # "0.75\\pi"

# Negative coefficients (special handling)
neg_pi = tm.Integer(n=-1) * pi
print(neg_pi.simplified().latex())  # "-\\pi" (not "-1\\pi")

# Perfect for geometric formulas
r = tm.Symbol(s="r")
h = tm.Symbol(s="h")

# Circle area: A = πr²
area = pi * r**tm.Integer(n=2)
print(area.simplified().latex())  # "\\pir^{2}"

# Circle circumference: C = 2πr
circumference = tm.Integer(n=2) * pi * r
print(circumference.simplified().latex())  # "2\\pir"

# Cylinder volume: V = πr²h
cylinder = pi * r**tm.Integer(n=2) * h
print(cylinder.simplified().latex())  # "\\pir^{2}h"

# Cone volume: V = (1/3)πr²h
cone = tm.Fraction(p=1, q=3) * pi * r**tm.Integer(n=2) * h
print(cone.simplified().latex())  # "\\dfrac{1}{3}\\pir^{2}h"

# Sphere volume: V = (4/3)πr³
sphere = tm.Fraction(p=4, q=3) * pi * r**tm.Integer(n=3)
print(sphere.simplified().latex())  # "\\dfrac{4}{3}\\pir^{3}"

# Addition operations
pi_plus_one = pi + tm.Integer(n=1)
print(pi_plus_one.simplified().latex())  # "\\pi + 1"
```

### Binary Operators

#### Addition & Subtraction
```python
x = tm.Symbol(s="x")
y = tm.Symbol(s="y")

# Addition
expr = x + y
print(expr.latex())  # "x + y"

# Automatic subtraction formatting
neg_expr = x + tm.Integer(n=-5)
print(neg_expr.latex())  # "x -5"
```

#### Multiplication
```python
# Coefficient notation
coeff = tm.Integer(n=3) * x
print(coeff.latex())  # "3x"

# Explicit multiplication
explicit = tm.Integer(n=2) * tm.Integer(n=5)
print(explicit.latex())  # "2 \\times 5"

# Decimal coefficients with functions - NEW in v0.0.11!
n = tm.Symbol(s="n")
v = tm.Function(name="V")
decimal_coeff = tm.Decimal(p=1, q=2)  # 0.5
function_app = v(n)  # V(n)

# Decimal * Function multiplication
result = decimal_coeff * function_app
print(result.simplified().latex())  # "0.5V(n)"

# Commutative property works correctly
result_commute = function_app * decimal_coeff  
print(result_commute.simplified().latex())  # "0.5V(n)" (coefficient first)

# Various decimal forms supported
float_decimal = tm.Decimal(x=0.75)
print((float_decimal * function_app).simplified().latex())  # "0.75V(n)"

# Works with complex function arguments
complex_arg = x + tm.Integer(n=1)  # x + 1
f = tm.Function(name="f")
print((decimal_coeff * f(complex_arg)).simplified().latex())  # "0.5f(x + 1)"
```

#### Fractions
```python
# Display fractions with \dfrac
frac = tm.Fraction(p=1, q=2)
print(frac.latex())  # "\\dfrac{1}{2}"

# Negative fraction handling
neg_frac = tm.Fraction(p=-3, q=4)
print(neg_frac.latex())  # "-\\dfrac{3}{4}"

# Complex fractions
x = tm.Symbol(s="x")
y = tm.Symbol(s="y")
complex_frac = (x + y) / tm.Integer(n=2)
print(complex_frac.latex())  # "\\dfrac{x + y}{2}"
```

#### Powers
```python
# Simple exponentiation
power = x ** tm.Integer(n=3)
print(power.latex())  # "x^{3}"

# Complex base with parentheses
complex_base = (x + tm.Integer(n=1)) ** tm.Integer(n=2)
print(complex_base.latex())  # "\\left(x + 1\\right)^{2}"
```

### Relations & Sets

#### Equations & Inequalities
```python
# Equality
eq = tm.Equality(l=x, r=tm.Integer(n=5))
print(eq.latex())  # "x = 5"

# Inequality  
ineq = tm.StrictGreaterThan(l=x, r=tm.Integer(n=0))
print(ineq.latex())  # "x > 0"
```

#### Intervals
```python
# Closed interval [0, 5]
interval = tm.Interval(
    l=tm.Integer(n=0), 
    r=tm.Integer(n=5)
)
print(interval.latex())  # "\\lbracket 0; 5\\rbracket"

# Open interval (0, 1)
open_interval = tm.Interval(
    l=tm.Integer(n=0),
    r=tm.Integer(n=1), 
    left_open=True,
    right_open=True
)
```

### Collections & Functions

#### Mathematical Collections
```python
# Tuples and sets
coll = tm.MathsCollection(elements=[x, y, tm.Integer(n=1)])
print(coll.latex())  # "\\left(x, y, 1\\right)"
```

#### Function Applications
```python
# Function definition
f = tm.Function(name="f")
print(f.latex())  # "f"

# Function application f(x)
fx = f(x)
print(fx.latex())  # "f(x)"

# Multi-argument functions f(x, y)
fxy = f(tm.MathsCollection(elements=[x, y]))
print(fxy.latex())  # "f(\\left(x, y\\right))"

# NEW in v0.0.11: Decimal coefficients with functions
decimal_coeff = tm.Decimal(p=3, q=4)  # 0.75
result = decimal_coeff * fx  # 0.75 * f(x)
print(result.simplified().latex())  # "0.75f(x)"

# Perfect for modeling scenarios like exponential decay
# V(n+1) = 0.5 * V(n) where volume decreases by 50% each period
n = tm.Symbol(s="n")
v = tm.Function(name="V")
decay_rate = tm.Decimal(p=1, q=2)  # 50% = 0.5
decay_formula = decay_rate * v(n)
print(decay_formula.simplified().latex())  # "0.5V(n)"
```

## 🔍 Complete Mathematical Object Reference

Here's a comprehensive breakdown of the `Fraction` class, demonstrating all features available in PCA Teachers mathematical objects:

### Fraction Class - Full API Reference

```python
class Fraction(MathsObject):
    """Represents mathematical fractions with automatic simplification and validation."""
```

#### Attributes

```python
# Core attributes
p: MathsObject          # Numerator (any MathsObject)
q: MathsObject          # Denominator (any MathsObject, cannot be zero)
sympy_expr: sp.Expr     # Automatically computed SymPy expression

# Inherited from MathsObject
__match_args__ = ("p", "q")  # Enable pattern matching
```

#### Construction Methods

```python
# From integers
frac1 = tm.Fraction(p=3, q=4)
frac2 = tm.Fraction(p=tm.Integer(n=3), q=tm.Integer(n=4))

# From other MathsObjects
x = tm.Symbol(s="x")
y = tm.Symbol(s="y")
symbolic_frac = tm.Fraction(p=x, q=y)

# From expressions
complex_frac = tm.Fraction(
    p=tm.Add(l=x, r=tm.Integer(n=1)),
    q=tm.Mul(l=y, r=tm.Integer(n=2))
)
```

#### Validation System

```python
# Field validators (automatic type conversion)
@field_validator("p", mode="before")
@classmethod
def format_numerator(cls, value: int | Integer) -> Integer:
    """Converts int to Integer, validates MathsObject types"""

@field_validator("q", mode="before")  
@classmethod
def format_denominator(cls, value: int | Integer) -> Integer:
    """Prevents zero denominators, converts int to Integer"""

# Model validator (SymPy integration)
@model_validator(mode="before")
@classmethod
def compute_sympy_expr(cls, data: Dict[str, Any]) -> Dict[str, Any]:
    """Automatically computes SymPy expression from p and q"""
```

#### Core Methods

```python
# String representation
def __repr__(self) -> str:
    return f"Fraction(p={repr(self.p)}, q={repr(self.q)})"

def __str__(self) -> str:
    return repr(self)

# Mathematical operations
def latex(self) -> str:
    """
    Generate LaTeX representation with proper negative handling:
    - Fraction(p=3, q=4).latex() → "\\dfrac{3}{4}"
    - Fraction(p=-3, q=4).latex() → "-\\dfrac{3}{4}"
    """

def eval(self) -> float:
    """Numerical evaluation: p.eval() / q.eval()"""

def simplified(self) -> 'Fraction':
    """
    Mathematical simplification with multiple cases:
    - GCD reduction for integer fractions
    - Identity simplification (x/1 → x)
    - Sign normalization (negative denominators)
    - Nested fraction handling
    """
```

#### Properties

```python
@property
def as_decimal(self) -> Decimal:
    """Convert to Decimal representation"""
    return Decimal(p=self.p.eval(), q=self.q.eval())

@property  
def as_percent(self) -> Integer | Decimal:
    """Convert to percentage (multiply by 100)"""
    x = 100 * self.eval()
    if x.is_integer():
        return Integer(n=int(x))
    else:
        return Decimal(x=x)

@property
def sympy_expr_data(self) -> Dict[str, Any]:
    """Serialized SymPy expression data for JSON compatibility"""
```

#### Operator Overloading (Inherited from MathsObject)

```python
# Arithmetic operators
frac + other    # → Add(l=frac, r=other)
frac - other    # → Add(l=frac, r=-other)  
frac * other    # → Mul(l=frac, r=other)
frac / other    # → Fraction(p=frac, q=other)
frac ** other   # → Pow(base=frac, exp=other)
-frac          # → Mul(l=Integer(n=-1), r=frac)

# Comparison operators  
frac > other    # → StrictGreaterThan(l=frac, r=other)
frac < other    # → StrictGreaterThan(l=other, r=frac)
```

#### Simplification Rules

The `simplified()` method handles numerous mathematical cases:

```python
# Identity rules
Fraction(p=x, q=1).simplified()           # → x
Fraction(p=x, q=-1).simplified()          # → -x

# Integer fraction reduction
Fraction(p=6, q=8).simplified()           # → Fraction(p=3, q=4)

# Sign normalization  
Fraction(p=3, q=-4).simplified()          # → Fraction(p=-3, q=4)

# Nested fractions
Fraction(p=Integer(n=2), q=Fraction(p=1, q=3)).simplified()  
# → Fraction(p=6, q=1) → Integer(n=6)

# Complex expressions
Fraction(
    p=Add(l=x, r=y), 
    q=Add(l=x, r=Integer(n=1))
).simplified()  # → Fraction(p=Add(...), q=Add(...)) [preserved]
```

#### SymPy Integration

```python
# Automatic SymPy expression computation
frac = Fraction(p=3, q=4)
print(frac.sympy_expr)  # sp.Rational(3, 4)

# Complex expression handling
complex_frac = Fraction(p=x, q=y)  
print(complex_frac.sympy_expr)  # sp.Mul(x, sp.Pow(y, -1))

# Serialization support
print(frac.sympy_expr_data)
# {
#   "type": "Rational", 
#   "sp.srepr": "Rational(3, 4)",
#   "str": "3/4"
# }
```

#### Usage Examples

```python
import teachers.maths as tm

# Basic fraction
half = tm.Fraction(p=1, q=2)
print(half.latex())        # "\\dfrac{1}{2}"
print(half.eval())         # 0.5
print(half.as_percent)     # Integer(n=50)

# Symbolic fraction
x, y = tm.Symbol(s="x"), tm.Symbol(s="y")
symbolic = tm.Fraction(p=x, q=y)
print(symbolic.latex())    # "\\dfrac{x}{y}"

# Complex fraction with simplification
complex_frac = tm.Fraction(
    p=tm.Add(l=x, r=tm.Integer(n=1)),
    q=tm.Integer(n=2)
)
print(complex_frac.latex())  # "\\dfrac{x + 1}{2}"

# Automatic reduction
reducible = tm.Fraction(p=6, q=8)
simplified = reducible.simplified()
print(simplified.latex())   # "\\dfrac{3}{4}"

# Negative handling
negative = tm.Fraction(p=-3, q=4)
print(negative.latex())     # "-\\dfrac{3}{4}"
```

#### Concrete Example: Building 1/(1+x) Step by Step

```python
import teachers.maths as tm

# Step 1: Create the variable x
x = tm.Symbol(s="x")
print(f"x = {x}")                    # Symbol(s='x')
print(f"x.latex() = {x.latex()}")    # "x"

# Step 2: Create the constant 1
one = tm.Integer(n=1)
print(f"one = {one}")                # Integer(n=1)
print(f"one.latex() = {one.latex()}")# "1"

# Step 3: Build the expression (1 + x) for the denominator
denominator = one + x  # This creates Add(l=Integer(n=1), r=Symbol(s='x'))
print(f"denominator = {denominator}")              # Add(l=Integer(n=1), r=Symbol(s='x'))
print(f"denominator.latex() = {denominator.latex()}")  # "1 + x"

# Step 4: Create the complete fraction 1/(1+x)
fraction = tm.Fraction(p=one, q=denominator)
print(f"fraction = {fraction}")
# Fraction(p=Integer(n=1), q=Add(l=Integer(n=1), r=Symbol(s='x')))

print(f"fraction.latex() = {fraction.latex()}")
# "\\dfrac{1}{1 + x}"

# Step 5: Work with the SymPy expression
print(f"fraction.sympy_expr = {fraction.sympy_expr}")
# 1/(x + 1)

# Step 5.5: Inspect the sympy_expr_data property
print(f"fraction.sympy_expr_data = {fraction.sympy_expr_data}")
# {
#   'type': 'Mul', 
#   'sp.srepr': 'Mul(Integer(1), Pow(Add(Integer(1), Symbol(\'x\')), Integer(-1)), evaluate=False)', 
#   'str': '1/(x + 1)'
# }

# Compare with a simple integer fraction
simple_frac = tm.Fraction(p=3, q=4)
print(f"simple_frac.sympy_expr_data = {simple_frac.sympy_expr_data}")
# {
#   'type': 'Rational', 
#   'sp.srepr': 'Rational(3, 4)', 
#   'str': '3/4'
# }

# Step 6: Simplification (no change for this case)
simplified = fraction.simplified()
print(f"simplified.latex() = {simplified.latex()}")
# "\\dfrac{1}{1 + x}"

# Step 7: Substitute a numerical value
# When x = 2, the fraction becomes 1/3
x_value = 2
numerical_result = fraction.sympy_expr.subs(x.sympy_expr, x_value)
print(f"When x = {x_value}: {numerical_result}")  # 1/3
print(f"Numerical value: {float(numerical_result)}")  # 0.3333...

# Step 8: Build more complex expressions with this fraction
# Example: 2 * (1/(1+x)) + 3
coefficient = tm.Integer(n=2)
constant = tm.Integer(n=3)
complex_expr = coefficient * fraction + constant
print(f"2 * (1/(1+x)) + 3 = {complex_expr.latex()}")
# Result: "2\\dfrac{1}{1 + x} + 3"
```

#### Real-World Educational Example

```python
# Teacher creates an exercise: "Simplify the expression 6/(2+4x)"
x = tm.Symbol(s="x")
numerator = tm.Integer(n=6)
denominator = tm.Integer(n=2) + tm.Integer(n=4) * x  # 2 + 4x

exercise_fraction = tm.Fraction(p=numerator, q=denominator)
print(f"Original: {exercise_fraction.latex()}")
# "\\dfrac{6}{2 + 4x}"

# Expected student answer after factoring: 3/(1+2x)
expected_num = tm.Integer(n=3)
expected_denom = tm.Integer(n=1) + tm.Integer(n=2) * x  # 1 + 2x
expected_answer = tm.Fraction(p=expected_num, q=expected_denom)
print(f"Expected: {expected_answer.latex()}")
# "\\dfrac{3}{1 + 2x}"

# Verify mathematical equivalence using SymPy
diff = exercise_fraction.sympy_expr - expected_answer.sympy_expr
simplified_diff = diff.simplify()
print(f"Are they equivalent? {simplified_diff == 0}")  # True
```

#### Error Handling

```python
# Zero denominator prevention
try:
    tm.Fraction(p=1, q=0)
except ValueError as e:
    print(e)  # "Denominator cannot be zero"

# Type validation
try:
    tm.Fraction(p="invalid", q=2)
except ValidationError as e:
    print(e)  # Pydantic validation error
```

This example demonstrates the full lifecycle of a PCA Teachers mathematical object, from construction through validation, computation, simplification, and LaTeX generation. All other mathematical objects follow similar patterns with their own specialized logic.

## 📝 LaTeX Generation

All mathematical objects generate clean, properly formatted LaTeX:

### Key Features

- **Proper Escaping**: No double-backslash issues
- **Context-Aware Parentheses**: Automatic grouping based on precedence
- **Educational Standards**: French mathematical notation compliance
- **Unicode Support**: Greek letters and special symbols

### Examples

```python
# Complex expression with proper formatting
x = tm.Symbol(s="x")
y = tm.Symbol(s="y") 
z = tm.Symbol(s="z")

complex_expr = ((x + y) ** tm.Integer(n=2)) / (z - tm.Integer(n=1))
print(complex_expr.latex())
# Output: "\\dfrac{\\left(x + y\\right)^{2}}{z -1}"
```

### LaTeX Output Quality

✅ **Clean Output**: `\dfrac{1}{2}` not `\\\\dfrac\\{1\\}\\{2\\}`  
✅ **Proper Braces**: `x^{3}` not `x^\\{3\\}`  
✅ **Smart Parentheses**: `\left(x + y\right)^{2}`  
✅ **Consistent Spacing**: `\lbracket 0; 5\rbracket`  
✅ **Clean Decimals**: `5` not `5.0`, `3.14` not `3,14`  
✅ **International Format**: Period decimal separator for global compatibility

## 🎯 Correction System

Automated validation of student mathematical input with detailed feedback.

### Workflow

```python
from teachers.corrector import correct

# Teacher's expected answer
teacher_answer = tm.Fraction(p=3, q=4)

# Student's input (from MathLive editor)
user_input = "\\frac{3}{4}"

# Automatic correction
result = correct(user_input, teacher_answer)
print(result.is_correct)  # True
print(result.feedback)    # Detailed feedback message
```

### Correction Features

- **MathLive Integration**: Cleans MathLive-specific formatting
- **LaTeX Parsing**: Converts student LaTeX to mathematical objects
- **Mathematical Equivalence**: Compares simplified expressions
- **Detailed Feedback**: Educational guidance for incorrect answers
- **Error Handling**: Graceful handling of invalid input

### Example Corrections

```python
# Perfect match
correct("\\frac{3}{4}", Fraction(p=3, q=4))  # ✅ Correct

# Mathematically equivalent
correct("\\frac{6}{8}", Fraction(p=3, q=4))   # ✅ Correct (simplifies to 3/4)

# Wrong answer with feedback
correct("\\frac{1}{2}", Fraction(p=3, q=4))   # ❌ Wrong (with explanation)
```

## 🧪 Testing

Comprehensive test suite ensuring reliability:

```bash
# Run all tests
python -m unittest

# Run specific test modules
python -m unittest tests.test_maths_objects
python -m unittest tests.test_corrector  
python -m unittest tests.test_latex_output
```

### Test Coverage

- **122 tests total** with **100% pass rate**
- **Unit tests**: Individual object behavior
- **Integration tests**: Cross-object interactions  
- **LaTeX tests**: Output formatting validation
- **Correction tests**: End-to-end workflows
- **Edge case tests**: Boundary conditions and error handling

### Test Categories

```
tests/
├── test_maths_objects.py     # Core mathematical object tests
├── test_corrector.py         # Correction pipeline tests
├── test_latex_output.py      # LaTeX generation tests  
├── test_eval_methods.py      # Numerical evaluation tests
├── test_interval.py          # Interval-specific tests
├── test_inf.py              # Infinity behavior tests
├── test_generator.py        # Content generation tests
├── test_formatting.py       # Educational formatting tests
├── test_complex_operations.py  # Multi-object interactions
├── test_deserialization_from_sympy.py  # SymPy conversion tests
└── test_deserialization_from_formal.py # Parser tests
```

## 🤝 Contributing

### Development Setup

```bash
# Setup development environment
git clone <repository>
cd pca-teachers
python -m venv env
source env/bin/activate
pip install -e .

# Run tests
python -m unittest
```

### Code Standards

- **Type Hints**: All functions must include type annotations
- **Docstrings**: Comprehensive documentation for all public methods
- **Pydantic Models**: Use for all data structures requiring validation
- **SymPy Integration**: Maintain consistency with SymPy mathematical semantics
- **Test Coverage**: New features require comprehensive test coverage

### Adding New Mathematical Objects

1. **Inherit from MathsObject**: Use the base class framework
2. **Implement Required Methods**: `latex()`, `simplified()`, `eval()`
3. **Add SymPy Integration**: Include `@model_validator` for SymPy expression
4. **Write Comprehensive Tests**: Cover creation, operations, and edge cases
5. **Update Documentation**: Add to this README and include examples

### Mathematical Accuracy

- **SymPy Consistency**: Ensure behavior matches SymPy semantics  
- **Educational Standards**: Follow French mathematical notation conventions
- **Precision Handling**: Proper decimal and fraction representation
- **Unicode Support**: Handle Greek letters and mathematical symbols

## 📄 License

See `LICENSE` file for details.

## 🔗 Dependencies

- [SymPy](https://www.sympy.org/) - Symbolic mathematics library
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation framework  
- [ANTLR4](https://www.antlr.org/) - Parser generator for LaTeX processing

---

**Built for educational excellence in mathematical content creation** 🎓
