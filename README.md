# Clinic Management System

A web-based patient record management system built for single-doctor clinics. Built with Python and Streamlit.

## 🔗 Live Demo
[Click here to use the app](https://clinic-management-system-mgavwty2utuozcyvkuh9yf.streamlit.app/)

## Features
- Register new patients with a permanent unique Patient ID (auto-generated)
- Store complete patient profile — personal information and past medical history
- Search patients by name or Patient ID
- View complete patient details instantly after search
- Add visit records — reason, symptoms, diagnosis, treatment plan
- Delete patient records with confirmation
- All data persists across sessions

## Tech Used
- Python
- Streamlit
- JSON for data storage

## How to Run Locally

1. Clone the repository
```
git clone https://github.com/sarveshdhawandkar07-tech/clinic-management-system.git
```

2. Install dependencies
```
pip install streamlit
```

3. Run the app
```
streamlit run app.py
```

## Project Structure
```
clinic-management-system/
├── app.py          # Streamlit web interface
├── main.py         # Core logic and Patient class
├── utils.py        # Helper functions (ID generation)
├── requirements.txt
└── README.md
```

## Author
Sarvesh Dhawandkar — First Year AI & Data Science Engineering Student