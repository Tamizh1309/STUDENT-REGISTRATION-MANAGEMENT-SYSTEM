-- -------------------------------------------------------------
-- Student Registration Management System
-- Seed Data for MySQL
-- -------------------------------------------------------------

USE `student_db`;

INSERT INTO `students` (`id`, `student_id`, `full_name`, `email`, `phone`, `course`, `gender`, `dob`, `address`, `status`, `total_fee`, `paid_fee`) VALUES
(1, 'STU2026001', 'Aarav Sharma', 'aarav.sharma@example.com', '+91 98765 43210', 'Computer Science', 'Male', '2003-05-15', '12 MG Road, Bengaluru, Karnataka', 'Active', 60000.0, 60000.0),
(2, 'STU2026002', 'Priya Ananth', 'priya.a@example.com', '+91 98123 45678', 'Information Technology', 'Female', '2002-11-20', '45 Anna Salai, Chennai, Tamil Nadu', 'Active', 55000.0, 40000.0),
(3, 'STU2026003', 'Rohan Verma', 'rohan.verma@example.com', '+91 97654 32109', 'Data Science', 'Male', '2004-01-10', '88 Park Street, Kolkata, West Bengal', 'Active', 65000.0, 30000.0),
(4, 'STU2026004', 'Ananya Iyer', 'ananya.iyer@example.com', '+91 99887 76655', 'Electronics & Communication', 'Female', '2003-08-04', '22 FC Road, Pune, Maharashtra', 'Active', 50000.0, 50000.0),
(5, 'STU2026005', 'Vikramaditya Das', 'vikram.das@example.com', '+91 91234 56789', 'Business Analytics', 'Male', '2002-03-29', '79 Civil Lines, Jaipur, Rajasthan', 'On Leave', 52000.0, 25000.0),
(6, 'STU2026006', 'Meera Pillai', 'meera.pillai@example.com', '+91 94455 66778', 'Computer Science', 'Female', '2003-12-14', '34 Kowdiar, Thiruvananthapuram, Kerala', 'Active', 60000.0, 60000.0),
(7, 'STU2026007', 'Karthik Raju', 'karthik.raju@example.com', '+91 93344 55667', 'Mechanical Engineering', 'Male', '2002-07-19', '102 Banjara Hills, Hyderabad, Telangana', 'Graduated', 58000.0, 58000.0);

INSERT INTO `grades` (`student_id`, `subject_name`, `semester`, `marks_obtained`, `max_marks`, `grade_letter`) VALUES
(1, 'Data Structures & Algorithms', 'Sem 1', 92.0, 100.0, 'A+'),
(1, 'Database Management Systems', 'Sem 1', 88.0, 100.0, 'A'),
(2, 'Web Architecture', 'Sem 1', 95.0, 100.0, 'A+'),
(3, 'Applied Statistics', 'Sem 1', 85.0, 100.0, 'A');

INSERT INTO `attendance` (`student_id`, `attendance_date`, `status`, `remarks`) VALUES
(1, '2026-10-09', 'Present', 'On time'),
(2, '2026-10-09', 'Present', 'On time'),
(3, '2026-10-09', 'Absent', 'Medical leave');
