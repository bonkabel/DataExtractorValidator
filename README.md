# Patient Record Validator
A console application built in python that extracts patient records from a PDF, validates each field, and outputs both a CSV of valid records and an error report with statistics. Valid records are also added to a SQLite database

## Web App
https://dataextractorvalidator.streamlit.app/
- Upload a patient data file
- You can view the patient data and statistics
- You can download the valid records, error report, and statistics files

## Features
- Writes valid records to a CSV and uploads them to a SQLite database
- Writes an error report complete with statistics on which fields had errors and the types of errors
- Gracefully handles any errors that occur while loading the PDF
- User friendly UI

## How It Works
1. RecordProcessor coordinates the extraction and validation of the patient records
2. PDFExtractor reads the PDF and extracts the data from the tables
3. Validator validates each field returning the errors found. ValidationError is used for storing the error data
4. OutputWriter handles creating the CSV of valid records, and creating the error report with statistics
5. SQLiteWriter writes the valid records to the database

## How to run it yourself
- Install pdfplumber `pip install pdfplumber`
- Install streamlit `pip install streamlit`
- Install plotly `pip install plotly`
- Run the application `python app.py <input.pdf> <output_folder>`
- OR run it through streamlit `streamlit run <AppWrappUI.py>`

## Dependencies
- pdfplumber
- streamlit
- pandas
- plotly

## Assumptions
- Assumes the first row of each table is the header
- Assumes the table columns follow the expected order of [Patient ID, Health Card Number, Version Code, Date of Birth, Service Date]
- Doesn't validate patient id

## Reasoning
I used Python for this project for simplicity. For a larger project handling real data I would lean towards using C#. I chose to use pdfplumber because it works very well for extracting table data.

## Potential Expansions
- Ability to manually fix records with errors
- Is patient id required? It seems unnecessary due to health card numbers being unique.
  - Remove?
  - Replace with health card number?
- Normalize and sanitize extracted data
  - Would have to identify what the system is allowed to auto correct first and what would require human confirmation
  - SHOULD the system be allowed to correct health card numbers, dates, etc. and to what extent?
- Account for different column orders?

