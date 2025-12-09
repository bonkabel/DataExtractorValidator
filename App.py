from app.OutputWriter import OutputWriter
from app.PDFExtractor import PDFExtractor
from app.RecordProcessor import RecordProcessor
from app.Validator import Validator
from app.SQLiteWriter import SQLiteWriter


class App:
    """
    Coordinates the flow of the application

    Steps:
        1. Extracts records from a PDF
        2. Validate each record
        3. Write valid records to a csv file
        4. Write an error report
    """
    def __init__(self, inputPDF, outputDirectory):
        """
        Creates the components of the application

        :param inputPDF: Path to the PDF containing the records
        :param outputDirectory: Directory where the output files will be written
        """

        # Extracts rows from the PDF
        self.extractor = PDFExtractor(inputPDF)

        # Validates the records
        self.validator = Validator()

        # Runs the components that extract and validate
        self.processor = RecordProcessor(self.extractor, self.validator)

        # Writes CSV and text report
        self.outputWriter = OutputWriter()

        # The target directory for the output files
        self.outDirectory = outputDirectory

        # SQLite writer
        dbPath = f"{self.outDirectory}/records.db"
        self.dbWriter = SQLiteWriter(dbPath)

    def run(self):
        """
        Runs the extraction and validation process
        Generates the output files
        """
        # Run the extraction and validation
        self.processor.process()

        # Paths for the output files
        validPath = f"{self.outDirectory}/valid_records.csv"
        invalidPath = f"{self.outDirectory}/error_report.txt"

        # Writing the CSV and error report
        self.outputWriter.writeValidCSV(self.processor.validRecords, validPath)
        self.outputWriter.writeErrorReport(self.processor.invalidRecords, invalidPath, len(self.processor.validRecords))

        # Write valid records to SQLite
        self.dbWriter.insertRecords(self.processor.validRecords)

if __name__ == "__main__":
    import sys
    import os

    # Expects two arguments
    if len(sys.argv) != 3:
        print("Usage: python app.py <input.pdf> <output directory>")
        sys.exit(1)

    # Read command line arguments
    inputPDF = sys.argv[1]
    outputDirectory = sys.argv[2]

    # Creates the output directory if it doesn't exist
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    # Create and run the application
    app = App(inputPDF, outputDirectory)
    app.run()

    print("Done.")