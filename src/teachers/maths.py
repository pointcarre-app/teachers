import ast
import sys
from typing import Any, Dict, Optional

# import antlr4  # noqa F401

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
    field_serializer,
    model_validator,
    ValidationError,
)

import sympy as sp
from sympy.ntheory import primefactors
from sympy.parsing.latex import parse_latex as sympy_parse_latex

##################################################
# BASE CLASS
##################################################


class MathsObject(BaseModel):
    # TODO: Mixin ABC
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sympy_expr: sp.Basic

    def __repr__(self):
        return f"|SYMPY:{sp.srepr(self.sympy_expr)}:SYMPY|>"

    def __str__(self):
        raise NotImplementedError(f"__str__ for {self.__class__.__name__}")

    @property
    def sympy_expr_data(self) -> Dict[str, Any]:
        """Returns the sympy expression as a serialized dict."""
        return self.serialize_sympy_expr_data(self.sympy_expr)

    @field_serializer("sympy_expr")
    def serialize_sympy_expr_data(self, value: sp.Basic) -> Dict[str, Any]:
        # This serializes any sympy expression to a JSON-compatible format
        return {"type": value.__class__.__name__, "sp.srepr": sp.srepr(value), "str": str(value)}

    # NOTE: the dunder methods are used for simplicity to write exercices
    # they are not intended to do anythin that building the corresponding tree and
    # do not resolve anything

    def __neg__(self):
        match self:
            case Integer(n):
                return Integer(n=-n)
            case Mul(Integer(n=-1), r1):
                return r1
            case _:
                return Mul(l=Integer(n=-1), r=self)

    def __add__(self, other):
        return Add(l=self, r=other)

    def __sub__(self, other):
        return Add(l=self, r=-other)

    def __mul__(self, other):
        return Mul(l=self, r=other)

    def __truediv__(self, other):
        return Fraction(p=self, q=other)

    def __pow__(self, other):
        return Pow(base=self, exp=other)

    def __gt__(self, other):
        return StrictGreaterThan(l=self, r=other)

    def __lt__(self, other):
        return StrictGreaterThan(l=other, r=self)

    # def __eq__(self, other):
    #     return Equality(l=self, r=other)

    def simplified(self):
        raise NotImplementedError(f"Simplified of {self.__class__.__name__}")

    def latex(self):
        raise NotImplementedError(f"Latex of {self.__class__.__name__}")

    def eval(self):
        raise NotImplementedError(f"Eval of {self.__class__.__name__}")

    # TODO
    # @property
    # def raise_not_implemented_simplification(self, data):
    #     raise NotImplementedError(f"{__class}({type(data['p'])=},{type(data['q'])=})\n{data['p']=}\n{data['q']=}")


