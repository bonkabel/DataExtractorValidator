from datetime import datetime, date, timedelta


class Validator:
    '''
    Validates PatientRecord objects and their attributes

    '''
    def validate(self, record):
        '''
        Validates an entire PatientRecord

        :param record: A PatientRecord object
        :return: (valid, errors):
            valid is True if the record passes all the checks
            errors is a list of strings that describes the errors with the record
        '''
        errors = []

        errors.extend(self.validateHealthCardNumber(record.healthCardNumber))
        errors.extend(self.validateVersionCode(record.versionCode))
        errors.extend(self.validateDateOfBirth(record.dateOfBirth))
        errors.extend(self.validateServiceDate(record.serviceDate, record.dateOfBirth))

        return (len(errors) == 0), errors


    def validateHealthCardNumber(self, healthCardNumber):
        '''
        Validate health card number and return error message

        Rules:
            - Must have a health card number
            - Must contain only digits
            - Must be exactly 10 digits
            - Must pass Luhn check

        :param healthCardNumber: The health card number to validate

        :return: List[str] List of errors. Empty list if valid
        '''

        errors = []

        # Check if the health card number is empty
        if healthCardNumber is None:
            errors.append("The health card number is missing")
            return errors

        # Check if the health card number is 10 characters
        if len(healthCardNumber) != 10:
            errors.append("The health card number is not 10 characters")

        # Check if the health card number is just digits
        if not healthCardNumber.isdigit():
            errors.append("The health card number contains non digit characters")
            return errors

        # Check if the health card number passes the luhn check
        if not self.luhnCheck(healthCardNumber):
            errors.append("The health card number failed MOD 10 validation")

        return errors

    def luhnCheck(self, number):
        '''
        Validates the number with the Luhn algorithm

        :param number: The number to validate
        :return: If the number passes the Luhn check
        '''
        # Convert all digits individually just for safety
        digits = [int(i) for i in number]

        checksum = 0

        # Determine which positions to double
        parity = (len(digits) - 2) % 2

        # Process the digits except the final check digit
        for i, d in enumerate(digits[:-1]):
            # Double every second digit
            if i % 2 == parity:
                d = d * 2
                # If the result is two digits, we subtract 9
                if d > 9:
                    d -= 9

            # Add to the checksum
            checksum += d

        checksum += digits[-1]

        return checksum % 10 == 0


    def validateVersionCode(self, versionCode):
        '''
        Validate the health card version code

        Rules:
            - Exactly 2 characters
            - Both characters must be uppercase letters

        :param versionCode: The version code to validate
        :return: If the health card version code is valid
        '''
        errors = []

        # Checks if the version code is missing
        if not versionCode:
            errors.append("The health card version code is missing")
            return errors

        # Version code needs to be 2 characters long
        if len(versionCode) != 2:
            errors.append("The health card version code must be exactly 2 characters")

        # The version code needs to be alphabetical, uppercase characters
        if not versionCode.isalpha() or not versionCode.isupper():
            errors.append("The health card version code must be uppercase letters")

        return errors

    def validateDateOfBirth(self, dateOfBirth):
        '''
        Validate the date of birth

        Rules:
            - Must be a valid date
            - Must be in the form YYYY-MM-DD
            - The date of brith can't be in the future
            - The date of birth can't be 150 years ago or more

        :param dateOfBirth: The date of birth to validate
        :return: If the date of birth is valid
        '''
        errors = []

        # Checks if the dateOfBirth is missing
        if dateOfBirth is None:
            errors.append("The date of birth is missing")
            return errors

        # Attempts to parse the dateOfBirth
        try:
            parsedDateOfBirth = datetime.strptime(str(dateOfBirth), '%Y-%m-%d').date()
        except ValueError:
            errors.append("Date of birth must be in the form YYYY-MM-DD")
            return errors

        today = datetime.today().date()

        age = self.calculateAge(today, parsedDateOfBirth)

        if age < 0:
            errors.append("The patient must be at least 0 years old")
            return errors

        if age >= 150:
            errors.append("The patient must be less than 150 years old")


        return errors

    def calculateAge(self, dateToday, dateOfBirth):
        '''
        Calculates an age based on the date today and the date of birth

        :param dateToday: The current date today
        :param dateOfBirth: The date of birth
        :return: The age
        '''
        age = dateToday.year - dateOfBirth.year

        # Checking if they haven't had their birthday yet
        if (dateToday.month, dateToday.day) < (dateOfBirth.month, dateOfBirth.day):
            age = age - 1

        return age


    def validateServiceDate(self, serviceDate, dateOfBirth):
        '''
        Validate the date of service

        Rules:
            - Must be a valid date in the form YYYY-MM-DD
            - Cannot be before the date of birth
            - Cannot be in the future
            - Cannot be more than 6 months in the past

        :param serviceDate: The date of service to validate
        :param dateOfBirth: The date of birth
        :return: If the date of service is valid
        '''
        errors = []

        # Checks if serviceDate is missing
        if serviceDate is None:
            errors.append("The date of service is missing")
            return errors

        # Attempts to parse the service date
        try:
            parsedServiceDate = datetime.strptime(str(serviceDate), '%Y-%m-%d').date()
        except ValueError:
            errors.append("Date of service must be in the form YYYY-MM-DD")
            return errors

        today = datetime.today().date()

        # Service date can't be in the future
        if parsedServiceDate > today:
            errors.append("The date of service cannot be in the future")
            return errors

        # Service date can't be more than 6 months ago
        if parsedServiceDate < (today - timedelta(days=183)):
            errors.append("The date of service cannot be more than 6 months in the past")
            return errors

        # Attempts to parse the date of birth
        try:
            parsedDateOfBirth = datetime.strptime(str(dateOfBirth), '%Y-%m-%d').date()
        except Exception:
            # This is handled in the date of birth validator
            parsedDateOfBirth = None

        # Service date can't be before the date of birth
        if (parsedDateOfBirth is not None) and (parsedServiceDate < parsedDateOfBirth):
            errors.append("The date of service cannot be before the date of birth")

        return errors
