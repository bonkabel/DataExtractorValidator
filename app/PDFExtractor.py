import pdfplumber
from pdfminer.pdfparser import PDFSyntaxError
from pdfplumber.utils.exceptions import PdfminerException

from app.Fields import Fields
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
            Assumes the header can only be in the first row of a table
            Assumes the tables columns are in the order patient id, health card numbers, version code, date of birth, service date

        :return: A list of PatientRecord objects. Each row of the PDF table after the header is converted into a PatientRecord object
        """

        records = []
        foundTable = False

        try:
            with pdfplumber.open(self.filePath) as pdf:
                for page in pdf.pages:
                    table = page.extract_table()

                    # Makes sure there is a table
                    if not table:
                        continue
                    else:
                        foundTable = True

                    # Go through the rows of the table
                    # Assuming the first row is the column names

                    table = self.removeHeader(table, Fields.getAllFields())

                    for row in table:
                        if row is None or len(row) != 5:
                            raise Exception(
                                f"Incomplete record found in '{self.filePath}' on page {page.page_number}\n"
                                f"Ensure that all rows are present and have 5 fields"
                            )
                        record = PatientRecord(row[0], row[1], row[2], row[3], row[4])
                        records.append(record)

            # Raise an exception if there's no table present
            if not foundTable:
                raise Exception(
                    f"The file '{self.filePath}' does not contain any readable tables\n"
                    f"Ensure the PDF has a table present")
        # Raise an exception if the file isn't found
        except FileNotFoundError as e:
            raise Exception(
                f"PDF file '{self.filePath}' was not found\n"
                f"Details: {str(e)}")
        # Raise an error if there is an IO exception
        except IOError as e:
            raise Exception(
                f"PDF file '{self.filePath}' could not be opened\n"
                f"Details: {str(e)}")
        # Raise an error if there is a issue with the PDF
        except (PDFSyntaxError, PdfminerException) as e:
            raise Exception(
                f"The file '{self.filePath}' is not a valid PDF file or has been corrupted\n"
                f"Details: {str(e)}")
        except Exception as e:
            raise Exception(
                f"An unexpected error has occurred while attempting to process '{self.filePath}'\n"
                f"Details: {str(e)}"
            )


        return records

    def removeHeader(self, table, headerData):
        """
        Removes a header from a table if the header contains headerData. Assumes the first row of a table is the header.

        :param table: A table to remove the header from
        :param headerData: The header data to look for
        :return: A table with the header removed. If no header present, returns table
        """
        firstRow = table[0]
        normalizedRow = [''.join(char.lower() for char in cell if char.isalpha()) for cell in firstRow]

        if headerData.issubset(normalizedRow):
            table.pop(0)
            return table
        else:
            return table