class MathsCollection(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    elements: list[MathsObject]
    sympy_expr: sp.Basic

    @model_validator(mode="before")
    @classmethod
    def compute_sympy_expr(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        # Create a sympy Tuple from the elements' sympy expressions
        # First check if all elements are valid MathsObjects
        elements = data.get("elements", [])

        # Validate that all elements have sympy_expr attribute (are MathsObjects)
        for elem in elements:
            if not hasattr(elem, "sympy_expr"):
                raise ValueError(f"All elements must be MathsObject instances, got {type(elem)}")

        sympy_elements = [elem.sympy_expr for elem in elements]
        data["sympy_expr"] = sp.Tuple(*sympy_elements)
        return data

    @property
    def sympy_expr_data(self) -> Dict[str, Any]:
        """Returns the sympy expression as a serialized dict."""
        return self.serialize_sympy_expr_data(self.sympy_expr)

    @field_serializer("sympy_expr")
    def serialize_sympy_expr_data(self, value: sp.Basic) -> Dict[str, Any]:
        # This serializes any sympy expression to a JSON-compatible format
        return {"type": value.__class__.__name__, "sp.srepr": sp.srepr(value), "str": str(value)}

    def __repr__(self):
        return "(" + ", ".join(repr(x) for x in self.elements) + ")"

    def __str__(self):
        return repr(self)

    def __getitem__(self, i: int):
        return self.elements[i]

    def latex(self):
        return "\\left(" + ", ".join(elem.latex() for elem in self.elements) + "\\right)"

    def simplified(self) -> "MathsCollection":
        return MathsCollection(elements=[elem.simplified() for elem in self.elements])


class Function(BaseModel):
    # NOTE: this is not a maths object per se as it would break liskov (see test_maths)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    sympy_expr: sp.FunctionClass

    @model_validator(mode="before")
    @classmethod
    def compute_sympy_expr(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if data["name"] == "":
            raise ValidationError("Symbol name cannot be an empty string", [])
        data["sympy_expr"] = sp.Function(data["name"])
        return data

    def __repr__(self):
        return f"Function(name={self.name})"

    def __call__(self, *args):
        # sympy_args = (x.sympy_expr for x in args)
        # sympy_expr = self.sympy_expr(*sympy_args)
        if len(args) == 1:
            args = args[0]
        else:
            args = MathsCollection(args)
        return Image(f=self, pre=args)
        # return Image(f=self, pre=args, sympy_expr=sympy_expr)
        # return sp.Function(self.name)(*args)

    def latex(self):
        return self.name


##################################################
# ATOMS
##################################################


class Symbol(MathsObject):
    s: str
    sympy_expr: sp.Symbol

    __match_args__ = ("s",)

    @model_validator(mode="before")
    @classmethod
    def compute_sympy_expr(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if data["s"] == "":
            raise ValidationError("Symbol name cannot be an empty string", [])
        data["sympy_expr"] = sp.Symbol(data["s"])
        return data

    def __repr__(self):
        return f"Symbol(s='{self.s}')"

    def __str__(self):
        return repr(self)

    def latex(self):
        return self.s

    def simplified(self):
        return self


class Integer(MathsObject):
    n: int
    sympy_expr: sp.Integer

    __match_args__ = ("n",)

    # @field_validator('n', mode="before")
    # @classmethod
    # def format_n(cls, value: int) -> int:
    #     if value < 0:
    #         raise ValueError("Negative integers are not allowed")
    #     return value

    @model_validator(mode="before")
    @classmethod
    def compute_sympy_expr(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["sympy_expr"] = sp.Integer(data["n"])
        return data

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"Integer(n={self.n})"

    def latex(self):
        return str(self.n)

    def eval(self):
        return self.n

    def simplified(self):
        return self

    @property
    def as_decimal(self):
        return Decimal(x=float(self.n))

    @property
    def as_percent(self):
        x = 100 * self.n
        return Integer(n=x)

    @property
    def primefactors(self):
        return primefactors(self.n)


class Decimal(MathsObject):
    p: Optional[int] = None
    q: Optional[int] = None
    x: Optional[float] = None

    __match_args__ = ("p", "q", "x")

    sympy_expr: sp.Rational

    @model_validator(mode="before")
    @classmethod
    def compute_sympy_expr(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        has_p = "p" in data and data["p"] is not None
        has_q = "q" in data and data["q"] is not None
        has_x = "x" in data and data["x"] is not None

        if has_p and has_q and has_x:
            raise ValueError("Must provide either 'x' OR 'p' and 'q'")
        elif has_p and has_q:
            data["sympy_expr"] = sp.Rational(data["p"], data["q"])
        elif has_x:
            data["sympy_expr"] = sp.Rational(data["x"])
        else:
            raise ValueError("Must provide either 'x' OR 'p' and 'q'")
        return data

    def __str__(self):
        return repr(self)

    def __repr__(self):
        if self.x:
            return f"Decimal(x={self.x})"
        else:
            return f"Decimal(p={self.p}, q={self.q})"

    def latex(self):
        value = self.eval()
        # Check if it's a whole number
        if value.is_integer():
            return str(int(value))
        else:
            # Use period as decimal separator, not comma
            return str(value)

    def eval(self):
        if self.x is not None:
            return self.x
        else:
            return self.p / self.q

    def simplified(self):
        return self

    def round(self, n_digits):
        return Decimal(x=round(self.eval(), n_digits))


class Image(MathsObject):
    f: Function
    pre: MathsObject | MathsCollection

    __match_args__ = ("f", "pre")

    @model_validator(mode="before")
    @classmethod
    def compute_sympy_expr(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        # if not data["sympy_expr"]:

        if isinstance(data["pre"], MathsCollection):
            sympy_args = (x.sympy_expr for x in data["pre"].elements)
            data["sympy_expr"] = data["f"].sympy_expr(*sympy_args)
        else:
            data["sympy_expr"] = data["f"].sympy_expr(data["pre"].sympy_expr)
        # data["sympy_expr"] = data["f"].sympy_expr(data["pre"].sympy_expr)
        return data

    def __repr__(self):
        return f"{repr(self.f)}({repr(self.pre)})"

    def __str__(self):
        return repr(self)

    def latex(self):
        return f"{self.f.latex()}({self.pre.latex()})"

    def simplified(self):
        return Image(f=self.f, pre=self.pre.simplified())


class Inf(MathsObject):
    sympy_expr: sp.Basic = sp.oo

    def latex(self):
        return "\\infty"

    def simplified(self):
        return self

    def __repr__(self):
        return "Inf()"


class Pi(MathsObject):
    sympy_expr: sp.Basic = sp.pi

    def latex(self):
        return "\\pi"

    def eval(self) -> float:
        return float(sp.pi)

    def simplified(self):
        return self

    def __repr__(self):
        return "Pi()"

    def __str__(self):
        return repr(self)


##################################################
# BINARY OPERATORS
##################################################


class Add(MathsObject):
    # NOTE: l/r stand for left/right

    l: MathsObject
    r: MathsObject
    sympy_expr: sp.Add

    __match_args__ = (
        "l",
        "r",
    )

    @model_validator(mode="before")
    @classmethod
    def compute_sympy_expr(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["sympy_expr"] = sp.Add(data["l"].sympy_expr, data["r"].sympy_expr, evaluate=False)
        return data

    def __repr__(self):
        return f"Add(l={repr(self.l)}, r={repr(self.r)})"

    def __str__(self):
        return repr(self)

    def _is_complex_expression(self, expr):
        """Check if an expression is complex enough to need parentheses when negated."""
        return isinstance(expr, (Add, Fraction)) or (
            isinstance(expr, Mul) and not (isinstance(expr.l, Integer) and expr.l.n == -1)
        )

    def latex(self):
        left = self.l.latex()

        # Handle the case where right operand is Mul(Integer(-1), complex_expr)
        # This prevents double minus issues like "x --5"
        match self.r:
            case Mul(Integer(n=-1), inner_expr) if self._is_complex_expression(inner_expr):
                # For negative complex expressions, use parentheses: "x - (complex_expr)"
                inner_latex = inner_expr.latex()
                return f"{left} - \\left({inner_latex}\\right)"
            case _:
                # Default behavior
                right = self.r.latex()
                if right.startswith("-"):
                    return f"{left} {right}"
                else:
                    return f"{left} + {right}"

    def eval(self):
        return self.l.eval() + self.r.eval()

    def simplified(self):
        l, r = self.l.simplified(), self.r.simplified()

        match l, r:
            # Identity: x + 0 = x
            case (x, Integer(0)) | (Integer(0), x):
                return x

            # Basic rules
            case Integer(n1), Integer(n2):
                return Integer(n=n1 + n2)
            case Fraction(p1, q1), Fraction(p2, q2):
                return Fraction(p=p1 * q2 + p2 * q1, q=q1 * q2).simplified()
            case (Fraction(p, q), Integer(n)) | (Integer(n), Fraction(p, q)):
                return Fraction(p=p + Integer(n=n) * q, q=q).simplified()

            # Integer + Decimal combinations
            case (Integer(n), Decimal(p, q, x)) | (Decimal(p, q, x), Integer(n)):
                if x is not None:
                    return Decimal(x=n + x)
                else:
                    return Decimal(x=n + (p / q))

            # Decimal + Fraction combinations
            case (Decimal(p1, q1, x1), Fraction(p2, q2)) | (Fraction(p2, q2), Decimal(p1, q1, x1)):
                if x1 is not None:
                    # Convert fraction to decimal and add
                    frac_decimal = p2.eval() / q2.eval()
                    return Decimal(x=x1 + frac_decimal)
                else:
                    # Convert both to decimal
                    dec_value = p1 / q1
                    frac_value = p2.eval() / q2.eval()
                    return Decimal(x=dec_value + frac_value)

            # Decimal + Decimal combinations
            case Decimal(p1, q1, x1), Decimal(p2, q2, x2):
                # Convert both to their decimal values and add
                val1 = x1 if x1 is not None else p1 / q1
                val2 = x2 if x2 is not None else p2 / q2
                return Decimal(x=val1 + val2)

            case Add(l, r), Decimal(p, q, x):
                if x:
                    return Add(l=l, r=Add(l=r, r=Decimal(x=x)))
                else:
                    return Add(l=l, r=Add(l=r, r=Decimal(p=p, q=q)))

            case Add(l, r), Integer(n):
                return Add(l=l, r=Add(l=r, r=Integer(n=n)))

            # Symbols
            case Symbol(s1), Symbol(s2) if s1 != s2:
                return Add(l=l, r=r)
            case (Symbol(_), Integer(_) | Decimal(_)) | (Integer(_) | Decimal(_), Symbol(_)):
                return Add(l=l, r=r)

            # Pi cases
            case (Pi(), Integer(_) | Decimal(_) | Fraction(_)) | (
                Integer(_) | Decimal(_) | Fraction(_),
                Pi(),
            ):
                return Add(l=l, r=r)

            # Do nothing
            case (Mul(_, _), Integer(_)) | (Integer(_), Mul(_, _)):
                return Add(l=l, r=r)
            case (Mul(_, _), Symbol(_)) | (Symbol(_), Mul(_, _)):
                return Add(l=l, r=r)
            case (Pow(_, _), Integer(_)) | (Integer(_), Pow(_, _)):
                return Add(l=l, r=r)
            case (Pow(_, _), Mul(_, _)) | (Mul(_, _), Pow(_, _)):
                return Add(l=l, r=r)
            case (Mul(_, _), Mul(_, _)):
                # Multiple multiplication terms - preserve as-is for now
                return Add(l=l, r=r)
            case _:
                # SymPy fallback for unhandled cases - Level 2 approach
                try:
                    # Let SymPy handle complex algebraic simplification
                    sympy_result = self.sympy_expr.expand().simplify()
                    return MathsObjectParser.from_sympy(sympy_result)
                except Exception:
                    # Ultimate fallback: preserve as-is if SymPy fails
                    return Add(l=l, r=r)


class Mul(MathsObject):
    # NOTE: l/r stand for left/right

    l: MathsObject
    r: MathsObject
    sympy_expr: sp.Mul

    __match_args__ = (
        "l",
        "r",
    )

    @model_validator(mode="before")
    @classmethod
    def compute_sympy_expr(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["sympy_expr"] = sp.Mul(data["l"].sympy_expr, data["r"].sympy_expr, evaluate=False)
        return data

    def __repr__(self):
        return f"Mul(l={repr(self.l)}, r={repr(self.r)})"

    def __str__(self):
        return repr(self)

    def latex(self):
        if self.l == Integer(n=-1):
            return "-" + self.r.latex()
        else:
            match self.l, self.r:
                # Coefficient × Variable should have no × symbol (e.g., 27x not 27×x)
                case Integer(_) | Decimal(_) | Fraction(_), Symbol(_):
                    # Special case: coefficient 1 should be omitted (1x → x)
                    if isinstance(self.l, Integer) and self.l.n == 1:
                        return self.r.latex()
                    else:
                        return self.l.latex() + self.r.latex()

                # Coefficient × Power should have no × symbol (e.g., 27x² not 27×x²)
                case Integer(_) | Decimal(_) | Fraction(_), Pow(_):
                    # Special case: coefficient 1 should be omitted (1x² → x²)
                    if isinstance(self.l, Integer) and self.l.n == 1:
                        return self.r.latex()
                    else:
                        return self.l.latex() + self.r.latex()

                # Number × Number should have × symbol (e.g., 3×4)
                case Integer(_) | Decimal(_), Integer(_) | Decimal():
                    return self.l.latex() + " \\times " + self.r.latex()

                # Fraction × Fraction should have × symbol
                case Fraction(_), Fraction(_):
                    return self.l.latex() + " \\times " + self.r.latex()

                # Complex expressions need parentheses and × symbol
                case Mul(_) | Add(_), Mul(_) | Add(_):
                    left, right = self.l.latex(), self.r.latex()
                    if isinstance(self.l, Add):
                        left = "\\left(" + left + "\\right)"
                    if isinstance(self.r, Add):
                        right = "\\left(" + right + "\\right)"
                    return left + " \\times " + right

                case Fraction(_) | Add(_), Fraction(_) | Add(_):
                    left, right = self.l.latex(), self.r.latex()
                    if isinstance(self.l, Add):
                        left = "\\left(" + left + "\\right)"
                    if isinstance(self.r, Add):
                        right = "\\left(" + right + "\\right)"
                    return left + " \\times " + right

                # Default: no × symbol for most cases (coefficient-like behavior)
                case _:
                    return self.l.latex() + self.r.latex()

    def eval(self):
        return self.l.eval() * self.r.eval()

    def simplified(self):
        l, r = self.l.simplified(), self.r.simplified()

        # raise Exception("GOTCHA")

        match l, r:
            case (Integer(1), x) | (x, Integer(1)):
                return x

            case (Integer(0), x) | (x, Integer(0)):
                return Integer(n=0)

            case Integer(n1), Integer(n2):
                return Integer(n=n1 * n2)

            case (Integer(n), Decimal(p, q, x)) | (Decimal(p, q, x), Integer(n)):
                if x:
                    return Decimal(x=n * x)
                else:
                    return Decimal(p=n * p, q=q)

            case (Integer(n), Fraction(p, q)) | (Fraction(p, q), Integer(n)):
                return Fraction(p=Integer(n=n) * p, q=q).simplified()

            case (Integer(n), Pow(base, exp)) | (Pow(base, exp), Integer(n)):
                return Mul(l=Integer(n=n), r=Pow(base=base, exp=exp))

            case Fraction(p1, q1), Fraction(p2, q2):
                return Fraction(p=p1 * p2, q=q1 * q2).simplified()

            case (Mul(l, Symbol(s)), Decimal(p, q, x)):
                # raise Exception("GOTCHA")
                if x:
                    return Mul(l=Mul(l=Decimal(x=x), r=l).simplified(), r=Symbol(s=s))
                else:
                    return Mul(l=Mul(l=Decimal(p=p, q=q), r=l).simplified(), r=Symbol(s=s))

                    # return Mul(l=l, r=Mul(l=r, r=Decimal(p=p, q=q)))

            case Symbol(s1), Symbol(s2) if s1 != s2:
                return Mul(l=l, r=r)

            case (Integer(n), Image(f, pre)) | (Image(f, pre), Integer(n)):
                return Mul(l=Integer(n=n), r=Image(f=f, pre=pre))

            case (Integer(n), Symbol(s)) | (Symbol(s), Integer(n)):
                return Mul(l=Integer(n=n), r=Symbol(s=s))

            case (Decimal(p, q, x), Image(f, pre)) | (Image(f, pre), Decimal(p, q, x)):
                return Mul(l=Decimal(p=p, q=q, x=x), r=Image(f=f, pre=pre))

            case (Integer(n), Pi()) | (Pi(), Integer(n)):
                return Mul(l=Integer(n=n), r=Pi())

            case (Decimal(p, q, x), Pi()) | (Pi(), Decimal(p, q, x)):
                return Mul(l=Decimal(p=p, q=q, x=x), r=Pi())

            case (Fraction(p, q), Pi()) | (Pi(), Fraction(p, q)):
                return Mul(l=Fraction(p=p, q=q), r=Pi())

            case (Pi(), Pow(base, exp)) | (Pow(base, exp), Pi()):
                return Mul(l=Pi(), r=Pow(base=base, exp=exp))

            case (Mul(mul_l, mul_r), Symbol(s)) | (Symbol(s), Mul(mul_l, mul_r)):
                # Handle Mul(Mul, Symbol) - distribute the symbol into the Mul
                return Mul(l=Mul(l=mul_l, r=mul_r), r=Symbol(s=s))

            case (Integer(n), Mul(mul_l, mul_r)):
                # Handle Integer * Mul - distribute the integer: n * (a * b) = (n * a) * b
                return Mul(l=Mul(l=Integer(n=n), r=mul_l).simplified(), r=mul_r).simplified()

            case (Mul(mul_l, mul_r), Integer(n)):
                # Handle Mul * Integer - distribute the integer: (a * b) * n = a * (b * n)
                return Mul(l=mul_l, r=Mul(l=mul_r, r=Integer(n=n)).simplified()).simplified()

            case (Mul(mul_l, mul_r), Pow(base, exp)) | (Pow(base, exp), Mul(mul_l, mul_r)):
                # Handle Mul * Pow - preserve both: (a * b) * x^n = (a * b) * x^n
                return Mul(l=Mul(l=mul_l, r=mul_r), r=Pow(base=base, exp=exp))

            # Polynomial multiplication: (a + b)(c + d) = ac + ad + bc + bd
            case Add(l1, r1), Add(l2, r2):
                # FOIL expansion for polynomial multiplication
                ac = (l1 * l2).simplified()
                ad = (l1 * r2).simplified()
                bc = (r1 * l2).simplified()
                bd = (r1 * r2).simplified()
                return (ac + ad + bc + bd).simplified()

            case _:
                # SymPy fallback for unhandled cases - Level 2 approach
                try:
                    # Let SymPy handle complex algebraic simplification
                    sympy_result = self.sympy_expr.expand().simplify()
                    return MathsObjectParser.from_sympy(sympy_result)
                except Exception:
                    # Ultimate fallback: preserve as-is if SymPy fails
                    return Mul(l=l, r=r)


class Fraction(MathsObject):
    p: MathsObject
    q: MathsObject
    sympy_expr: sp.Expr

    __match_args__ = (
        "p",
        "q",
    )

    @field_validator("p", mode="before")
    @classmethod
    def format_numerator(cls, value: int | Integer) -> Integer:
        if isinstance(value, int):
            return Integer(n=value)
        elif isinstance(value, MathsObject):
            return value
        else:
            raise NotImplementedError

    @field_validator("q", mode="before")
    @classmethod
    def format_denominator(cls, value: int | Integer) -> Integer:
        if isinstance(value, int):
            if value == 0:
                raise ValueError("Denominator cannot be zero")
            return Integer(n=value)
        elif isinstance(value, MathsObject):
            if isinstance(value, Integer):
                if value.n == 0:
                    raise ValueError("Denominator cannot be zero")
            return value
        else:
            raise NotImplementedError

    @model_validator(mode="before")
    @classmethod
    def compute_sympy_expr(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        match data["p"], data["q"]:
            case (int(p) | Integer(p), int(q) | Integer(q)):
                data["sympy_expr"] = sp.Rational(int(p), int(q))
            case (MathsObject(), MathsObject()):
                data["sympy_expr"] = sp.Mul(data["p"].sympy_expr, sp.Pow(data["q"].sympy_expr, -1))
            case _:
                raise NotImplementedError(
                    f"Fraction({type(data['p'])=},{type(data['q'])=})\n{data['p']=}\n{data['q']=}"
                )
        return data

    def __repr__(self):
        return f"Fraction(p={repr(self.p)}, q={repr(self.q)})"

    def __str__(self):
        return repr(self)

    def latex(self):
        # if tf.Formatting.DECIMAL_OR_INTEGER in formatting:
        #     val = self.eval()
        #     if val.is_integer():
        #         return str(int(val))
        #     else:
        #         return str(val)

        # elif tf.Formatting.PERCENT in formatting:
        #     val = 100 * self.eval()
        #     if val.is_integer():
        #         return str(int(val))
        #     else:
        #         return str(val)

        # elif tf.Formatting.FRACTION_OR_INTEGER in formatting:
        # NOTE: simplified is in charge of having minus above only
        if isinstance(self.p, Integer) and self.p.n < 0:
            return "-\\dfrac{" + (-self.p).latex() + "}{" + self.q.latex() + "}"
        else:
            return "\\dfrac{" + self.p.latex() + "}{" + self.q.latex() + "}"

        # else:
        #     raise NotImplementedError
        # return r"\\dfrac\{" + self.p.latex + r"\}\{" + self.q.latex + r"\}"

    def eval(self):
        return self.p.eval() / self.q.eval()

    def simplified(self):
        p = self.p.simplified()
        q = self.q.simplified()
        match p, q:
            case _, Integer(1):
                return p
            case _, Integer(n2) if n2 < 0:
                return Fraction(p=-p, q=-q).simplified()

            case Integer(n1), Integer(n2):
                gcd = int(sp.gcd(self.p.sympy_expr, self.q.sympy_expr))
                if gcd > 1:
                    p, q = int(n1 / gcd), int(n2 / gcd)
                    return Fraction(p=Integer(n=p), q=Integer(n=q)).simplified()
                else:
                    return Fraction(p=p, q=q)

            case Integer(n), Fraction(p, q):
                return Fraction(p=Integer(n=n * q.n), q=p).simplified()

            case Integer(n), Decimal(p, q, x):
                if x:
                    Decimal(x=n / x)
                else:
                    return Decimal(x=(n * q) / p)

            case Mul(l1, r1), Add(l2, r2):
                return Fraction(p=p, q=q)

            case Fraction(p1, q1), Fraction(p2, q2):
                return Fraction(p=p1 * q2, q=p2 * q1).simplified()

            case Add(add_l, add_r), Add(add_l2, add_r2):
                # Handle complex fractions with Add expressions - preserve as-is for now
                return Fraction(p=p, q=q)

            # Handle Symbol in numerator with various denominators
            case Symbol(s), Mul(l, r):
                # Symbol over multiplication - preserve as-is since it's already in simplest form
                return Fraction(p=p, q=q)

            case Symbol(s1), Symbol(s2):
                # Symbol over symbol - preserve as-is
                return Fraction(p=p, q=q)

            case Symbol(s), Pi():
                # Symbol over pi - preserve as-is
                return Fraction(p=p, q=q)

            case Symbol(s), Pow(base, exp):
                # Symbol over power - preserve as-is
                return Fraction(p=p, q=q)

            # Handle Mul in numerator with various denominators
            case Mul(l1, r1), Symbol(s):
                # Multiplication over symbol - preserve as-is
                return Fraction(p=p, q=q)

            case Mul(l1, r1), Mul(l2, r2):
                # Multiplication over multiplication - preserve as-is
                return Fraction(p=p, q=q)

            case Mul(l1, r1), Pi():
                # Multiplication over pi - preserve as-is
                return Fraction(p=p, q=q)

            case Mul(l1, r1), Pow(base, exp):
                # Multiplication over power - preserve as-is
                return Fraction(p=p, q=q)

            # Handle other combinations that should be preserved as-is
            case Pi(), Symbol(s):
                # Pi over symbol - preserve as-is
                return Fraction(p=p, q=q)

            case Pi(), Mul(l, r):
                # Pi over multiplication - preserve as-is
                return Fraction(p=p, q=q)

            case Pi(), Pi():
                # Pi over pi = 1
                return Integer(n=1)

            case Integer(n), Pi():
                # Integer over pi - preserve as-is
                return Fraction(p=p, q=q)

            case Pow(base1, exp1), Symbol(s):
                # Power over symbol - preserve as-is
                return Fraction(p=p, q=q)

            case Pow(base1, exp1), Mul(l, r):
                # Power over multiplication - preserve as-is
                return Fraction(p=p, q=q)

            case Pow(base1, exp1), Pow(base2, exp2):
                # Power over power - preserve as-is
                return Fraction(p=p, q=q)

            case _:
                # SymPy fallback for unhandled cases - Level 2 approach
                try:
                    # Let SymPy handle complex algebraic simplification
                    sympy_result = self.sympy_expr.simplify()
                    return MathsObjectParser.from_sympy(sympy_result)
                except Exception:
                    # Ultimate fallback: preserve as-is if SymPy fails
                    return Fraction(p=p, q=q)

    @property
    def as_decimal(self):
        return Decimal(p=self.p.eval(), q=self.q.eval())

    @property
    def as_percent(self):
        x = 100 * self.eval()
        if x.is_integer():
            return Integer(n=int(x))
        else:
            return Decimal(x=x)

    # def as_float(self):
    #     if isinstance(self.p, Integer) and isinstance(self.q, Integer):
    #         return self.p.n / self.q.n
    #     else:
    #         raise NotImplementedError(f"as_float for Fraction with members {type(self.p)} and {type(self.q)}")

    # @property
    # def as_percent(self):
    #     x = 100 * int(self.p) / int(self.q)
    #     if x.is_integer():
    #         return int(x)
    #     else:
    #         return x


class Pow(MathsObject):
    # NOTE: l/r stand for left/right

    base: MathsObject
    exp: MathsObject
    sympy_expr: sp.Pow

    __match_args__ = (
        "base",
        "exp",
    )

    @field_validator("base", mode="before")
    @classmethod
    def format_base(cls, value: int | MathsObject) -> MathsObject:
        if isinstance(value, int):
            return Integer(n=value)
        elif isinstance(value, MathsObject):
            return value
        else:
            raise NotImplementedError(f"Unsupported base type: {type(value)}")

    @field_validator("exp", mode="before")
    @classmethod
    def format_exp(cls, value: int | MathsObject) -> MathsObject:
        if isinstance(value, int):
            return Integer(n=value)
        elif isinstance(value, MathsObject):
            return value
        else:
            raise NotImplementedError(f"Unsupported exp type: {type(value)}")

    @model_validator(mode="before")
    @classmethod
    def compute_sympy_expr(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["sympy_expr"] = sp.Pow(data["base"].sympy_expr, data["exp"].sympy_expr, evaluate=False)
        return data

    def __repr__(self):
        return f"Pow(base={repr(self.base)}, exp={repr(self.exp)})"

    def __str__(self):
        return repr(self)

    def latex(self):
        # Special case: detect square root (exponent = 1/2)
        if (
            isinstance(self.exp, Fraction)
            and isinstance(self.exp.p, Integer)
            and self.exp.p.n == 1
            and isinstance(self.exp.q, Integer)
            and self.exp.q.n == 2
        ):
            base = self.base.latex()
            # For square roots, we don't need the outer parentheses that regular powers use
            return f"\\sqrt{{{base}}}"

        # Original logic for other exponents
        base = self.base.latex()
        if isinstance(self.base, (Add, Mul, Fraction)):
            base = "\\left(" + base + "\\right)"
        return base + "^{" + self.exp.latex() + "}"

    def eval(self):
        return self.base.eval() ** self.exp.eval()

    def simplified(self):
        base, exp = self.base.simplified(), self.exp.simplified()
        match base, exp:
            case (_, Integer(-1)):
                return Fraction(p=Integer(n=1), q=base)

            # Handle negative integer exponents (other than -1)
            case Integer(n1), Integer(n2) if n2 < 0:
                # Convert a^(-n) to 1/(a^n) as a Fraction
                return Fraction(p=Integer(n=1), q=Integer(n=n1 ** (-n2)))

            # Indeitité remarquables
            case Add(l, r), Integer(2):
                return l ** Integer(n=2) + (Integer(n=2) * l * r).simplified() + r ** Integer(n=2)

            # TODO: root
            case Mul(l, r), Fraction(p, q):
                return Pow(base=base, exp=exp)

            # Simplif for positive integer exponents
            case Integer(n1), Integer(n2):
                return Integer(n=n1**n2)
            case Integer(n), Fraction(Integer(p), Integer(q)):
                x = n ** (p / q)
                if x.is_integer():
                    return Integer(n=int(x))
                else:
                    return Pow(base=base, exp=exp)
            case Fraction(Integer(n1), Integer(n2)), Integer(n3):
                return Fraction(p=n1**n3, q=n2**n3)
            case Decimal(p, q, x), Integer(n):
                if x:
                    return Decimal(x=x**n)
                else:
                    return Decimal(p=p**n, q=q**n)

            # Do nothing
            case (Symbol(s), Integer(n)) | (Integer(n), Symbol(s)):
                return self
            case _:
                raise NotImplementedError(
                    f"Simplification of Pow of {type(base)} and {type(exp)}\n{base=}\n{exp=}"
                )


##################################################
# RELATIONS
##################################################


class Equality(MathsObject):
    sympy_expr: sp.Equality
    l: MathsObject
    r: MathsObject

    __match_args__ = (
        "l",
        "r",
    )

    def __repr__(self):
        return f"Equality(l={repr(self.l)}, r={repr(self.r)})"

    def __str__(self):
        return repr(self)

    @model_validator(mode="before")
    @classmethod
    def compute_sympy_expr(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["sympy_expr"] = sp.Equality(data["l"].sympy_expr, data["r"].sympy_expr, evaluate=False)
        return data

    def simplified(self):
        l, r = self.l.simplified(), self.r.simplified()
        return Equality(l=l, r=r)

    def latex(self):
        return f"{self.l.latex()} = {self.r.latex()}"


class StrictGreaterThan(MathsObject):
    sympy_expr: sp.StrictGreaterThan
    l: MathsObject
    r: MathsObject

    __match_args__ = (
        "l",
        "r",
    )

    def __repr__(self):
        return f"StrictGreaterThan(l={repr(self.l)}, r={repr(self.r)})"

    def __str__(self):
        return repr(self)

    @model_validator(mode="before")
    @classmethod
    def compute_sympy_expr(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["sympy_expr"] = sp.StrictGreaterThan(
            data["l"].sympy_expr, data["r"].sympy_expr, evaluate=False
        )
        return data

    def simplified(self):
        l, r = self.l.simplified(), self.r.simplified()
        return StrictGreaterThan(l=l, r=r)

    def latex(self):
        return f"{self.l.latex()} > {self.r.latex()}"


##################################################
# SETS
##################################################


class Interval(MathsObject):
    sympy_expr: sp.Interval
    left_open: Optional[bool] = False
    right_open: Optional[bool] = False
    l: MathsObject
    r: MathsObject

    __match_args__ = (
        "l",
        "r",
    )

    def __repr__(self):
        return f"Interval(l={repr(self.l)}, r={repr(self.r)}, left_open={self.left_open}, right_open={self.right_open})"

    def __str__(self):
        return repr(self)

    @model_validator(mode="before")
    @classmethod
    def compute_sympy_expr(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        # Provide defaults if missing (consistent with field defaults)
        left_open = data.get("left_open", False)
        right_open = data.get("right_open", False)

        data["sympy_expr"] = sp.Interval(
            data["l"].sympy_expr,
            data["r"].sympy_expr,
            left_open=left_open,
            right_open=right_open,
        )
        return data

    def simplified(self):
        l, r = self.l.simplified(), self.r.simplified()
        return Interval(l=l, r=r, left_open=self.left_open, right_open=self.right_open)

    def latex(self):
        return "\\lbracket " + self.l.latex() + "; " + self.r.latex() + "\\rbracket"


##################################################
# TERM GROUPING AND COLLECTION
##################################################


##################################################
# TERM GROUPING
##################################################


def group_terms(expr: MathsObject, symbol: Optional[Symbol] = None) -> MathsObject:
    """
    Group and collect like terms in a mathematical expression with proper polynomial ordering.

    This function uses SymPy's Poly class to ensure polynomial terms are ordered by
    descending powers (ax² + bx + c), providing consistent mathematical presentation.

    Args:
        expr: The MathsObject expression to group
        symbol: Optional specific symbol to collect by. If None, collects by all symbols.

    Returns:
        A MathsObject with grouped terms in descending power order

    Examples:
        >>> x = Symbol(s='x')
        >>> expr = x + Integer(n=2) * x + Integer(n=3)
        >>> grouped = group_terms(expr)  # Returns: 3x + 3

        >>> # Polynomial expansion with proper ordering
        >>> expr = (Integer(n=2)*x + Integer(n=3)) * (Fraction(p=-1, q=2)*x + Integer(n=1))
        >>> simplified = expr.simplified()
        >>> grouped = group_terms(simplified)  # Returns: -x² + (-1/2)x + 3 (descending powers)
    """
    try:
        # Get the SymPy expression and force complete expansion
        sympy_expr = expr.sympy_expr

        # Force complete flattening using a more aggressive approach
        def completely_flatten(expr):
            """Aggressively flatten nested structures by converting to string and back"""
            # Convert to string representation and parse back
            # This forces SymPy to rebuild the expression from scratch
            try:
                expr_str = str(expr)
                # Use SymPy's sympify to parse the string back to an expression
                flattened = sp.sympify(expr_str)
                return sp.expand(flattened)
            except:
                # Fallback to regular expand if string conversion fails
                return sp.expand(expr)

        # Apply aggressive flattening
        expanded = completely_flatten(sympy_expr)

        # Determine symbols to work with
        if symbol is not None:
            target_symbols = [symbol.sympy_expr]
        else:
            target_symbols = list(expanded.free_symbols)
            target_symbols.sort(key=str)

        # Process based on number of symbols
        if not target_symbols:
            # No symbols - just return expanded form
            ordered = expanded
        elif len(target_symbols) == 1:
            # Single variable - use manual coefficient extraction and reconstruction
            sym = target_symbols[0]

            # Extract all terms and their coefficients manually
            # This bypasses SymPy's Poly limitations with nested structures
            def extract_polynomial_terms(expr, symbol):
                """Extract coefficients for each power of the symbol"""
                coeffs = {}

                # Force expansion first
                expr = sp.expand(expr)

                # Use SymPy's built-in methods to extract coefficients for all powers
                # This is more reliable than manual parsing
                max_degree = sp.degree(expr, symbol)

                for power in range(max_degree + 1):
                    coeff = expr.coeff(symbol, power)
                    if coeff != 0:
                        coeffs[power] = coeff

                return coeffs

            # Extract coefficients
            coeff_dict = extract_polynomial_terms(expanded, sym)

            if coeff_dict:
                # Rebuild polynomial in descending order
                terms = []
                for power in sorted(coeff_dict.keys(), reverse=True):
                    coeff = coeff_dict[power]
                    if coeff != 0:
                        if power == 0:
                            terms.append(coeff)
                        elif power == 1:
                            terms.append(coeff * sym)
                        else:
                            terms.append(coeff * sym**power)

                if terms:
                    ordered = sp.Add(*terms, evaluate=False)
                else:
                    ordered = sp.S.Zero
            else:
                ordered = expanded
        else:
            # Multiple variables - use collect
            ordered = sp.collect(expanded, target_symbols, evaluate=True)

        # Convert back to MathsObject
        result = MathsObjectParser.from_sympy(ordered)
        return result

    except Exception:
        # Ultimate fallback - return original expression
        return expr


##################################################
# PARSER
##################################################

# TODO: If i could move this to a separate file, I'd be super happy


class MathsObjectParser:
    """Parser for reconstructing MathsObjects from their string representation using AST."""

    @staticmethod
    def from_repr(repr_str: str) -> "MathsObject":
        """
        Parse a string representation of a MathsObject and return the corresponding instance.

        Args:
            repr_str: String representation of a MathsObject (e.g., "Integer(n=5)")

        Returns:
            The reconstructed MathsObject instance
        """
        try:
            # Parse the string into an AST
            node = ast.parse(repr_str, mode="eval").body

            # Convert the AST to a MathsObject
            return MathsObjectParser._ast_to_maths_object(node)
        except Exception as e:
            raise ValueError(f"Failed to parse representation: {repr_str}. Error: {str(e)}")

    @staticmethod
    def _ast_to_maths_object(node: ast.AST) -> Any:
        """
        Convert an AST node to a MathsObject instance.

        Args:
            node: AST node representing a MathsObject

        Returns:
            The corresponding MathsObject instance
        """

        current_module = sys.modules[__name__]

        if isinstance(node, ast.Call):
            # Handle nested function calls for Image objects like Function(name=f)(Symbol(s='x'))
            if isinstance(node.func, ast.Call):
                # This is likely an Image object - Function(args)(pre)
                function_obj = MathsObjectParser._ast_to_maths_object(node.func)

                if len(node.args) == 1:
                    pre_obj = MathsObjectParser._ast_to_maths_object(node.args[0])
                else:
                    # Handle multiple arguments by creating a MathsCollection
                    pre_objs = [MathsObjectParser._ast_to_maths_object(arg) for arg in node.args]
                    pre_obj = MathsCollection(elements=pre_objs)

                # Create an Image object
                return Image(f=function_obj, pre=pre_obj)

            # Get the class name for regular call
            if hasattr(node.func, "id"):
                class_name = node.func.id
            elif hasattr(node.func, "attr"):  # Handle module.Class syntax
                class_name = node.func.attr
            else:
                raise ValueError(f"Unsupported function call structure: {ast.dump(node.func)}")

            # Make sure the class exists in the current module
            if not hasattr(current_module, class_name):
                raise ValueError(f"Unknown MathsObject class: {class_name}")

            cls = getattr(current_module, class_name)

            # Process the arguments
            args = []
            kwargs = {}

            # Handle positional arguments
            for arg in node.args:
                args.append(MathsObjectParser._ast_to_maths_object(arg))

            for kw in node.keywords:
                # Special case for Function(name=f)
                if class_name == "Function" and kw.arg == "name" and isinstance(kw.value, ast.Name):
                    # Use the name directly as a string instead of converting to Symbol
                    kwargs[kw.arg] = kw.value.id
                else:
                    kwargs[kw.arg] = MathsObjectParser._ast_to_maths_object(kw.value)

            # Create and return the instance
            return cls(*args, **kwargs)

        elif isinstance(node, ast.Constant):
            # Handle literals like integers, strings, etc.
            return node.value

        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            # Handle negative numbers
            if isinstance(node.operand, ast.Constant):
                return -node.operand.value

        elif isinstance(node, ast.Name):
            # Handle variable names (possibly used for None, True, False)
            if node.id == "None":
                return None
            elif node.id == "True":
                return True
            elif node.id == "False":
                return False

        # If we get here, we've encountered a node type we don't know how to handle
        raise ValueError(f"Unsupported AST node type: {type(node)}")

    @staticmethod
    def from_sympy(sympy_expr: sp.Basic) -> "MathsObject":
        """
        Convert a sympy expression to the corresponding MathsObject.

        Args:
            sympy_expr: A sympy expression

        Returns:
            The corresponding MathsObject instance
        """

        if isinstance(sympy_expr, sp.Integer):
            return Integer(n=int(sympy_expr))

        elif isinstance(sympy_expr, sp.Rational):
            return Fraction(p=Integer(n=sympy_expr.p), q=Integer(n=sympy_expr.q))

        elif isinstance(sympy_expr, sp.Symbol):
            return Symbol(s=sympy_expr.name)

        elif isinstance(sympy_expr, sp.Add):
            args = list(sympy_expr.args)
            if len(args) == 2:
                return Add(
                    l=MathsObjectParser.from_sympy(args[0]), r=MathsObjectParser.from_sympy(args[1])
                )
            else:
                # For expressions with more than two terms, make sure first term is a single object
                # and nest the remainder as needed
                first_term = args[0]
                rest_terms = sp.Add(*args[1:], evaluate=False)
                return Add(
                    l=MathsObjectParser.from_sympy(first_term),
                    r=MathsObjectParser.from_sympy(rest_terms),
                )

        # Add special case for division to handle fractions differently
        # We need to check if the structure is actually a*b^-1 which is how SymPy represents division
        elif isinstance(sympy_expr, sp.Mul) and any(
            isinstance(arg, sp.Pow) and arg.args[1] == -1 for arg in sympy_expr.args
        ):
            # Extract numerator and denominator parts
            num_parts = []
            denom_parts = []

            for arg in sympy_expr.args:
                if isinstance(arg, sp.Pow) and arg.args[1] == -1:
                    denom_parts.append(arg.args[0])  # Base of the power with -1 exponent
                else:
                    num_parts.append(arg)

            # Create the numerator expression
            if len(num_parts) == 0:
                numerator = Integer(n=1)  # If no numerator parts, it's just 1
            elif len(num_parts) == 1:
                numerator = MathsObjectParser.from_sympy(num_parts[0])
            else:
                numerator = MathsObjectParser.from_sympy(sp.Mul(*num_parts, evaluate=False))

            # Create the denominator expression
            if len(denom_parts) == 1:
                denominator = MathsObjectParser.from_sympy(denom_parts[0])
            else:
                denominator = MathsObjectParser.from_sympy(sp.Mul(*denom_parts, evaluate=False))

            return Fraction(p=numerator, q=denominator)

        elif isinstance(sympy_expr, sp.Mul):
            args = list(sympy_expr.args)
            if len(args) == 2:
                return Mul(
                    l=MathsObjectParser.from_sympy(args[0]), r=MathsObjectParser.from_sympy(args[1])
                )
            else:
                # For expressions with more than two terms, make sure first term is a single object
                # and nest the remainder as needed
                first_term = args[0]
                rest_terms = sp.Mul(*args[1:], evaluate=False)
                return Mul(
                    l=MathsObjectParser.from_sympy(first_term),
                    r=MathsObjectParser.from_sympy(rest_terms),
                )

        elif isinstance(sympy_expr, sp.Pow):
            args = list(sympy_expr.args)
            if len(args) == 2:
                return Pow(
                    base=MathsObjectParser.from_sympy(args[0]),
                    exp=MathsObjectParser.from_sympy(args[1]),
                )
            else:
                raise NotImplementedError("Sympy power with something other than 2 arguments")

        elif isinstance(sympy_expr, sp.Function):
            # Handle function applications
            func_name = type(sympy_expr).__name__
            func = Function(name=func_name)

            if len(sympy_expr.args) == 1:
                pre = MathsObjectParser.from_sympy(sympy_expr.args[0])
            else:
                pre_objs = [MathsObjectParser.from_sympy(arg) for arg in sympy_expr.args]
                pre = MathsCollection(elements=pre_objs)

            return Image(f=func, pre=pre)

        elif isinstance(sympy_expr, sp.Equality):
            l, r = sympy_expr.args
            return Equality(l=MathsObjectParser.from_sympy(l), r=MathsObjectParser.from_sympy(r))

        elif isinstance(sympy_expr, sp.StrictGreaterThan):
            l, r = sympy_expr.args
            return StrictGreaterThan(
                l=MathsObjectParser.from_sympy(l), r=MathsObjectParser.from_sympy(r)
            )

        elif isinstance(sympy_expr, sp.Float):
            return Decimal(x=float(sympy_expr))

        else:
            raise NotImplementedError(
                f"Conversion from sympy type {type(sympy_expr)} is not implemented"
            )

    def _latex_to_sympy(self, latex):
        sympy_expr = sympy_parse_latex(latex)
        return sympy_expr

    def from_latex(self, latex):
        """
        Convert a LaTeX string to a MathsObject by using sympy's parsing capabilities.

        Args:
            latex: A LaTeX string

        Returns:
            The corresponding MathsObject instance
        """

        sympy_expr = self._latex_to_sympy(latex)
        return self.from_sympy(sympy_expr)
