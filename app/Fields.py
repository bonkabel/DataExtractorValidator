class Fields:
    """
    Defines standardized field identifiers.
    """

    PATIENT_ID = "patientid"
    HEALTH_CARD_NUMBER = "healthcardnumber"
    VERSION_CODE = "versioncode"
    DATE_OF_BIRTH = "dateofbirth"
    SERVICE_DATE = "servicedate"

    ALL_FIELDS = {
        PATIENT_ID,
        HEALTH_CARD_NUMBER,
        VERSION_CODE,
        DATE_OF_BIRTH,
        SERVICE_DATE,
    }


    DISPLAY_NAME = {
        PATIENT_ID: "Patient ID",
        HEALTH_CARD_NUMBER: "Health Card Number",
        VERSION_CODE: "Version Code",
        DATE_OF_BIRTH: "Date of Birth",
        SERVICE_DATE: "Service Date",
    }

    @staticmethod
    def getDisplayName(field):
        """
        Returns the display name of a field.

        :param field: The field name
        :return:
        """
        return Fields.DISPLAY_NAME.get(field, field)
