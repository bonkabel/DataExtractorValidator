class ValidationError:
    """
    Represents a single validation error

    Meant for use with Fields and Rules
    """
    def __init__(self, field, rule, message):
        """
        Create a validation error

        :param field: The field that has the validation error
        :param rule: The validation rule that is being broken
        :param message: An friendly error message for the user
        """
        self.field = field
        self.rule = rule
        self.message = message

    def toDictionary(self):
        """
        Convert the error to a dictionary

        :return: A dictionary of the error
        """
        return {
            "field": self.field,
            "rule": self.rule,
            "message": self.message
        }