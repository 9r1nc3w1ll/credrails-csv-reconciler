import unittest
import csv
from csv_reconciler import reconcile_csv, HEADER_TYPE, HEADER_RECORD_ID, HEADER_FIELD, HEADER_SOURCE_VALUE, HEADER_TARGET_VALUE

class TestReconcileCSV(unittest.TestCase):
    def test_reconcile_csv(self):
        reconcile_csv("input/source.csv", "input/target.csv", "output.csv")

        output_data = []
        with open("output.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                record = {
                    HEADER_TYPE: row[HEADER_TYPE],
                    HEADER_RECORD_ID: row[HEADER_RECORD_ID],
                    HEADER_FIELD: row[HEADER_FIELD],
                    HEADER_SOURCE_VALUE: row[HEADER_SOURCE_VALUE],
                    HEADER_TARGET_VALUE: row[HEADER_TARGET_VALUE],
                }
                output_data.append(record)
        
        self.assertEqual(len(output_data), 3)
        self.assertEqual(output_data[0][HEADER_TYPE], "Missing in Target")
        self.assertEqual(output_data[0][HEADER_RECORD_ID], "003")
        self.assertEqual(output_data[1][HEADER_TYPE], "Missing in Source")
        self.assertEqual(output_data[1][HEADER_RECORD_ID], "004")
        self.assertEqual(output_data[2][HEADER_TYPE], "Field Discrepancy")
        self.assertEqual(output_data[2][HEADER_RECORD_ID], "002")
        self.assertEqual(output_data[2][HEADER_FIELD], "Date")
        self.assertEqual(output_data[2][HEADER_SOURCE_VALUE], "2023-01-02")
        self.assertEqual(output_data[2][HEADER_TARGET_VALUE], "2023-01-04")

if __name__ == '__main__':
    unittest.main()
