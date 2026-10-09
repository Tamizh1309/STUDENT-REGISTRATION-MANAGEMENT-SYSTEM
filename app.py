import os
import csv
from io import StringIO, TextIOWrapper
from datetime import datetime, date, timezone
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'student_mgmt_secret_key_2026_super_secure')

# File Upload Settings
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max upload

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database Configuration (Dual Mode)
MYSQL_USER = os.getenv('MYSQL_USER', '')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_DB = os.getenv('MYSQL_DB', 'student_db')

if MYSQL_USER and MYSQL_PASSWORD:
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
else:
    db_path = os.path.join(app.root_path, 'students.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------- DATABASE MODELS -----------------



class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    address = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='Active', nullable=False)
    profile_image = db.Column(db.String(255), nullable=True)
    
    # Financial fields
    total_fee = db.Column(db.Float, default=50000.0)
    paid_fee = db.Column(db.Float, default=0.0)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    grades = db.relationship('Grade', backref='student', cascade='all, delete-orphan', lazy=True)
    attendance_records = db.relationship('Attendance', backref='student', cascade='all, delete-orphan', lazy=True)

    @property
    def pending_fee(self):
        return max(0.0, (self.total_fee or 0.0) - (self.paid_fee or 0.0))

    @property
    def attendance_percentage(self):
        total = len(self.attendance_records)
        if total == 0:
            return 100.0
        present = sum(1 for a in self.attendance_records if a.status in ['Present', 'Late'])
        return round((present / total) * 100, 1)

    @property
    def gpa(self):
        if not self.grades:
            return 0.0
        total_pct = sum((g.marks_obtained / g.max_marks * 100) for g in self.grades if g.max_marks > 0)
        avg = total_pct / len(self.grades)
        # Convert to 4.0 GPA scale
        return round((avg / 100) * 4.0, 2)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'course': self.course,
            'gender': self.gender,
            'dob': self.dob.strftime('%Y-%m-%d') if self.dob else '',
            'address': self.address,
            'status': self.status,
            'profile_image': self.profile_image,
            'total_fee': self.total_fee,
            'paid_fee': self.paid_fee,
            'pending_fee': self.pending_fee,
            'attendance_percentage': self.attendance_percentage,
            'gpa': self.gpa,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''
        }


class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(30), nullable=False, default='Semester 1')
    marks_obtained = db.Column(db.Float, nullable=False)
    max_marks = db.Column(db.Float, nullable=False, default=100.0)
    grade_letter = db.Column(db.String(5), nullable=False, default='A')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(20), nullable=False, default='Present')  # Present, Absent, Late, Excused
    remarks = db.Column(db.String(255), nullable=True)


