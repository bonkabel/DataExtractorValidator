import csv
from datetime import datetime
from app.Fields import Fields
import json


class OutputWriter:
    """
    Responsible for producing the output files.
        1. Writes valid records to a csv file.
        2. Produces an error report text file for the invalid records.

    Only responsible for formatting and writing.
    """

    def __init__(self, validRecords, invalidRecords):
        self.validRecords = validRecords
        self.invalidRecords = invalidRecords
        self.totalRecords = len(validRecords) + len(invalidRecords)
        self.ruleStats = {}
        self.fieldStats = {}

        for record, errors in invalidRecords:
            for e in errors:
                self.ruleStats[e.rule] = self.ruleStats.get(e.rule, 0) + 1
                self.fieldStats[e.field] = self.fieldStats.get(e.field, 0) + 1

    def writeValidCSV(self, path):
        """
        Writes the valid patient records to a csv file

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
            for record in self.validRecords:
                writer.writerow([
                    record.patientId,
                    record.healthCardNumber,
                    record.versionCode,
                    record.dateOfBirth,
                    record.serviceDate
                ])

    def writeErrorReport(self, path):
        """
        Write a text report describing the invalid records and their errors.

        Includes
            - Timestamp of generation
            - Summary of total, valid and invalid records
            - List of invalid records with error messages
        """

        with open(path, "w") as f:
            f.write("Summary\n")
            f.write("============\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write(f"Total Records Processed: {self.totalRecords}\n")
            f.write(f"Valid Records: {self.validRecords}\n")
            f.write(f"Invalid Records: {len(self.invalidRecords)}\n")
            f.write(f"Percent of records valid: {len(self.validRecords) / self.totalRecords * 100}%\n\n")

            f.write(f"Validation Issues\n")
            f.write(f"=================\n")
            for rule, count in self.ruleStats.items():
                f.write(f"{rule}: {count}\n")
            f.write("\n")

            f.write(f"What fields had the issues\n")
            f.write(f"==========================\n")
            for field, count in self.fieldStats.items():
                f.write(f"{Fields.getDisplayName(field)}: {count}\n")
            f.write("\n")

            f.write("Invalid Records\n")
            f.write("===============\n")
            # Write each invalid record with its error message
            for record, errors in self.invalidRecords:
                f.write(f"Patient ID: {record.patientId}\n")

                for error in errors:
                    f.write(f"\t- {error.message}\n")
                f.write("\n")

    def writeJSON(self, path):
        """Writes to a JSON file"""

        stats = {
            "summary": {
                "timestamp": datetime.now().isoformat(),
                "totalRecordsProcessed": self.totalRecords,
                "validRecords": len(self.validRecords),
                "invalidRecords": len(self.invalidRecords),
                "percentRecordsValid": len(self.validRecords) / self.totalRecords * 100
            },
            "validationIssues": self.ruleStats,
            "fieldsWithIssues": self.fieldStats
        }

        with open(path, "w") as f:
            json.dump(stats, f, indent=4)