from fastapi import FastAPI, UploadFile, File
import csv

app = FastAPI()


@app.post("/reconcilation-report")
async def reconcilation_report(source: UploadFile = File(...), target: UploadFile = File(...)):
    data = []
    for file in [source, target]:
        if file.filename and file.filename.endswith(".csv"):
            contents = await file.read()
            decoded_contents = contents.decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_contents, delimiter=",")
            for row in reader:
                record = {
                    "ID": row["ID"],
                    "Name": row["Name"],
                    "Date": row["Date"],
                    "Amount": float(row["Amount"])
                }
                data.append(record)
        else:
            return {"error": "Only CSV files are allowed"}

    return data