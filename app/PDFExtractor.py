import pdfplumber
from app.PatientRecord import PatientRecord

class PDFExtractor:
    """
    Extracts patient records from a PDF file

    Attributes:
        filePath: Path to the PDF file
    """

    def __init__(self, filePath):
        """
        Creates a new PDFExtractor object

        :param filePath: Path to the PDF file that contains patient data
        """
        self.filePath = filePath

    def extractRecords(self):
        """
        Extracts patient records from a PDF file

        Notes:
            Assumes the first row of the PDF is the column headings

        :return: A list of PatientRecord objects. Each row of the PDF table after the header is converted into a PatientRecord object
        """

        # return a list of patient records
        records = []

        with pdfplumber.open(self.filePath) as pdf:
            for page in pdf.pages:
                table = page.extract_table()

                # Makes sure there is a table
                if not table:
                    continue

                # Go through the rows of the table
                # Assuming the first row is the column names
                for row in table[1:]:
                    record = PatientRecord(row[0], row[1], row[2], row[3], row[4])
                    records.append(record)

        return records
