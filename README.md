# 🎓 Student Registration & Academic Management System

![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=for-the-badge&logo=flask&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Supported-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Default-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.style=for-the-badge)

A full-stack web application designed for educational institutions to streamline **Student Registration**, **Academic Grade Tracking (GPA)**, **Daily Attendance Management**, **Financial Fee Tracking**, **Profile Photo Uploads**, **Bulk CSV Imports/Exports**, and **Printable Academic Transcripts**.

---

## 🚀 Live Demo & Repository

- **GitHub Repository**: [https://github.com/Tamizh1309/STUDENT-REGISTRATION-MANAGEMENT-SYSTEM](https://github.com/Tamizh1309/STUDENT-REGISTRATION-MANAGEMENT-SYSTEM)

---

## ✨ Key Features

### 📊 1. Interactive Analytics Dashboard
- **Key Metrics**: Real-time statistics for Total Students, Active Enrollments, Students on Leave, Alumni Graduated, Total Fees Collected, and Outstanding Dues.
- **Chart.js Visualizations**:
  - Course Distribution Bar Chart.
  - Fee Collection vs Pending Dues Doughnut Chart.
- **Recent Registrations**: Quick access to newly enrolled students.

### 📝 2. Student Registration & Full CRUD
- **Registration Form**: Client-side & server-side validation with auto-generated unique Student Roll IDs (e.g. `STU2026001`).
- **Profile Image Upload**: Upload and store student profile avatars (`JPG`, `PNG`, `WEBP`).
- **Record Listing & Filters**: Multi-parameter search (Name, Student ID, Email, Phone), Course Filter, and Status Filter.
- **Detailed Student Profiles**: Individual card layout detailing personal info, academic grades, attendance logs, and fee status.
- **Record Editing & Safe Deletion**: Pre-filled update forms and modal popups for record deletion.

### 🎓 3. Academic Grade Management & GPA Calculator
- Add subject marks per semester with automated letter grade assignment ($A+$, $A$, $B$, $C$, $F$).
- Dynamic Cumulative GPA calculation on a $4.0$ scale.

### 📅 4. Attendance System
- **Bulk Daily Attendance Marker** (`/attendance/bulk`): Record daily attendance (*Present*, *Absent*, *Late*, *Excused*) for all active students simultaneously.
- **Attendance Percentage**: Visual attendance progress tracking for every student.

### 💳 5. Financial Fee Management
- Track Total Course Fees, Amount Paid, and Pending Dues.
- Visual payment progress bars on student profiles and status badges on the records table.

### 📤 6. Import / Export Capabilities
- **One-Click CSV Export**: Download all student records in CSV format.
- **Bulk CSV Import**: Upload a `.csv` file to auto-register multiple students with duplicate validation.

### 🖨️ 7. Printable Academic Transcript & ID Card
- Dedicated print layout (`/students/<id>/print`) formatted with `@media print` CSS for PDF downloads and hard copy printing.

### 🌓 8. Modern UI & Dark Mode
- Styled with custom CSS variables, Google Fonts (*Plus Jakarta Sans* & *Outfit*), Bootstrap 5, and Bootstrap Icons.
- Built-in **Dark / Light Mode** theme toggle with preference saved in `localStorage`.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.14, Flask, Flask-SQLAlchemy, SQLAlchemy ORM, Gunicorn
- **Frontend**: HTML5, Vanilla CSS3 (Custom Variables & Dark Mode), JavaScript (ES6+), Bootstrap 5.3, Chart.js
- **Databases**: SQLite (Default out-of-the-box local database), MySQL (Production ready via `PyMySQL`)
- **Testing**: Python `unittest` framework

---

## 📁 Repository Structure

```text
STUDENT REGISTRATION MANAGEMENT SYSTEM/
├── app.py                  # Flask application, SQLAlchemy models, and route logic
├── schema.sql              # MySQL DDL schema definition
├── seed_data.sql           # MySQL sample seed data SQL script
├── test_app.py             # Automated unit and integration test suite
├── requirements.txt        # Production Python dependencies
├── Procfile                # Gunicorn deployment process file
├── render.yaml             # Render cloud deployment blueprint
├── static/
│   ├── css/
│   │   └── style.css       # Custom design system & dark mode CSS
│   ├── js/
│   │   └── main.js         # Client-side validation, theme toggle & search logic
│   └── uploads/            # Uploaded student profile photos
└── templates/
    ├── base.html           # Master layout template (navbar, alerts, modals)
    ├── dashboard.html      # Interactive analytics dashboard with Chart.js
    ├── students.html       # Student records table, search, filter & CSV import
    ├── student_form.html   # Registration and edit student form
    ├── student_detail.html # Comprehensive student profile card view
    ├── bulk_attendance.html# Bulk daily attendance marker page
    └── student_print.html  # Printable official transcript layout
```

---

## 💻 Quick Start Guide

### 1. Clone the Repository

```bash
git clone https://github.com/Tamizh1309/STUDENT-REGISTRATION-MANAGEMENT-SYSTEM.git
cd STUDENT-REGISTRATION-MANAGEMENT-SYSTEM
```

### 2. Set Up Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

Open your browser and visit: **`http://127.0.0.1:5000/`**

*Note: The app will automatically initialize `students.db` and seed initial sample data on first run.*

---

## 🗄️ MySQL Database Setup (Optional)

To connect the application to a live MySQL database server:

1. Import `schema.sql` and `seed_data.sql` into MySQL:
   ```bash
   mysql -u root -p < schema.sql
   mysql -u root -p student_db < seed_data.sql
   ```

2. Export environment variables prior to running `app.py`:
   ```bash
   set MYSQL_USER=root
   set MYSQL_PASSWORD=your_password
   set MYSQL_HOST=localhost
   set MYSQL_DB=student_db
   python app.py
   ```

---

## 🧪 Running Automated Tests

Run the backend test suite covering CRUD operations, GPA calculations, attendance, CSV import, and routes:

```bash
python test_app.py
```

Expected Output: `Ran 9 tests in ... OK`

---

## 🌐 Deploying to Production (Render / Heroku / Railway)

This repository includes pre-configured deployment files (`requirements.txt`, `Procfile`, `render.yaml`):

### 1-Click Deployment on Render:
1. Sign in to **[Render Dashboard](https://dashboard.render.com/)** with your GitHub account.
2. Click **New +** $\rightarrow$ **Web Service**.
3. Select **`Tamizh1309/STUDENT-REGISTRATION-MANAGEMENT-SYSTEM`**.
4. Click **Deploy Web Service**!

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).