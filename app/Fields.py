class Fields:
    """
    Defines standardized field identifiers.
    """

    PATIENT_ID = "patientid"
    HEALTH_CARD_NUMBER = "healthcardnumber"
    VERSION_CODE = "versioncode"
    DATE_OF_BIRTH = "dateofbirth"
    SERVICE_DATE = "servicedate"

    DISPLAY_NAME = {
        PATIENT_ID: "Patient ID",
        HEALTH_CARD_NUMBER: "Health Card Number",
        VERSION_CODE: "Version Code",
        DATE_OF_BIRTH: "Date of Birth",
        SERVICE_DATE: "Service Date",
    }

    @classmethod
    def getDisplayName(cls, fieldName):
        """
        Returns the display name of a field.

        :param fieldName: The field name
        :return:
        """
        return Fields.DISPLAY_NAME.get(fieldName, fieldName)

    @classmethod
    def getAllFields(cls):
        """

        :return: A list of all fields.
        """
        return set(cls.DISPLAY_NAME.keys())