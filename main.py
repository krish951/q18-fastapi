from fastapi import FastAPI, UploadFile, File, Header, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import csv
import io

app = FastAPI()

# Proper CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 88 * 1024
VALID_EXTENSIONS = {".csv", ".json", ".txt"}
REQUIRED_TOKEN = "howlprelp9ftxxnf"


@app.get("/")
def health(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {"status": "ok"}


@app.post("/upload")
async def upload_file(
    response: Response,
    file: UploadFile = File(...),
    x_upload_token_5790: str = Header(None)
):
    # 🔥 Force CORS header manually
    response.headers["Access-Control-Allow-Origin"] = "*"

    # Authentication
    if x_upload_token_5790 != REQUIRED_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # File type check
    filename = file.filename.lower()
    if not any(filename.endswith(ext) for ext in VALID_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await file.read()

    # File size check
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # CSV processing
    if filename.endswith(".csv"):
        try:
            decoded = contents.decode("utf-8")
            reader = csv.DictReader(io.StringIO(decoded))

            rows = list(reader)
            row_count = len(rows)
            columns = reader.fieldnames

            total_value = 0.0
            category_counts = {}

            for row in rows:
                total_value += float(row["value"])
                category = row["category"]
                category_counts[category] = category_counts.get(category, 0) + 1

            return {
                "email": "24f1000352@ds.study.iitm.ac.in",
                "filename": file.filename,
                "rows": row_count,
                "columns": columns,
                "totalValue": round(total_value, 2),
                "categoryCounts": category_counts
            }

        except Exception:
            raise HTTPException(status_code=400, detail="Invalid CSV format")

    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }