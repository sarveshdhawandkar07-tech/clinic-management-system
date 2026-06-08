import streamlit as st
from main import Patient
import utils
from datetime import datetime

patient_manager = Patient()

st.sidebar.title("Clinic Management System")

page = st.sidebar.radio("Navigate", [
    "Add Patient",
    "Patient Records"
])

if page == "Add Patient":
    st.title("Add New Patient") # Title

    # Patient Information Section
    st.subheader("Patient Information")
    name = st.text_input("Enter Patient's Full Name")
    age = st.number_input("Age",min_value=1,max_value=120)
    weight = st.number_input("Weight(kg)",min_value=1,max_value=300)
    gender = st.selectbox("Gender",["Male","Female","Transgender"])
    contact = st.text_input("Contact Number",placeholder="e.g. +1234567890")
    address = st.text_area("Address")
    
    
    # Medical History Section
    st.subheader("Medical History")
    conditions = st.text_area("Medical Conditions")
    past_surgeries = st.text_area("Past Surgeries")
    current_medications = st.text_area("Current Medications")
    allergies = st.text_area("Allergies")
    family_history = st.text_area("Family Medical History")
    social_history = st.text_area("Social History (Smoking, Alcohol, etc.)")
    
    if st.button("Add Patient"):
        patient_manager.load_data()
        
        conditions = [c.strip() for c in conditions.split(",") if c.strip()] or ["None Reported"]
        past_surgeries = [c.strip() for c in past_surgeries.split(",") if c.strip()] or ["None Reported"]
        current_medications = [c.strip() for c in current_medications.split(",") if c.strip()] or ["None Reported"]
        allergies = [c.strip() for c in allergies.split(",") if c.strip()] or ["None Reported"]
        family_history = [c.strip() for c in family_history.split(",") if c.strip()] or ["None Reported"]
        social_history = [c.strip() for c in social_history.split(",") if c.strip()] or ["None Reported"]
        
        patient_id = utils.patient_id_generator()
        
        patient_data = {
            "patient_id": patient_id,
            "personal_information": {
            "name": name,
            "age": age,
            "weight": weight,
            "gender": gender,
            "contact": contact,
            "address": address
            },
            "past_medical_history": {
                "conditions": conditions,
                "past_surgeries": past_surgeries,
                "current_medications": current_medications,
                "allergies": allergies,
                "family_history": family_history,
                "social_history": social_history
            },
            "visits": []
        }
        patient_manager.patients.append(patient_data)
        patient_manager.save_data()
        st.success(f"Patient {name} added successfully! ID: {patient_id}")

elif page == "Patient Records":
    st.title("Patient Records")
    
    search_choice = st.radio("Search by", ["Patient ID", "Name"])
    search_info = st.text_input("Enter search value")
    
    if st.button("Search"):
        patient_manager.load_data()
        results = []
        for p in patient_manager.patients:
            if search_choice == "Patient ID":
                if p["patient_id"] == search_info:
                    results.append(p)
            else:
                if p["personal_information"]["name"].lower() == search_info.lower():
                    results.append(p)
        if results:
            st.session_state.patient_results = results
        else:
            st.error("No patient found.")

    if "patient_results" in st.session_state:
        options = [f"{p['patient_id']} - {p['personal_information']['name']}" for p in st.session_state.patient_results]
        selected = st.selectbox("Select Patient", options)
        selected_id = selected.split(" - ")[0]

        # Find selected patient
        selected_patient = next((p for p in st.session_state.patient_results if p["patient_id"] == selected_id), None)

        if selected_patient:
            # --- Buttons at top ---
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Add Visit"):
                    st.session_state.show_add_visit = True
                    st.session_state.selected_id = selected_id

            with col2:
                if st.button("Delete Patient"):
                    patient_manager.load_data()
                    patient_manager.patients = [p for p in patient_manager.patients if p["patient_id"] != selected_id]
                    patient_manager.save_data()
                    del st.session_state.patient_results
                    st.success("Patient deleted successfully.")
                    st.stop()

            # --- Add Visit Form ---
            if st.session_state.get("show_add_visit") and st.session_state.get("selected_id") == selected_id:
                st.subheader("Add Visit")
                visit_reason = st.text_input("Reason for Visit")
                symptoms = st.text_area("Symptoms")
                diagnosis = st.text_area("Diagnosis")
                treatment = st.text_area("Treatment Plan")

                if st.button("Submit Visit"):
                    patient_manager.load_data()
                    for patient in patient_manager.patients:
                        if patient["patient_id"] == selected_id:
                            patient["visits"].append({
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "reason_for_visit": visit_reason,
                                "symptoms": symptoms,
                                "diagnosis": diagnosis,
                                "treatment_plan": treatment
                            })
                            break
                    patient_manager.save_data()
                    st.success("Visit added successfully!")
                    st.session_state.show_add_visit = False

            # --- Patient Information ---
            st.subheader(f"Patient ID: {selected_patient['patient_id']}")

            st.write("**Personal Information**")
            st.write(f"**Name:** {selected_patient['personal_information']['name']}")
            st.write(f"**Age:** {selected_patient['personal_information']['age']}")
            st.write(f"**Weight:** {selected_patient['personal_information']['weight']} kg")
            st.write(f"**Gender:** {selected_patient['personal_information']['gender']}")
            st.write(f"**Contact:** {selected_patient['personal_information']['contact']}")
            st.write(f"**Address:** {selected_patient['personal_information']['address']}")

            st.write("**Past Medical History**")
            st.write(f"**Conditions:** {', '.join(selected_patient['past_medical_history']['conditions'])}")
            st.write(f"**Past Surgeries:** {', '.join(selected_patient['past_medical_history']['past_surgeries'])}")
            st.write(f"**Current Medications:** {', '.join(selected_patient['past_medical_history']['current_medications'])}")
            st.write(f"**Allergies:** {', '.join(selected_patient['past_medical_history']['allergies'])}")
            st.write(f"**Family History:** {', '.join(selected_patient['past_medical_history']['family_history'])}")
            st.write(f"**Social History:** {', '.join(selected_patient['past_medical_history']['social_history'])}")

            st.write("**Visits**")
            if selected_patient["visits"]:
                for visit in list(reversed(selected_patient["visits"])):
                    st.write(f"**Date:** {visit['date']} - **Reason:** {visit['reason_for_visit']}")
                    st.write(f"**Symptoms:** {visit['symptoms']}")
                    st.write(f"**Diagnosis:** {visit['diagnosis']}")
                    st.write(f"**Treatment Plan:** {visit['treatment_plan']}")
                    st.divider()
            else:
                st.write("No visits recorded yet.")
    
    
    
    



