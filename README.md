# Patient Record Validator
A console application built in python that extracts patient records from a PDF, validates each field, and outputs both a CSV of valid records and an error report with statistics. Valid records are also added to a SQLite database

## Features
- Extracts data tables from PDFs using pdfplumber
- Validates fields using Validator and ValidationError
- Converts each row into a PatientRecord object
- Writes valid records to a CSV
- Writes an error report complete with statistics
- Gracefully handles any errors that occur while loading the PDF

## How It Works
1. PDFExtractor reads the PDF and extracts the data from the tables
2. Validator validates each field returning the errors found. ValidationError is used for storing the errors
3. OutputWriter handles creating the CSV of valid records, putting them in the SQLite database, and creating the error report with statistics

## How To Use
- Install pdfplumber `pip install pdfplumber`
- Run the application `python app.py <input.pdf> <output_folder>`

## Dependencies
- pdfplumber
- pdfminer.six (Installed with pdfplumber)

## Assumptions
- Assumes the first row of each table is the header
- Assumes the table columns follow the expected order of [Patient ID, Health Card Number, Version Code, Date of Birth, Service Date]
- Doesn't validate patient id

