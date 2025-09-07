from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

# Load students, subjects, and attendance data
with open('data/students.json') as f:
    students = json.load(f)

with open('data/subjects.json') as f:
    subjects = json.load(f)

# Initialize attendance.json if empty
try:
    with open('data/attendance.json') as f:
        attendance = json.load(f)
except FileNotFoundError:
    attendance = {}

# ---------------- Home ----------------
@app.route('/')
def index():
    return render_template('index.html')

# ---------------- Teacher Dashboard ----------------
@app.route('/teacher_dashboard', methods=['GET', 'POST'])
def teacher_dashboard():
    message = None
    if request.method == 'POST':
        roll_no = request.form['roll_no']
        status = request.form['status']
        subject_code = request.form['subject']
        today = datetime.now().strftime("%Y-%m-%d")

        # Find student
        student = next((s for s in students if s['class_roll_no'] == roll_no), None)
        if student:
            attendance.setdefault(subject_code, {})
            attendance[subject_code][roll_no] = {
                'name': student['name'],
                'status': 'Present' if status == 'P' else 'Absent',
                'date': today
            }
            with open('data/attendance.json', 'w') as f:
                json.dump(attendance, f, indent=4)
            message = f"Attendance marked for {student['name']} as {'Present' if status == 'P' else 'Absent'}"
        else:
            message = "Student not found!"

    return render_template('teacher_dashboard.html',
                           students=students,
                           subjects=subjects,
                           attendance=attendance,
                           message=message)

# ---------------- Student Login ----------------
@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    error = None
    if request.method == 'POST':
        uni_roll_no = request.form.get('uni_roll_no', '').strip()
        name_input = request.form.get('name', '').strip()

        student = next(
            (s for s in students if s['uni_roll_no'] == uni_roll_no and s['name'].lower() == name_input.lower()),
            None
        )
        if student:
            return redirect(url_for('student_attendance', roll_no=student['class_roll_no']))
        else:
            error = "Student not found! Check University Roll No and Name."
    return render_template('student_login.html', error=error)

# ---------------- Student Attendance ----------------
@app.route('/student_attendance/<roll_no>', methods=['GET'])
def student_attendance(roll_no):
    student = next((s for s in students if s['class_roll_no'] == roll_no), None)
    if not student:
        return redirect(url_for('student_login'))

    # Filter attendance for this student
    student_attendance_data = {}
    for subj in subjects:
        records = attendance.get(subj['subject_code'], {})
        if roll_no in records:
            student_attendance_data[subj['subject_code']] = records[roll_no]

    return render_template('student_attendance.html',
                           student=student,
                           subjects=subjects,
                           attendance=student_attendance_data)

# ---------------- Attendance Report ----------------
@app.route('/report')
def report():
    return render_template('report.html', attendance=attendance, students=students, subjects=subjects)

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
