import utils
import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Get the directory of the current file
PATIENTS_FILE = os.path.join(BASE_DIR, "patients.json") # Define the path to the patients.json file in the same directory as the current file

class Patient:
    def __init__(self):
        self.patients = [] # Initialize patients as an empty list to store patient data

    def load_data(self): #loads the existing data to the patients list from the json file
        if os.path.exists(PATIENTS_FILE):
            with open(PATIENTS_FILE, "r") as f:
                try:
                    self.patients = json.load(f)
                except json.JSONDecodeError:
                    self.patients = [] # If the file is not valid JSON, initialize as an empty list
        else:
            self.patients = [] # If the file doesn't exist, we initialize patients as an empty list

    def save_data(self): # saves the data from patients list to the json file
        with open(PATIENTS_FILE, "w") as f:
            json.dump(self.patients, f, indent=4)
            
    def show_data(self,to_search_id= None,to_search_name= None):
        print("Results Found are :")
        result = False
        count = 0
        found_patients = []
        if to_search_id:
            for patient in self.patients:
                if to_search_id == patient["patient_id"]:
                    result = True
                    count += 1
                    found_patients.append(patient["patient_id"])
                    print(f"[{count}]  {patient["personal_information"]["name"]} | AGE: {patient["personal_information"]["age"]} | Contact No.: {patient["personal_information"]["contact"]} | ID: {patient["patient_id"]} ")
                    
                
        elif to_search_name:
            for patient in self.patients:
                if to_search_name.lower() == patient["personal_information"]["name"].lower():
                    result = True
                    count += 1
                    found_patients.append(patient["patient_id"])
                    print(f"[{count}]  {patient["personal_information"]["name"]} | AGE: {patient["personal_information"]["age"]} | Contact No.: {patient["personal_information"]["contact"]} | ID: {patient["patient_id"]} ")
        
        if not result:
            print("Sorry No results found")
        
        return found_patients
    
    def validate_medical_dataInput(self,items,field_name):
        if not items or items == [""]:
            items = ["None Reported"]
        else:
            items = [item.strip() for item in items if item.strip()]
            if not items:
                items = ["None Reported"]
        if any(not(char.isdigit() or  char.isalpha() or char.isspace() or char in {"-","_",".","(",")","[","]","{","}"})for item in items  for char in item ):
            print(f"Invalid input. {field_name} should only contain letters, numbers, spaces, hyphens,dots and brackets.")
            return None
        return items
    
    


    
    def add_patient(self):
        self.load_data() # Load existing data before adding a new patient   
        
        """Personal Information"""
        try:
            name = input("Enter patient's name: ").title()
            if not name or any(char.isdigit() for char in name) or any(not char.isalnum() and not char.isspace() for char in name) or len(name) > 100 or len(name) < 2 or name.lower() in ["unknown", "n/a", "none"] or name.strip() == "" or name[0].isspace() or name[-1].isspace():
                print("Invalid name. Please enter a valid patient name.")
                return
            age = int(input("Enter patient's age:(0-120) :"))
            if age not in range(0,121):
                print("Invalid age. Please enter a value between 0 and 120.")
                return
            weight = float(input("Enter patient's weight (kg): "))
            if weight <= 0 or weight > 300:
                print("Invalid weight. Please enter a value greater than 0 and less than or equal to 300 kg.")
                return
            gender = input("Enter patient's gender: ").strip().capitalize()
            if gender.lower() not in ["male","female","transgender"]:
                print("Invalid gender. Please enter 'male', 'female', or 'transgender'.")
                return
            contact = input("Enter patient's contact number: ").strip()
            if not contact.isdigit() or len(contact) != 10:
                print("Invalid contact number. Please enter a 10-digit number.")
                return
            address = input("Enter patient's address: ")
            if not address.strip() or len(address.strip())<5:
                print("Invalid address. Please enter a valid address with at least 5 characters.")
                return
        except ValueError:
            print("Invalid input. Please enter valid values.")
            return

        """Past Medical History"""
        conditions = input("Enter Patient's Medical Conditions(comma-separated): ").split(",")
        conditions = self.validate_medical_dataInput(conditions,"Medical conditions")
        if conditions is None:
            return
        past_surgeries = input("Enter Patient's Past Surgeries(comma-separated): ").split(",")
        past_surgeries = self.validate_medical_dataInput(past_surgeries,"Past Surgeries")
        if past_surgeries is None:
            return
        current_medications = input("Enter Patient's Current Medications(comma-separated): ").split(",")
        current_medications = self.validate_medical_dataInput(current_medications,"Current Medications")
        if current_medications is None:
            return
        allergies = input("Enter Patient's Allergies(comma-separated): ").split(",")
        allergies = self.validate_medical_dataInput(allergies,"Allergies")
        if allergies is None:
            return
        family_history = input("Enter Patient's Family History(comma-separated): ").split(",")
        family_history = self.validate_medical_dataInput(family_history,"Family History")
        if family_history is None:
            return
        social_history = input("Enter Patient's Social History(comma-separated): ").split(",")
        social_history = self.validate_medical_dataInput(social_history,"Social History")
        if social_history is None:
            return

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
        
        self.patients.append(patient_data)
        self.save_data()
        print(f"Patient {name} added with ID: {patient_id}")
        
    def search_patient(self):
        self.load_data()
        try:
            search_choice = input("How do you want to search 1.PATIENT ID 2.NAME : ")
            if search_choice not in ["1","2"]:
                print("Invalid choice. Please enter '1' or '2'.")
                return []
        except ValueError:
            print("Invalid input. Please enter a valid choice.")
            return []
        if search_choice == "1" :
            try:
                search_info = input("Enter the Patient's ID :")
                if not search_info:                    
                    print("Patient ID cannot be empty. Please enter a valid patient ID.")
                    return [] 
                elif len(search_info) != 9 or not search_info[5:].isdigit() or search_info[4] != '-' or not search_info[:4].isdigit():
                    print("Invalid patient ID format. Please enter a valid patient ID in the format 'YYYY-XXXX'.")
                    return []
            except ValueError:
                print("Invalid input. Please enter a valid patient ID.")
                return []
            return self.show_data(to_search_id=search_info)
        elif search_choice == "2" :
            try:
                search_info = input("Enter the Patient's Name :")
                if not search_info:
                    print("Patient name cannot be empty. Please enter a valid patient name.")
                    return []
                if any(char.isdigit() for char in search_info):
                    print("Patient name cannot contain numbers. Please enter a valid patient name.")
                    return []
                if any(not char.isalnum() and not char.isspace() for char in search_info):
                    print("Patient name cannot contain special characters. Please enter a valid patient name.")
                    return []
                if len(search_info) > 100:
                    print("Patient name is too long. Please enter a name with 100 characters or fewer.")
                    return []
                if len(search_info) < 2:
                    print("Patient name is too short. Please enter a name with at least 2 characters.")
                    return []
                if search_info.lower() in ["unknown", "n/a", "none"]:
                    print("Patient name cannot be 'unknown', 'n/a', or 'none'. Please enter a valid patient name.")
                    return []
                if search_info.strip() == "":
                    print("Patient name cannot be just whitespace. Please enter a valid patient name.")
                    return []
                if search_info[0].isspace() or search_info[-1].isspace():
                    print("Patient name cannot start or end with whitespace. Please enter a valid patient name.")
                    return []
            except ValueError:
                print("Invalid input. Please enter a valid patient name.")
                return []
            return self.show_data(to_search_name=search_info)
        return []
    
    def delete_patient(self):
        found_patients = self.search_patient()
        if not found_patients:
            print("No patient found with the given information.") 
            return
        try:
            choice = int(input("Select the patient (if none, enter 0):"))
            if choice < 0 or choice > len(found_patients):
                print("Invalid choice. Please select a valid patient number.")
                return
            if choice == 0:
                print("No patient selected. Returning to main menu.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid choice.")
            return
        confirm = input("Are you sure you want to delete this patient :(yes/no)").strip()
        if confirm.lower() == "yes":
            self.patients = [p for p in self.patients if found_patients[choice-1] != p["patient_id"]]
            self.save_data()
            print("Patient Removed from records successfully")
        elif confirm.lower() == "no":
            print("Patient deletion cancelled.")
            return
        else :
            print("Invalid input. Please enter 'yes' or 'no'.")
            return
        

    
    def add_visit(self):
        found_patients = self.search_patient()
        if not found_patients:
            print("No patient found with the given information.")
            return
        try:
            choice = int(input("Select the patient (if none, enter 0):"))
            if choice < 0 or choice > len(found_patients):
                print("Invalid choice. Please select a valid patient number.")
                return
            if choice == 0:
                print("No patient selected. Returning to main menu.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid choice.")
            return
        for patient in self.patients:
            if (found_patients[choice-1] == patient["patient_id"]):
                date = datetime.now().strftime("%Y-%m-%d %H:%M")
                try:
                    visit_reason = input("Enter the reason for visit: ")
                    symptoms = input("Enter the Symptoms: ")
                    diagnosis = input("Enter the diagnosis: ")
                    treatment = input("Enter the Treatment Plan: ")
                except ValueError:
                    print("Invalid input. Please enter valid values.")
                    return

                patient["visits"].append({"date" : date,
                                          "reason_for_visit" : visit_reason,
                                          "symptoms" : symptoms,
                                          "diagnosis" : diagnosis,
                                          "treatment_plan" : treatment})
                break
        self.save_data()
        print("Visit Added successfully")

    def view_patient(self):
        found_patients = self.search_patient()
        if not found_patients:
            print("No patient found with the given information.")
            return
        try:
            choice = int(input("Select the patient (if none, enter 0):"))
            if choice < 0 or choice > len(found_patients):
                print("Invalid choice. Please select a valid patient number.")
                return
            if choice == 0:
                print("No patient selected. Returning to main menu.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid choice.")
            return
        for patient in self.patients:
             if (found_patients[choice-1] == patient["patient_id"]):
                print("Personal Information".center(50,"-"))
                print(f"Name: {patient['personal_information']['name']}")
                print(f"Age: {patient['personal_information']['age']}")
                print(f"Weight: {patient['personal_information']['weight']} kg")
                print(f"Gender: {patient['personal_information']['gender']}")
                print(f"Contact: {patient['personal_information']['contact']}")
                print(f"Address: {patient['personal_information']['address']}")

                print("\nPast Medical History".center(50,"-"))
                print(f"Conditions: {', '.join(patient['past_medical_history']['conditions'])}")
                print(f"Past Surgeries: {', '.join(patient['past_medical_history']['past_surgeries'])}")
                print(f"Current Medications: {', '.join(patient['past_medical_history']['current_medications'])}")
                print(f"Allergies: {', '.join(patient['past_medical_history']['allergies'])}")
                print(f"Family History: {', '.join(patient['past_medical_history']['family_history'])}")
                print(f"Social History: {', '.join(patient['past_medical_history']['social_history'])}")

                print("\nVisits".center(50,"-"))
                for visit in reversed(patient['visits']):
                    print(f"Date: {visit['date']}")
                    print(f"Reason for Visit: {visit['reason_for_visit']}")
                    print(f"Symptoms: {visit['symptoms']}")
                    print(f"Diagnosis: {visit['diagnosis']}")
                    print(f"Treatment Plan: {visit['treatment_plan']}")
                    print("-" * 50)
                



if __name__ == "__main__":
    patient_manager = Patient()
    while True:
        print("\nClinic Management System")
        print("1. Add New Patient")
        print("2. Search Patient")
        print("3. Add Visit")
        print("4. View Patient Details")
        print("5. Delete Patient")
        print("6. Exit")
        
        
        choice = input("Enter your choice: ").strip()
    
        if choice == "1":
            patient_manager.add_patient()
        elif choice == "2":
            patient_manager.search_patient()
        elif choice == "3":
            patient_manager.add_visit()
        elif choice == "4":
            patient_manager.view_patient()
        elif choice == "5":
            patient_manager.delete_patient()
        elif choice == "6":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
    
