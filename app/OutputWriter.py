import csv
from datetime import datetime

class OutputWriter:
    """
    Responsible for producing the output files.
        1. Writes valid records to a csv file.
        2. Produces an error report text file for the invalid records.

    Only responsible for formatting and writing.
    """
    def writeValidCSV(self, records, path):
        """
        Writes the valid patient records to a csv file

        :param records: List of valid PatientRecord objects
        :param path: Output file path for the csv file
        """
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
        """
        Write a text report describing the invalid records and their errors.

        Includes
            - Timestamp of generation
            - Summary of total, valid and invalid records
            - List of invalid records with error messages

        :param invalidRecords: List of tuples (record, errors)
        :param path: Output file path for the report file
        :param validCount: Number of valid records
        """

        totalProcessed = validCount + len(invalidRecords)

        # Set up the error statistics
        ruleStats = {}
        fieldStats = {}
        for record, errors in invalidRecords:
            for e in errors:
                ruleStats[e.rule] = ruleStats.get(e.rule, 0) + 1
                fieldStats[e.field] = fieldStats.get(e.field, 0) + 1



        with open(path, "w") as f:
            f.write("Summary\n")
            f.write("============\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write(f"Total Records Processed: {totalProcessed}\n")
            f.write(f"Valid Records: {validCount}\n")
            f.write(f"Invalid Records: {len(invalidRecords)}\n")
            f.write(f"Percent of records valid: {validCount / totalProcessed * 100}%\n\n")

            f.write(f"Validation Issues\n")
            f.write(f"=================\n")
            for rule, count in ruleStats.items():
                f.write(f"{rule}: {count}\n")
            f.write("\n")

            f.write(f"What fields had the issues\n")
            f.write(f"==========================\n")
            for field, count in fieldStats.items():
                f.write(f"{field}: {count}\n")
            f.write("\n")

            f.write("Invalid Records\n")
            f.write("===============\n")
            # Write each invalid record with its error message
            for record, errors in invalidRecords:
                f.write(f"Patient ID: {record.patientId}\n")

                for error in errors:
                    f.write(f"\t- {error.message}\n")
                f.write("\n")