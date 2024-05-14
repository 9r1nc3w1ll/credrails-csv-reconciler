import unittest
import csv
import io
from csv_reconciler import reconcile_csv

class TestReconcileCSV(unittest.TestCase):
    def test_reconcile_csv(self):
        reconcile_csv("input/source.csv", "input/target.csv", "output.csv")

        output_data = []
        with open("output.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                record = {
                    "Type": row["Type"],
                    "Record Identifier": row["Record Identifier"],
                    "Field": row["Field"],
                    "Source Value": row["Source Value"],
                    "Target Value": row["Target Value"],
                }
                output_data.append(record)
        
        self.assertEqual(len(output_data), 3)
        self.assertEqual(output_data[0]["Type"], "Missing in Target")
        self.assertEqual(output_data[0]["Record Identifier"], "003")
        self.assertEqual(output_data[1]["Type"], "Missing in Source")
        self.assertEqual(output_data[1]["Record Identifier"], "004")
        self.assertEqual(output_data[2]["Type"], "Field Discrepancy")
        self.assertEqual(output_data[2]["Record Identifier"], "002")
        self.assertEqual(output_data[2]["Field"], "Date")
        self.assertEqual(output_data[2]["Source Value"], "2023-01-02")
        self.assertEqual(output_data[2]["Target Value"], "2023-01-04")

if __name__ == '__main__':
    unittest.main()
