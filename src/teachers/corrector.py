import difflib
import re


import sympy as sp

import teachers.maths as tm


def correct(user_mathlive: str, answer_formal_repr):
    # Compute needed stuff
    ######################

    parser = tm.MathsObjectParser()

    # Answer
    answer_maths_object = parser.from_repr(answer_formal_repr)
    answer_simplified_maths_object = answer_maths_object.simplified()
    answer_simplified_latex = answer_simplified_maths_object.latex()
    perfect_latex = clean_teachers_latex(answer_simplified_latex)

    # User
    user_cleaned_mathlive = clean_mathlive(user_mathlive)
    user_maths_object = parser.from_latex(user_cleaned_mathlive)
    user_for_display_latex = clean_latex_for_display(user_cleaned_mathlive)

    correction = {
        # "user_mathlive": user_mathlive,
        # "user_cleaned_mathlive": user_cleaned_mathlive,
        # "user_for_display_latex": user_for_display_latex,
        # "user_maths_object": repr(user_maths_object),
        # "answer_formal_repr": answer_formal_repr,
        # "answer_maths_object": answer_maths_object,
        # "answer_simplified_maths_object": answer_simplified_maths_object,
        # "answer_simplified_latex": answer_simplified_latex,
        # "perfect_latex": perfect_latex,
        "answer": {
            # "latex": answer["maths_object"].latex(),
            "simplified_latex": answer_simplified_latex,
            # "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": answer_formal_repr,
        },
    }

    # sel: format for the correction object
    # correction = {
    #     "user": {
    #         "mathlive": user_mathlive,
    #         "cleaned_mathlive": user_cleaned_mathlive,
    #         "for_display_latex": user_for_display_latex,
    #         "maths_object": repr(user_maths_object),
    #         "tags": {
    #             "is_affine": True,
    #             "is_integer": True,
    #             "is_positive": True,
    #             .....
    #         }
    #     },
    #     "answer": {
    #         "formal_repr": answer_formal_repr,
    #         "maths_object": repr(answer_maths_object),
    #         "simplified_maths_object": repr(answer_simplified_maths_object),
    #         "simplified_latex": answer_simplified_latex,
    #         "perfect_latex": perfect_latex,
    #         "tags": {
    #             "is_affine": True,
    #             "is_integer": True,
    #             "is_positive": True,
    #             .....
    #         }
    #     },
    #     # "is_perfect": is_perfect,
    #     # "is_correct": is_correct,
    #     # "diff": diff_text,
    #     Sel: ET Logique sur les tags user et answer
    #     "tags": {
    #
    #         .....
    #     }
    # }

    # Latex comparision
    ###################

    if user_cleaned_mathlive == perfect_latex:
        correction["is_perfect"] = True
    else:
        correction["is_perfect"] = False
        # NOTE: do not erasse, really useful for debugging as it appears in the stdout of the backend executor
        print("ERROR:")
        print("user:", user_cleaned_mathlive)
        print("teacher:", perfect_latex)
        # Calculate and display the diff between the two strings
        diff = difflib.ndiff(user_cleaned_mathlive.splitlines(), perfect_latex.splitlines())
        diff_text = "\n".join(diff)
        print("DIFF:")
        print(diff_text)

    # Sympy comparison
    ##################

    diff_sympy = answer_maths_object.sympy_expr - user_maths_object.sympy_expr
    diff_sympy = sp.simplify(diff_sympy)
    if diff_sympy == 0:
        correction["is_correct"] = True
    else:
        correction["is_correct"] = False

    return correction


## TODO : separate into multiple functions independently tested
## Feed output of generator and corrector (ie from JS)
def clean_mathlive(mathlive: str) -> str:
    # Handle fractions without braces like \frac16 -> \frac{1}{6} and \dfrac16 -> \frac{1}{6}
    # This pattern matches \frac or \dfrac followed by exactly two single characters/digits
    # All fractions are normalized to \frac format
    frac_without_braces_regex = r"\\d?frac([a-zA-Z0-9])([a-zA-Z0-9])"

    def replace_fraction(match):
        numerator = match.group(1)
        denominator = match.group(2)
        return f"\\frac{{{numerator}}}{{{denominator}}}"

    # Replace all occurrences of the pattern
    result = re.sub(frac_without_braces_regex, replace_fraction, mathlive)

    # In all cases
    # Todo: check escaping and raw strings

    result = result.replace("\\dfrac", "\\frac")

    # Normalize parentheses
    result = result.replace("\\left(", "(")
    result = result.replace("\\right)", ")")

    #
    result = re.sub(r"([a-zA-Z0-9\)\]\}])([><=≥≤≠])([a-zA-Z0-9\(\[\{])", r"\1 \2 \3", result)

    # Normalize other brackets
    # result = result.replace("\\left[", "[")
    # result = result.replace("\\right]", "]")
    # result = result.replace("\\left\\{", "{")
    # result = result.replace("\\right\\}", "}")

    return result


def clean_teachers_latex(latex: str) -> str:
    # Decimal
    latex = latex.replace(".", ",")

    # Fractions
    latex = latex.replace("dfrac", "frac")

    # remove backslashes before braces
    # teacher_string = teacher_string.replace("\\{", "{")
    # teacher_string = teacher_string.replace("\\}", "}")

    # replace \frac{}{} with \frac{A}{B}

    return latex


def clean_latex_for_display(latex):
    cleaned_for_display = latex.replace("frac", "dfrac")
    return cleaned_for_display


# missive(
#     {
#         "user_answer_raw": user_answer,
#         "user_answer_cleaned": cleaned_user_answer,
#         "user_answer_for_display": for_display_user_answer,
#         "answer_raw": answer,
#         "answer_cleaned": cleaned_answer,
#         "are_cleaned_latex_equal": are_cleaned_latex_equal,
#     }
# )  # noqa F821


# if "user_answer" in globals():
#     print(user_answer, clean_mathlive_latex(user_answer))
# if "answer" in globals():
#     print(answer, clean_teachers_latex(answer))
# print(json.loads(components))
# print(statement)  # noqa F821
# print(components)  # noqa F821
# print(answer_formating)  # noqa F821
