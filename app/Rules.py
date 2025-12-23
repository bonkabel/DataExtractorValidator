class Rules:
    """
    Defines standardized rule identifiers for validation errors
    Each rule is a category for errors that can occur during validation
    """

    # A required field is empty or not present
    MISSING = "missingfield"

    # A field has a value but it is not logically valid
    # E.g. failed luhn check, invalid date, bad characters, etc.
    INVALID = "invalidvalue"

    # A value is outside the allowed range
    RANGE = "valueoutsiderange"

    # The value exists but it is of the wrong type
    # E.g. String instead of int
    TYPE = "type"

    # The record structure is incorrect
    # E.g. Wrong number of fields, missing columns, malformed data
    STRUCTURE = "structure"

    DISPLAY_NAME = {
        MISSING: "Missing Field",
        INVALID: "Invalid Field",
        RANGE: "Value Outside Range",
        TYPE: "Type",
        STRUCTURE: "Structure"
    }

    @classmethod
    def getDisplayName(cls, ruleName):
        """
        Returns the display name of a rule.

        :param ruleName: The rule name
        :return:
        """
        return Rules.DISPLAY_NAME.get(ruleName, ruleName)

    @classmethod
    def getAllFields(cls):
        """
        :return: A list of all fields.
        """
        return set(cls.DISPLAY_NAME.keys())