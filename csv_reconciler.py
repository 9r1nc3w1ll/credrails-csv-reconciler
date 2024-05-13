import csv
import argparse

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
        fieldnames = ["Type", "Record", "Identifier", "Field", "Source Value", "Target Value"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for id in source_ids - target_ids:
            writer.writerow({"Type": "Missing in Target", "Record": id})

        for id in target_ids - source_ids:
            writer.writerow({"Type": "Missing in Source", "Record": id})

        for id in source_ids & target_ids:
            s = find_index_by_key_value(source_data, "ID", id)
            t = find_index_by_key_value(target_data, "ID", id)

            if (s and t):
                if (source_data[s]["Date"] != target_data[t]["Date"]):
                    writer.writerow({
                        "Type": "Field Discrepancy",
                        "Record": id,
                        "Field": "Date",
                        "Source Value": source_data[s]["Date"],
                        "Target Value": target_data[s]["Date"]
                    })

                if (source_data[s]["Name"] != target_data[t]["Name"]):
                    writer.writerow({
                        "Type": "Field Discrepancy",
                        "Record": id,
                        "Field": "Name",
                        "Source Value": source_data[s]["Name"],
                        "Target Value": target_data[s]["Name"]
                    })

                if (source_data[s]["Amount"] != target_data[t]["Amount"]):
                    writer.writerow({
                        "Type": "Field Discrepancy",
                        "Record": id,
                        "Field": "Amount",
                        "Source Value": source_data[s]["Amount"],
                        "Target Value": target_data[s]["Amount"]
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
                "ID": row["ID"],
                "Name": row["Name"],
                "Date": row["Date"],
                "Amount": row["Amount"]
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
    print(f"Reconciliation report generated and saved to {args.output}")

if __name__ == "__main__":
    main()
