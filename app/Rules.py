class Rules:
    """
    Defines standardized rule identifiers for validation errors
    Each rule is a category for errors that can occur during validation
    """

    # A required field is empty or not present
    MISSING = "missing"

    # A field has a value but it is not logically valid
    # E.g. failed luhn check, invalid date, bad characters, etc.
    INVALID = "invalid"

    # A value is outside the allowed range
    RANGE = "range"

    # The value exists but it is of the wrong type
    # E.g. String instead of int
    TYPE = "type"

    # The record structure is incorrect
    # E.g. Wrong number of fields, missing columns, malformed data
    STRUCTURE = "structure"
