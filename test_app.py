import unittest
import os
from io import BytesIO
from datetime import datetime, date
from app import app, db, Student, Grade, Attendance

class StudentManagementSystemTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
            # Seed 2 initial test records
            s1 = Student(
                student_id="TEST001",
                full_name="Alice Smith",
                email="alice@example.com",
                phone="1234567890",
                course="Computer Science",
                gender="Female",
                dob=datetime.strptime("2002-01-01", "%Y-%m-%d").date(),
                address="123 Test St",
                status="Active",
                total_fee=50000.0,
                paid_fee=30000.0
            )
            s2 = Student(
                student_id="TEST002",
                full_name="Bob Jones",
                email="bob@example.com",
                phone="9876543210",
                course="Data Science",
                gender="Male",
                dob=datetime.strptime("2001-05-15", "%Y-%m-%d").date(),
                address="456 Sample Rd",
                status="On Leave",
                total_fee=60000.0,
                paid_fee=60000.0
            )
            db.session.add_all([s1, s2])
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_dashboard_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student Management Dashboard', response.data)
        self.assertIn(b'Alice Smith', response.data)

    def test_list_students_route(self):
        response = self.app.get('/students')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Alice Smith', response.data)
        self.assertIn(b'Bob Jones', response.data)

    def test_search_student(self):
        response = self.app.get('/students?search=Alice')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TEST001', response.data)
        self.assertNotIn(b'TEST002', response.data)

    def test_register_student_success(self):
        data = {
            'student_id': 'TEST003',
            'full_name': 'Charlie Brown',
            'email': 'charlie@example.com',
            'phone': '5551234567',
            'course': 'Information Technology',
            'gender': 'Male',
            'dob': '2003-03-30',
            'address': '789 Park Ave',
            'status': 'Active',
            'total_fee': 50000.0,
            'paid_fee': 10000.0
        }
        response = self.app.post('/students/register', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Charlie Brown', response.data)

    def test_add_grade(self):
        data = {
            'subject_name': 'Software Engineering',
            'semester': 'Sem 1',
            'marks_obtained': 92,
            'max_marks': 100
        }
        response = self.app.post('/students/1/grades/add', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Software Engineering', response.data)

        with app.app_context():
            g = Grade.query.filter_by(student_id=1).first()
            self.assertIsNotNone(g)
            self.assertEqual(g.grade_letter, 'A+')

    def test_mark_attendance(self):
        data = {
            'attendance_date': '2026-10-09',
            'status': 'Present',
            'remarks': 'On time'
        }
        response = self.app.post('/students/1/attendance/add', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with app.app_context():
            att = Attendance.query.filter_by(student_id=1).first()
            self.assertIsNotNone(att)
            self.assertEqual(att.status, 'Present')

    def test_bulk_attendance(self):
        data = {
            'attendance_date': '2026-10-09',
            'status_1': 'Present'
        }
        response = self.app.post('/attendance/bulk', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_print_transcript(self):
        response = self.app.get('/students/1/print')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Official Student Transcript', response.data)

    def test_csv_import(self):
        csv_content = b"student_id,full_name,email,phone,course,gender,dob,status\nTEST999,Imported Student,imported@example.com,+91 99999 88888,Data Science,Male,2003-01-01,Active\n"
        data = {
            'csv_file': (BytesIO(csv_content), 'import.csv')
        }
        response = self.app.post('/students/import/csv', data=data, content_type='multipart/form-data', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Import Complete', response.data)

        with app.app_context():
            st = Student.query.filter_by(student_id='TEST999').first()
            self.assertIsNotNone(st)
            self.assertEqual(st.full_name, 'Imported Student')

if __name__ == '__main__':
    unittest.main()
