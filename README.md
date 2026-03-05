# 🏥 Hospital Management System

A web-based Hospital Management System built with **Flask** and **Firebase Firestore**. It supports three user roles — **Admin**, **Hospital**, and **Doctor** — and exposes a REST API for mobile app integration (appointment booking).

---

## ✨ Features

### 👨‍💼 Admin
- Login with admin credentials
- View all registered hospitals
- Add new hospitals (with image upload, location coordinates, and login credentials)

### 🏨 Hospital
- Login with hospital credentials
- View hospital dashboard (departments & doctors overview)
- Add / Edit / Delete departments
- Add / Edit / Delete doctors (with specialization, timing, and password)

### 👨‍⚕️ Doctor
- Login via hospital dashboard (password-protected)
- View assigned appointments
- Accept / Reject appointments
- Write prescriptions for patients

### 📱 Mobile API
- `POST /api/book-appointment` — Book an appointment from a mobile app (JSON payload)

---

## 🗂️ Project Structure

```
hospital_management/
│
├── app.py                  # Main Flask application & all routes
├── firebase_config.py      # Firebase Admin SDK initialization
├── firebase_key.json       # Firebase service account key (keep private!)
├── requirements.txt        # Python dependencies
│
├── static/
│   └── uploads/            # Uploaded hospital images
│
└── templates/
    ├── login.html
    ├── admin_dashboard.html
    ├── add_hospital.html
    ├── hospital_dashboard.html
    ├── add_department.html
    ├── add_doctor.html
    ├── edit_doctor.html
    ├── doctor_login.html
    ├── doctor_dashboard.html
    ├── prescribe.html
    └── ...
```

---

## 🛠️ Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Backend     | Python, Flask                     |
| Database    | Firebase Firestore                |
| Auth/Storage| Firebase Admin SDK                |
| Frontend    | HTML, Jinja2 Templates            |
| File Upload | Werkzeug                          |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8+
- A Firebase project with Firestore enabled
- Firebase service account key (`firebase_key.json`)

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd hospital_management
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Firebase
Place your Firebase service account key file as `firebase_key.json` in the project root.

> ⚠️ **Never commit `firebase_key.json` to version control.** Add it to `.gitignore`.

### 5. Run the application
```bash
python app.py
```

The app will be available at **http://127.0.0.1:5000/**

---

## 🔌 API Endpoint

### Book Appointment (Mobile App)

**`POST /api/book-appointment`**

**Request Body (JSON):**
```json
{
  "hospital_id": "HOSPITAL_FIRESTORE_DOC_ID",
  "patient_name": "John Doe",
  "patient_age": 28,
  "patient_gender": "Male",
  "doctor_id": "DOCTOR_FIRESTORE_DOC_ID",
  "date": "2026-03-10",
  "time": "11:00 AM"
}
```

**Response:**
```json
{ "status": "success" }
```

---

## 🔐 User Roles & Login

| Role     | Login URL          | Credentials stored in        |
|----------|--------------------|------------------------------|
| Admin    | `/` (select Admin) | `admins` Firestore collection |
| Hospital | `/` (select Hospital) | `hospitals` Firestore collection |
| Doctor   | `/doctor/login/<doctor_id>` | `doctors` sub-collection under hospital |

---

## 🗃️ Firestore Data Structure

```
admins/
  └── {adminId}: { username, password }

hospitals/
  └── {hospitalId}: { name, username, password, contact, latitude, longitude, image, active }
        ├── departments/
        │     └── {deptId}: { name }
        ├── doctors/
        │     └── {doctorId}: { name, specialization, department, timing, password }
        └── appointments/
              └── {appointmentId}: { patient_name, patient_age, patient_gender, doctor_id, date, time, status, prescription? }
```

---

## 📝 .gitignore Recommendations

```
venv/
__pycache__/
firebase_key.json
static/uploads/
*.pyc
```

---

## 📄 License

This project was developed as part of an internship. All rights reserved.
