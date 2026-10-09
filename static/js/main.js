/* -------------------------------------------------------------
   Student Registration Management System - Main JavaScript Logic
   ------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initFlashAlerts();
    initDeleteModal();
    initFormValidation();
    initLiveSearch();
});

/* --- 1. Theme Switcher (Dark/Light Mode) --- */
function initTheme() {
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');

    // Retrieve stored theme preference or use system preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    let currentTheme = savedTheme || (prefersDark ? 'dark' : 'light');
    applyTheme(currentTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            currentTheme = (currentTheme === 'light') ? 'dark' : 'light';
            applyTheme(currentTheme);
            localStorage.setItem('theme', currentTheme);
        });
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        if (themeIcon) {
            if (theme === 'dark') {
                themeIcon.className = 'bi bi-sun-fill';
            } else {
                themeIcon.className = 'bi bi-moon-stars-fill';
            }
        }
    }
}

/* --- 2. Auto Dismiss Flash Alerts --- */
function initFlashAlerts() {
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 6000);
    });
}

/* --- 3. Modal Confirmation for Deletion --- */
function initDeleteModal() {
    const deleteButtons = document.querySelectorAll('.btn-delete-trigger');
    const deleteForm = document.getElementById('deleteStudentForm');
    const deleteStudentName = document.getElementById('deleteStudentName');

    deleteButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const studentId = btn.getAttribute('data-id');
            const studentName = btn.getAttribute('data-name');
            const deleteUrl = btn.getAttribute('data-url');

            if (deleteForm) {
                deleteForm.action = deleteUrl;
            }
            if (deleteStudentName) {
                deleteStudentName.textContent = studentName;
            }
        });
    });
}

/* --- 4. Form Validation for Registration & Edit --- */
function initFormValidation() {
    const form = document.getElementById('studentForm');
    if (!form) return;

    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');
    const idInput = document.getElementById('student_id');

    form.addEventListener('submit', (event) => {
        let isValid = true;
        
        // Remove previous invalid classes
        form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));

        // Validate Full Name
        const nameInput = document.getElementById('full_name');
        if (nameInput && nameInput.value.trim().length < 2) {
            markInvalid(nameInput, 'Full name must be at least 2 characters.');
            isValid = false;
        }

        // Validate Student ID
        if (idInput && idInput.value.trim().length < 3) {
            markInvalid(idInput, 'Student ID must be valid (e.g. STU2026001).');
            isValid = false;
        }

        // Validate Email
        if (emailInput) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(emailInput.value.trim())) {
                markInvalid(emailInput, 'Please enter a valid email address.');
                isValid = false;
            }
        }

        // Validate Phone
        if (phoneInput) {
            const phoneRegex = /^[\d\+\-\s\(\)]{8,20}$/;
            if (!phoneRegex.test(phoneInput.value.trim())) {
                markInvalid(phoneInput, 'Please enter a valid phone number (at least 8 digits).');
                isValid = false;
            }
        }

        if (!isValid) {
            event.preventDefault();
            event.stopPropagation();
        }
    });

    function markInvalid(element, message) {
        element.classList.add('is-invalid');
        const feedback = element.nextElementSibling;
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.textContent = message;
        }
    }
}

/* --- 5. Quick Client-Side Table Filter --- */
function initLiveSearch() {
    const searchInput = document.getElementById('clientTableSearch');
    const tableBody = document.getElementById('studentsTableBody');

    if (!searchInput || !tableBody) return;

    searchInput.addEventListener('input', () => {
        const filter = searchInput.value.toLowerCase();
        const rows = tableBody.getElementsByTagName('tr');

        Array.from(rows).forEach(row => {
            const text = row.innerText.toLowerCase();
            if (text.includes(filter)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
}
