import os
import subprocess
from pathlib import Path

BUCKET = os.getenv("S3_BUCKET", "qa-intelligence-reports-sathishp")
REPORT_DIR = Path("reports")

REPORT_DIR.mkdir(exist_ok=True)

print(f"Downloading reports from {BUCKET}...")

subprocess.run([
    "aws",
    "s3",
    "sync",
    f"s3://{BUCKET}",
    str(REPORT_DIR)
], check=True)

print("Reports downloaded successfully.")

for report in REPORT_DIR.glob("*.json"):
    print(f"Found: {report.name}")