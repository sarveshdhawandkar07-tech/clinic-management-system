import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATIENTS_FILE = os.path.join(BASE_DIR, "patients.json")

def patient_id_generator(patients_file=PATIENTS_FILE):
    count = 0
    patients = []
    patient_id = f"{datetime.now().year}-0001"
    
    if os.path.exists(patients_file):
        with open(patients_file, "r") as f:
            try:
                patients = json.load(f)
            except json.JSONDecodeError:
                patients = []
            count = len(patients) if isinstance(patients, list) else 0 # If patients is not a list, we treat it as empty and start counting from 0
            count += 1
            patient_id = f"{datetime.now().year}-{count:04d}"
    
        while patient_id in {data.get("patient_id", "") for data in patients}: # Ensure uniqueness of patient_id
            count += 1
            patient_id = f"{datetime.now().year}-{count:04d}"

    return patient_id
    