# Seed Sample Data Function
def seed_sample_data():
    if Student.query.count() == 0:
        samples = [
            Student(
                student_id="STU2026001",
                full_name="Aarav Sharma",
                email="aarav.sharma@example.com",
                phone="+91 98765 43210",
                course="Computer Science",
                gender="Male",
                dob=datetime.strptime("2003-05-15", "%Y-%m-%d").date(),
                address="12 MG Road, Bengaluru, Karnataka",
                status="Active",
                total_fee=60000.0,
                paid_fee=60000.0
            ),
            Student(
                student_id="STU2026002",
                full_name="Priya Ananth",
                email="priya.a@example.com",
                phone="+91 98123 45678",
                course="Information Technology",
                gender="Female",
                dob=datetime.strptime("2002-11-20", "%Y-%m-%d").date(),
                address="45 Anna Salai, Chennai, Tamil Nadu",
                status="Active",
                total_fee=55000.0,
                paid_fee=40000.0
            ),
            Student(
                student_id="STU2026003",
                full_name="Rohan Verma",
                email="rohan.verma@example.com",
                phone="+91 97654 32109",
                course="Data Science",
                gender="Male",
                dob=datetime.strptime("2004-01-10", "%Y-%m-%d").date(),
                address="88 Park Street, Kolkata, West Bengal",
                status="Active",
                total_fee=65000.0,
                paid_fee=30000.0
            ),
            Student(
                student_id="STU2026004",
                full_name="Ananya Iyer",
                email="ananya.iyer@example.com",
                phone="+91 99887 76655",
                course="Electronics & Communication",
                gender="Female",
                dob=datetime.strptime("2003-08-04", "%Y-%m-%d").date(),
                address="22 FC Road, Pune, Maharashtra",
                status="Active",
                total_fee=50000.0,
                paid_fee=50000.0
            ),
            Student(
                student_id="STU2026005",
                full_name="Vikramaditya Das",
                email="vikram.das@example.com",
                phone="+91 91234 56789",
                course="Business Analytics",
                gender="Male",
                dob=datetime.strptime("2002-03-29", "%Y-%m-%d").date(),
                address="79 Civil Lines, Jaipur, Rajasthan",
                status="On Leave",
                total_fee=52000.0,
                paid_fee=25000.0
            ),
            Student(
                student_id="STU2026006",
                full_name="Meera Pillai",
                email="meera.pillai@example.com",
                phone="+91 94455 66778",
                course="Computer Science",
                gender="Female",
                dob=datetime.strptime("2003-12-14", "%Y-%m-%d").date(),
                address="34 Kowdiar, Thiruvananthapuram, Kerala",
                status="Active",
                total_fee=60000.0,
                paid_fee=60000.0
            ),
            Student(
                student_id="STU2026007",
                full_name="Karthik Raju",
                email="karthik.raju@example.com",
                phone="+91 93344 55667",
                course="Mechanical Engineering",
                gender="Male",
                dob=datetime.strptime("2002-07-19", "%Y-%m-%d").date(),
                address="102 Banjara Hills, Hyderabad, Telangana",
                status="Graduated",
                total_fee=58000.0,
                paid_fee=58000.0
            ),
        ]
        db.session.add_all(samples)
        db.session.commit()

        # Seed sample grades and attendance for Aarav & Priya
        g1 = Grade(student_id=1, subject_name="Data Structures & Algorithms", semester="Sem 1", marks_obtained=92.0, max_marks=100.0, grade_letter="A+")
        g2 = Grade(student_id=1, subject_name="Database Management Systems", semester="Sem 1", marks_obtained=88.0, max_marks=100.0, grade_letter="A")
        g3 = Grade(student_id=2, subject_name="Web Architecture", semester="Sem 1", marks_obtained=95.0, max_marks=100.0, grade_letter="A+")
        g4 = Grade(student_id=3, subject_name="Applied Statistics", semester="Sem 1", marks_obtained=85.0, max_marks=100.0, grade_letter="A")

        att1 = Attendance(student_id=1, attendance_date=date.today(), status='Present', remarks='On time')
        att2 = Attendance(student_id=2, attendance_date=date.today(), status='Present', remarks='On time')
        att3 = Attendance(student_id=3, attendance_date=date.today(), status='Absent', remarks='Medical leave')

        db.session.add_all([g1, g2, g3, g4, att1, att2, att3])
        db.session.commit()

# Ensure database tables and sample data exist when imported by Gunicorn or run locally
with app.app_context():
    db.create_all()
    seed_sample_data()

# Context Processor for layout helpers
@app.context_processor
def inject_now():
    return {'now': datetime.now(timezone.utc)}


# ----------------- ROUTES -----------------

@app.route('/')
def dashboard():
    total_students = Student.query.count()
    active_students = Student.query.filter_by(status='Active').count()
    on_leave = Student.query.filter_by(status='On Leave').count()
    graduated = Student.query.filter_by(status='Graduated').count()
    
    # Financial metrics
    total_fee_collected = db.session.query(func.sum(Student.paid_fee)).scalar() or 0.0
    total_fee_pending = db.session.query(func.sum(Student.total_fee - Student.paid_fee)).scalar() or 0.0

    # Course breakdown data
    courses = db.session.query(Student.course, func.count(Student.id)).group_by(Student.course).all()
    course_names = [c[0] for c in courses]
    course_counts = [c[1] for c in courses]

    recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()

    return render_template(
        'dashboard.html',
        total_students=total_students,
        active_students=active_students,
        on_leave=on_leave,
        graduated=graduated,
        total_fee_collected=total_fee_collected,
        total_fee_pending=total_fee_pending,
        courses=courses,
        course_names=course_names,
        course_counts=course_counts,
        recent_students=recent_students
    )

