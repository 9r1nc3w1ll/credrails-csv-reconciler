import csv
import argparse

# Input CSV headers
HEADER_ID = "ID"
HEADER_NAME = "Name"
HEADER_AMOUNT = "Amount"
HEADER_DATE = "Date"

# Output CSV headers
HEADER_TYPE = "Type"
HEADER_RECORD_ID = "Record Identifier"
HEADER_FIELD = "Field"
HEADER_SOURCE_VALUE = "Source Value"
HEADER_TARGET_VALUE = "Target Value"

def reconcile_csv(source_path, target_path, output_path):
    source_data = read_csv(source_path)
    target_data = read_csv(target_path)

    source_ids = set()
    target_ids = set()

    for record in source_data:
        source_ids.add(record["ID"])
    
    for record in target_data:
        target_ids.add(record["ID"])

    with open(output_path, "w", newline="") as csvfile:

        fieldnames = [HEADER_TYPE, HEADER_RECORD_ID, HEADER_FIELD, HEADER_SOURCE_VALUE, HEADER_TARGET_VALUE]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for id in source_ids - target_ids:
            writer.writerow({HEADER_TYPE: "Missing in Target", HEADER_RECORD_ID: id})

        for id in target_ids - source_ids:
            writer.writerow({HEADER_TYPE: "Missing in Source", HEADER_RECORD_ID: id})

        for id in source_ids & target_ids:
            source_index = find_index_by_key_value(source_data, "ID", id)
            target_index = find_index_by_key_value(target_data, "ID", id)

            if (source_index and target_index):
                if (source_data[source_index]["Date"] != target_data[target_index]["Date"]):
                    writer.writerow({
                        HEADER_TYPE: "Field Discrepancy",
                        HEADER_RECORD_ID: id,
                        HEADER_FIELD: "Date",
                        HEADER_SOURCE_VALUE: source_data[source_index]["Date"],
                        HEADER_TARGET_VALUE: target_data[source_index]["Date"]
                    })

                if (source_data[source_index]["Name"] != target_data[target_index]["Name"]):
                    writer.writerow({
                        HEADER_TYPE: "Field Discrepancy",
                        HEADER_RECORD_ID: id,
                        HEADER_FIELD: "Name",
                        HEADER_SOURCE_VALUE: source_data[source_index]["Name"],
                        HEADER_TARGET_VALUE: target_data[source_index]["Name"]
                    })

                if (source_data[source_index]["Amount"] != target_data[target_index]["Amount"]):
                    writer.writerow({
                        HEADER_TYPE: "Field Discrepancy",
                        HEADER_RECORD_ID: id,
                        HEADER_FIELD: "Amount",
                        HEADER_SOURCE_VALUE: source_data[source_index]["Amount"],
                        HEADER_TARGET_VALUE: target_data[source_index]["Amount"]
                    })

def find_index_by_key_value(lst, key, value):
    for index, item in enumerate(lst):
        if item.get(key) == value:
            return index
    return None

def read_csv(file_path):
    data = []
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            record = {
                HEADER_ID: row[HEADER_ID],
                HEADER_NAME: row[HEADER_NAME],
                HEADER_DATE: row[HEADER_DATE],
                HEADER_AMOUNT: row[HEADER_AMOUNT]
            }
            data.append(record)
    return data

def main():
    parser = argparse.ArgumentParser(description="Reconcile two CSV files.")
    parser.add_argument("-s", "--source", metavar="source_file", type=str, required=True, help="Source CSV file")
    parser.add_argument("-t", "--target", metavar="target_file", type=str, required=True, help="Target CSV file")
    parser.add_argument("-o", "--output", metavar="output_file", type=str, required=True, help="Output reconciliation report CSV file")
    args = parser.parse_args()

    reconcile_csv(args.source, args.target, args.output)
    print(f"Report saved to {args.output}")

if __name__ == "__main__":
    main()
