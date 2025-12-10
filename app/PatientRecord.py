class PatientRecord:
    """
    Represents a single patient record

    Attributes:
        patientId: Unique identifier for the patient
        healthCardNumber: Ten digit Ontario health card number. Must pass Luhn algo check
        versionCode: Two letter (uppercase) health card version code
        dateOfBirth: Patient date of birth in YYYY-MM-DD format
        serviceDate: Date the service was provided in YYYY-MM-DD format
    """
    def __init__(self, patientId, healthCardNumber, versionCode, dateOfBirth, serviceDate):
        self.patientId = patientId
        self.healthCardNumber = healthCardNumber
        self.versionCode = versionCode
        self.dateOfBirth = dateOfBirth
        self.serviceDate = serviceDate
