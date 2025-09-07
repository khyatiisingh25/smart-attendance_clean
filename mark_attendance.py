# mark_attendance.py
import json
from datetime import datetime

# Paths to JSON files
STUDENTS_FILE = 'data/students.json'
SUBJECTS_FILE = 'data/subjects.json'
ATTENDANCE_FILE = 'data/attendance.json'
FINGERPRINTS_FILE = 'data/fingerprints.json'  # optional

# Load students
with open(STUDENTS_FILE, 'r') as f:
    students = json.load(f)

# Load subjects
with open(SUBJECTS_FILE, 'r') as f:
    subjects = json.load(f)

# Load fingerprints (optional)
try:
    with open(FINGERPRINTS_FILE, 'r') as f:
        fingerprints = json.load(f)
except FileNotFoundError:
    fingerprints = {}

# Load attendance
try:
    with open(ATTENDANCE_FILE, 'r') as f:
        attendance = json.load(f)
except FileNotFoundError:
    attendance = {}

# ---------- Helper Functions ----------
def find_student(student_id):
    student_id = student_id.strip()
    for s in students:
        if student_id == s['class_roll_no'] or student_id == s['university_roll_no'] or student_id.lower() == s['name'].lower():
            return s
    return None

def find_subject(subject_code):
    subject_code = subject_code.strip()
    for s in subjects:
        if subject_code == s['subject_code']:
            return s
    return None

def save_attendance():
    with open(ATTENDANCE_FILE, 'w') as f:
        json.dump(attendance, f, indent=4)
    print(f"Attendance saved in {ATTENDANCE_FILE}")

# ---------- Manual Attendance ----------
def manual_attendance():
    print("\n--- Manual Attendance ---")
    student_id = input("Enter Class Roll No, University Roll No, or Name: ").strip()
    student = find_student(student_id)
    if not student:
        print("Student not found!")
        return
    
    print("\nAvailable Subjects:")
    for s in subjects:
        print(f"{s['subject_code']}: {s['subject_name']}")
    subject_code = input("Enter Subject Code: ").strip()
    subject = find_subject(subject_code)
    if not subject:
        print("Subject not found!")
        return
    
    status = input("Enter P for Present or A for Absent: ").strip().upper()
    if status not in ['P', 'A']:
        print("Invalid input! Defaulting to Absent.")
        status = 'A'
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    attendance.setdefault(subject_code, {})
    attendance[subject_code][student['class_roll_no']] = {
        "name": student['name'],
        "status": status,
        "date": today,
        "method": "Manual"
    }
    save_attendance()
    print(f"Attendance marked for {student['name']} in {subject['subject_name']}.")

# ---------- Fingerprint Attendance ----------
def fingerprint_attendance():
    print("\n--- Fingerprint Attendance ---")
    if not fingerprints:
        print("No fingerprints found!")
        return
    
    today = datetime.now().strftime("%Y-%m-%d")
    subject_code = input("Enter Subject Code for this class: ").strip()
    subject = find_subject(subject_code)
    if not subject:
        print("Subject not found!")
        return
    
    for roll, data in fingerprints.items():
        attendance.setdefault(subject_code, {})
        if roll in attendance[subject_code]:
            continue  # already marked
        print(f"Detected fingerprint for {data['name']}")
        attendance[subject_code][roll] = {
            "name": data['name'],
            "status": "P",
            "date": today,
            "method": "Fingerprint"
        }
    save_attendance()
    print("Fingerprint attendance completed!")

# ---------- Generate Report ----------
def generate_report():
    print("\n--- Attendance Report ---")
    student_id = input("Enter Class Roll No, University Roll No, or Name: ").strip()
    student = find_student(student_id)
    if not student:
        print("Student not found!")
        return
    
    print(f"\nAttendance Report for {student['name']} (Roll {student['class_roll_no']}):")
    
    total_classes = 0
    total_present = 0
    
    for subject in subjects:
        sub_code = subject['subject_code']
        sub_name = subject['subject_name']
        records = attendance.get(sub_code, {})
        student_record = records.get(student['class_roll_no'])
        if student_record:
            status = "Present" if student_record['status'] == 'P' else "Absent"
            date = student_record['date']
            method = student_record.get('method', 'Unknown')
            print(f"{sub_name} ({sub_code}): {status} on {date} ({method})")
            total_classes += 1
            if status == "Present":
                total_present += 1
        else:
            print(f"{sub_name} ({sub_code}): Not marked")
    
    percentage = (total_present / total_classes * 100) if total_classes > 0 else 0
    print(f"\nTotal Classes: {total_classes}")
    print(f"Present: {total_present}")
    print(f"Absent: {total_classes - total_present}")
    print(f"Attendance Percentage: {percentage:.2f}%")

# ---------- Menu ----------
def attendance_menu():
    while True:
        print("\n--- Attendance Menu ---")
        print("1. Manual Attendance")
        print("2. Fingerprint Attendance")
        print("3. Generate Report")
        print("4. Exit")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            manual_attendance()
        elif choice == '2':
            fingerprint_attendance()
        elif choice == '3':
            generate_report()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

# ---------- Main ----------
if __name__ == "__main__":
    print("--- Welcome to Smart Attendance System (CLI) ---")
    attendance_menu()
