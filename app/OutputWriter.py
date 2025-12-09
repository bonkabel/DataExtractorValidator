import csv
from datetime import datetime

class OutputWriter:
    '''
    Responsible for producing the output files.
        1. Writes valid records to a csv file.
        2. Produces an error report text file for the invalid records.

    Only responsible for formatting and writing.
    '''
    def writeValidCSV(self, records, path):
        '''
        Writes the valid patient records to a csv file

        :param records: List of valid PatientRecord objects
        :param path: Output file path for the csv file
        '''
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow([
                "Patient ID",
                "Health Card Number",
                "Version Code",
                "Date of Birth",
                "Service Date"
            ])

            # Write the actual records
            for record in records:
                writer.writerow([
                    record.patientId,
                    record.healthCardNumber,
                    record.versionCode,
                    record.dateOfBirth,
                    record.serviceDate
                ])

    def writeErrorReport(self, invalidRecords, path, validCount):
        '''
        Write a text report describing the invalid records and their errors.

        Includes
            - Timestamp of generation
            - Summary of total, valid and invalid records
            - List of invalid records with error messages




        :param records: List of tuples (record, errors)
        :param path: Output file path for the report file
        :param validCount: Number of valid records
        '''

        totalProcessed = validCount + len(invalidRecords)

        with open(path, "w") as f:
            f.write("ERROR REPORT\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write(f"Total Records Processed: {totalProcessed}\n")
            f.write(f"Valid Records: {validCount}\n")
            f.write(f"Invalid Records: {len(invalidRecords)}\n")
            f.write("INVALID RECORDS:\n\n")

            # Write each invalid record with its error message
            for record, errors in invalidRecords:
                f.write(f"Patient ID: {record.patientId}\n")

                for error in errors:
                    f.write(f"\t- {error}\n")
                f.write("\n")