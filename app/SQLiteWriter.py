import sqlite3

class SQLiteWriter:
    '''
    Handles saving valid patient records into a SQLite database.
    '''

    def __init__(self, dbPath):
        self.dbPath = dbPath
        self.createTable()

    def createTable(self):
        '''
        Creates the table if it doesn't exist
        '''

        connection = sqlite3.connect(self.dbPath)
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patientRecords (
                patientId TEXT PRIMARY KEY,
                healthCardNumber TEXT,
                versionCode TEXT,
                dateOfBirth TEXT,
                serviceDate TEXT
            )
        ''')

        connection.commit()
        connection.close()

    def saveRecord(self, record):
        '''
        Inserts or updates a valid PatientRecord
        Expects a record object

        :param record: The PatientRecord object
        '''
        connection = sqlite3.connect(self.dbPath)
        cursor = connection.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO patientRecords
            (patientId, healthCardNumber, versionCode, dateOfBirth, serviceDate)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            record.patientId,
            record.healthCardNumber,
            record.versionCode,
            record.dateOfBirth,
            record.serviceDate
        ))

        connection.commit()
        connection.close()

    def insertRecords(self, records):
        '''
        Insert records into the database
        :param records: The records to insert into the database
        '''
        if not records:
            return

        connection = sqlite3.connect(self.dbPath)
        cursor = connection.cursor()

        cursor.executemany('''
            INSERT OR REPLACE INTO patientRecords
            (patientId, healthCardNumber, versionCode, dateOfBirth, serviceDate)
            VALUES (?, ?, ?, ?, ?)
        ''', [
            (
                record.patientId,
                record.healthCardNumber,
                record.versionCode,
                record.dateOfBirth,
                record.serviceDate
            )
            for record in records
        ])

        connection.commit()
        connection.close()

    def fetchAll(self):
        '''
        Returns all records from the database
        :return: The records from the database
        '''
        connection = sqlite3.connect(self.dbPath)
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM patientRecords')
        rows = cursor.fetchall()

        connection.close()
        return rows