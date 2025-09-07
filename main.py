# main.py
import json
from datetime import datetime
import sys

# Load students
with open('data/students.json', 'r') as f:
    students = json.load(f)

# Load subjects
with open('data/subjects.json', 'r') as f:
    subjects = json.load(f)

# Load enrollments
with open('data/enrollments.json', 'r') as f:
    enrollments = json.load(f)

# Load attendance
try:
    with open('data/attendance.json', 'r') as f:
        attendance_data = json.load(f)
except FileNotFoundError:
    attendance_data = {}

def manual_attendance():
    print("\n--- Manual Attendance ---")
    student_id = input("Enter your Class Roll Number, University Roll Number, or Name: ").strip()
    
    matched_student = next(
        (s for s in students if s['class_roll_no'] == student_id or s['university_roll_no'] == student_id or s['name'].lower() == student_id.lower()),
        None
    )
    
    if not matched_student:
        print("Student not found!")
        return
    
    print(f"\nMarking attendance for {matched_student['name']}")
    
    # Choose subject
    print("\nAvailable Subjects:")
    for sub in subjects:
        print(f"{sub['subject_code']}: {sub['subject_name']}")
    
    sub_code = input("Enter subject code for this class: ").strip()
    matched_subject = next((s for s in subjects if s['subject_code'] == sub_code), None)
    
    if not matched_subject:
        print("Subject not found!")
        return
    
    status = input("Enter P for Present or A for Absent: ").strip().upper()
    if status not in ['P', 'A']:
        print("Invalid input!")
        return
    
    # Record attendance in Flask-compatible format
    today = datetime.now().strftime("%Y-%m-%d")
    attendance_data.setdefault(sub_code, {})
    attendance_data[sub_code][matched_student['class_roll_no']] = {
        "name": matched_student['name'],
        "status": status,
        "date": today
    }
    
    with open('data/attendance.json', 'w') as f:
        json.dump(attendance_data, f, indent=4)
    
    print(f"Attendance recorded successfully for {matched_student['name']} in {matched_subject['subject_name']}!")

def fingerprint_attendance():
    print("\nFingerprint attendance is currently disabled.")

def face_attendance():
    print("\nFace recognition attendance is currently disabled.")

def generate_report():
    print("\n--- Attendance Report ---")
    if not attendance_data:
        print("No attendance recorded yet.")
        return
    
    student_id = input("Enter your Class Roll Number, University Roll Number, or Name: ").strip()
    
    matched_student = next(
        (s for s in students if s['class_roll_no'] == student_id or s['university_roll_no'] == student_id or s['name'].lower() == student_id.lower()),
        None
    )
    
    if not matched_student:
        print("Student not found!")
        return
    
    student_records = []
    for sub_code, records in attendance_data.items():
        if matched_student['class_roll_no'] in records:
            rec = records[matched_student['class_roll_no']]
            student_records.append({
                "subject_code": sub_code,
                "subject_name": next((s['subject_name'] for s in subjects if s['subject_code'] == sub_code), sub_code),
                "status": rec['status'],
                "date": rec['date']
            })
    
    if not student_records:
        print("No attendance found for this student.")
        return
    
    total_classes = len(student_records)
    present_count = sum(1 for r in student_records if r['status'] == 'P')
    absent_count = total_classes - present_count
    percentage = (present_count / total_classes) * 100
    
    print(f"\nAttendance Report for {matched_student['name']}:")
    print(f"Total Classes: {total_classes}")
    print(f"Present: {present_count}")
    print(f"Absent: {absent_count}")
    print(f"Attendance Percentage: {percentage:.2f}%")
    print("\nClass-wise Details:")
    for rec in student_records:
        print(f"{rec['subject_name']} ({rec['subject_code']}): {rec['status']} on {rec['date']}")

def main():
    while True:
        print("\n--- Attendance Menu ---")
        print("1. Manual Attendance")
        print("2. Fingerprint Attendance (Disabled)")
        print("3. Face Recognition Attendance (Disabled)")
        print("4. Generate Report")
        print("5. Exit")
        
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            manual_attendance()
        elif choice == '2':
            fingerprint_attendance()
        elif choice == '3':
            face_attendance()
        elif choice == '4':
            generate_report()
        elif choice == '5':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    print("--- Welcome to Smart Attendance System ---")
    main()
