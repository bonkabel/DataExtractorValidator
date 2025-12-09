
class RecordProcessor:
    '''

    RecordProcessor coordinates the processing of the patient records

    Steps:
        1. The records are retrieved from the extractor
        2. The records are validated with the validator
        3. The records are separated into valid and invalid groups

    Attributes:
        extractor: Responsible for reading records from the input source
        validator: Responsible for validating the records
        validRecords: A list of the records that pass validation
        invalidRecords: A list of tuples, containing the record and its associated error
    '''
    def __init__(self, extractor, validator):
        self.extractor = extractor
        self.validator = validator
        self.validRecords = []
        self.invalidRecords = []

    '''
    Extracts the records, validates them, and populates the valid and invalid lists
    '''
    def process(self):
        # Extracting the records from the PDF into records
        records = self.extractor.extractRecords()


        for record in records:
            # valid: boolean, if the record is valid
            # errors: list of issues with the record
            valid, errors = self.validator.validate(record)

            if valid:
                self.validRecords.append(record)
            else:
                self.invalidRecords.append((record, errors))