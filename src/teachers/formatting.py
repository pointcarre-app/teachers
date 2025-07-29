import enum


class Formatting(enum.Enum):
    DECIMAL_OR_INTEGER = "Ta réponse doit être un nombre décimal ou un entier."
    FRACTION_OR_INTEGER = "Ta réponse doit être une fraction irréductible ou un entier."
    PERCENT = "Ta réponse doit être un pourcentage."
    GIVE_FORMULA = ...