@app.route('/students')
def list_students():
    search_query = request.args.get('search', '').strip()
    course_filter = request.args.get('course', '').strip()
    status_filter = request.args.get('status', '').strip()
    
    query = Student.query

    if search_query:
        query = query.filter(
            or_(
                Student.full_name.ilike(f'%{search_query}%'),
                Student.student_id.ilike(f'%{search_query}%'),
                Student.email.ilike(f'%{search_query}%'),
                Student.phone.ilike(f'%{search_query}%')
            )
        )
    if course_filter:
        query = query.filter_by(course=course_filter)
    if status_filter:
        query = query.filter_by(status=status_filter)

    students = query.order_by(Student.student_id.asc()).all()
    all_courses = db.session.query(Student.course).distinct().all()
    course_list = [c[0] for c in all_courses]

    return render_template(
        'students.html',
        students=students,
        search_query=search_query,
        course_filter=course_filter,
        status_filter=status_filter,
        course_list=course_list
    )

@app.route('/students/register', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip()
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        course = request.form.get('course', '').strip()
        gender = request.form.get('gender', '').strip()
        dob_str = request.form.get('dob', '').strip()
        address = request.form.get('address', '').strip()
        status = request.form.get('status', 'Active').strip()
        total_fee = float(request.form.get('total_fee', 50000.0) or 50000.0)
        paid_fee = float(request.form.get('paid_fee', 0.0) or 0.0)

        # Handle Profile Picture Upload
        profile_image_filename = None
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename and allowed_file(file.filename):
                fname = secure_filename(file.filename)
                profile_image_filename = f"{student_id}_{fname}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_image_filename))

        # Validation
        errors = []
        if not student_id:
            errors.append("Student ID is required.")
        elif Student.query.filter_by(student_id=student_id).first():
            errors.append(f"Student ID '{student_id}' is already registered.")

        if not full_name:
            errors.append("Full Name is required.")
        if not email:
            errors.append("Email Address is required.")
        elif Student.query.filter_by(email=email).first():
            errors.append(f"Email address '{email}' is already registered.")

        if not phone:
            errors.append("Phone number is required.")
        if not course:
            errors.append("Course selection is required.")
        if not gender:
            errors.append("Gender selection is required.")
        if not dob_str:
            errors.append("Date of birth is required.")

        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
        except ValueError:
            errors.append("Invalid date format. Please use YYYY-MM-DD.")

        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('student_form.html', student=request.form, is_edit=False)

        new_student = Student(
            student_id=student_id,
            full_name=full_name,
            email=email,
            phone=phone,
            course=course,
            gender=gender,
            dob=dob,
            address=address,
            status=status,
            total_fee=total_fee,
            paid_fee=paid_fee,
            profile_image=profile_image_filename
        )

        db.session.add(new_student)
        db.session.commit()

        flash(f"Student '{full_name}' ({student_id}) registered successfully!", "success")
        return redirect(url_for('list_students'))

    # Auto-generate next suggested Student ID
    last_student = Student.query.order_by(Student.id.desc()).first()
    next_num = (last_student.id + 1) if last_student else 1
    suggested_id = f"STU2026{next_num:03d}"

    return render_template('student_form.html', student={'student_id': suggested_id, 'total_fee': 50000.0, 'paid_fee': 0.0}, is_edit=False)

@app.route('/students/<int:id>')
def view_student(id):
    student = db.get_or_404(Student, id)
    grades = Grade.query.filter_by(student_id=id).order_by(Grade.created_at.desc()).all()
    attendance_list = Attendance.query.filter_by(student_id=id).order_by(Attendance.attendance_date.desc()).all()
    return render_template('student_detail.html', student=student, grades=grades, attendance_list=attendance_list)

@app.route('/students/<int:id>/edit', methods=['GET', 'POST'])
def edit_student(id):
    student = db.get_or_404(Student, id)

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        course = request.form.get('course', '').strip()
        gender = request.form.get('gender', '').strip()
        dob_str = request.form.get('dob', '').strip()
        address = request.form.get('address', '').strip()
        status = request.form.get('status', 'Active').strip()
        total_fee = float(request.form.get('total_fee', student.total_fee or 50000.0))
        paid_fee = float(request.form.get('paid_fee', student.paid_fee or 0.0))

        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename and allowed_file(file.filename):
                fname = secure_filename(file.filename)
                profile_image_filename = f"{student.student_id}_{fname}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_image_filename))
                student.profile_image = profile_image_filename

        errors = []
        if not full_name:
            errors.append("Full Name is required.")
        if not email:
            errors.append("Email Address is required.")
        else:
            existing_email = Student.query.filter(Student.email == email, Student.id != id).first()
            if existing_email:
                errors.append(f"Email '{email}' is already taken by another student.")

        if not phone:
            errors.append("Phone number is required.")
        if not course:
            errors.append("Course is required.")

        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else student.dob
        except ValueError:
            errors.append("Invalid date format.")

        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('student_form.html', student=request.form, is_edit=True, student_obj=student)

        student.full_name = full_name
        student.email = email
        student.phone = phone
        student.course = course
        student.gender = gender
        student.dob = dob
        student.address = address
        student.status = status
        student.total_fee = total_fee
        student.paid_fee = paid_fee

        db.session.commit()

        flash(f"Student record for '{student.full_name}' updated successfully!", "success")
        return redirect(url_for('view_student', id=student.id))

    return render_template('student_form.html', student=student.to_dict(), is_edit=True, student_obj=student)

@app.route('/students/<int:id>/delete', methods=['POST'])
def delete_student(id):
    student = db.get_or_404(Student, id)
    name = student.full_name
    student_id = student.student_id
    
    db.session.delete(student)
    db.session.commit()

    flash(f"Student '{name}' ({student_id}) was successfully deleted.", "info")
    return redirect(url_for('list_students'))

# --- Grade Management Route ---
@app.route('/students/<int:id>/grades/add', methods=['POST'])
def add_grade(id):
    student = db.get_or_404(Student, id)
    subject_name = request.form.get('subject_name', '').strip()
    semester = request.form.get('semester', 'Semester 1').strip()
    marks_obtained = float(request.form.get('marks_obtained', 0))
    max_marks = float(request.form.get('max_marks', 100))

    if not subject_name:
        flash("Subject name is required to add grade.", "danger")
        return redirect(url_for('view_student', id=id))

    pct = (marks_obtained / max_marks * 100) if max_marks > 0 else 0
    if pct >= 90: grade_letter = 'A+'
    elif pct >= 80: grade_letter = 'A'
    elif pct >= 70: grade_letter = 'B'
    elif pct >= 60: grade_letter = 'C'
    elif pct >= 50: grade_letter = 'D'
    else: grade_letter = 'F'

    grade = Grade(
        student_id=id,
        subject_name=subject_name,
        semester=semester,
        marks_obtained=marks_obtained,
        max_marks=max_marks,
        grade_letter=grade_letter
    )
    db.session.add(grade)
    db.session.commit()

    flash(f"Grade added for {subject_name} ({grade_letter})!", "success")
    return redirect(url_for('view_student', id=id))

# --- Attendance Marker Route ---
@app.route('/students/<int:id>/attendance/add', methods=['POST'])
def mark_attendance(id):
    student = db.get_or_404(Student, id)
    att_date_str = request.form.get('attendance_date', str(date.today()))
    status = request.form.get('status', 'Present')
    remarks = request.form.get('remarks', '').strip()

    try:
        att_date = datetime.strptime(att_date_str, "%Y-%m-%d").date()
    except ValueError:
        att_date = date.today()

    att = Attendance(
        student_id=id,
        attendance_date=att_date,
        status=status,
        remarks=remarks
    )
    db.session.add(att)
    db.session.commit()

    flash(f"Attendance recorded as '{status}' for {att_date}!", "success")
    return redirect(url_for('view_student', id=id))

# --- Bulk Attendance Marker Route ---
@app.route('/attendance/bulk', methods=['GET', 'POST'])
def bulk_attendance():
    if request.method == 'POST':
        att_date_str = request.form.get('attendance_date', str(date.today()))
        try:
            att_date = datetime.strptime(att_date_str, "%Y-%m-%d").date()
        except ValueError:
            att_date = date.today()

        students = Student.query.filter_by(status='Active').all()
        count = 0
        for s in students:
            status_val = request.form.get(f'status_{s.id}', 'Present')
            att = Attendance(student_id=s.id, attendance_date=att_date, status=status_val)
            db.session.add(att)
            count += 1

        db.session.commit()
        flash(f"Bulk attendance recorded for {count} active students on {att_date}!", "success")
        return redirect(url_for('dashboard'))

    students = Student.query.filter_by(status='Active').order_by(Student.student_id.asc()).all()
    return render_template('bulk_attendance.html', students=students, today_date=date.today().strftime('%Y-%m-%d'))

# --- CSV Bulk Import Route ---
@app.route('/students/import/csv', methods=['POST'])
def import_csv():
    if 'csv_file' not in request.files:
        flash("No file selected for CSV import.", "danger")
        return redirect(url_for('list_students'))

    file = request.files['csv_file']
    if not file or file.filename == '':
        flash("No file selected.", "danger")
        return redirect(url_for('list_students'))

    try:
        stream = TextIOWrapper(file.stream, encoding='utf-8')
        csv_reader = csv.DictReader(stream)
        
        imported_count = 0
        skipped_count = 0

        for row in csv_reader:
            student_id = row.get('Student ID', '').strip() or row.get('student_id', '').strip()
            full_name = row.get('Full Name', '').strip() or row.get('full_name', '').strip()
            email = row.get('Email', '').strip() or row.get('email', '').strip()
            phone = row.get('Phone', '').strip() or row.get('phone', '').strip()
            course = row.get('Course', '').strip() or row.get('course', '').strip()
            gender = row.get('Gender', 'Male').strip() or row.get('gender', 'Male').strip()
            dob_str = row.get('DOB', '2003-01-01').strip() or row.get('dob', '2003-01-01').strip()
            status = row.get('Status', 'Active').strip() or row.get('status', 'Active').strip()
            address = row.get('Address', '').strip() or row.get('address', '').strip()

            if not student_id or not full_name or not email:
                skipped_count += 1
                continue

            # Check if student ID or email exists
            if Student.query.filter(or_(Student.student_id == student_id, Student.email == email)).first():
                skipped_count += 1
                continue

            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                dob = date(2003, 1, 1)

            st = Student(
                student_id=student_id,
                full_name=full_name,
                email=email,
                phone=phone or '+91 99999 00000',
                course=course or 'Computer Science',
                gender=gender,
                dob=dob,
                address=address,
                status=status
            )
            db.session.add(st)
            imported_count += 1

        db.session.commit()
        flash(f"CSV Import Complete: {imported_count} students registered, {skipped_count} duplicates/skipped.", "success")
    except Exception as e:
        flash(f"Error reading CSV file: {str(e)}", "danger")

    return redirect(url_for('list_students'))

# --- Print Transcript / Student Card Route ---
@app.route('/students/<int:id>/print')
def print_transcript(id):
    student = db.get_or_404(Student, id)
    grades = Grade.query.filter_by(student_id=id).all()
    attendance_list = Attendance.query.filter_by(student_id=id).all()
    return render_template('student_print.html', student=student, grades=grades, attendance_list=attendance_list)

@app.route('/students/export/csv')
def export_csv():
    students = Student.query.order_by(Student.student_id.asc()).all()
    si = StringIO()
    cw = csv.writer(si)
    
    cw.writerow(['ID', 'Student ID', 'Full Name', 'Email', 'Phone', 'Course', 'Gender', 'DOB', 'Status', 'GPA', 'Fee Paid', 'Fee Pending', 'Address', 'Registered Date'])
    for s in students:
        cw.writerow([
            s.id,
            s.student_id,
            s.full_name,
            s.email,
            s.phone,
            s.course,
            s.gender,
            s.dob.strftime('%Y-%m-%d') if s.dob else '',
            s.status,
            s.gpa,
            s.paid_fee,
            s.pending_fee,
            s.address or '',
            s.created_at.strftime('%Y-%m-%d %H:%M') if s.created_at else ''
        ])

    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=student_records.csv"}
    )

# API Endpoint
@app.route('/api/students')
def api_students():
    query = request.args.get('q', '').strip()
    if query:
        students = Student.query.filter(
            or_(
                Student.full_name.ilike(f'%{query}%'),
                Student.student_id.ilike(f'%{query}%'),
                Student.email.ilike(f'%{query}%'),
                Student.course.ilike(f'%{query}%')
            )
        ).all()
    else:
        students = Student.query.all()

    return jsonify([s.to_dict() for s in students])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_sample_data()
    app.run(debug=True, port=5000)
