from flask import Flask, render_template, request, redirect, session, jsonify
from firebase_config import db
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "secret-key"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================================================
# LOGIN (ADMIN / HOSPITAL)
# =========================================================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        username = request.form.get("username")
        password = request.form.get("password")

        # ADMIN
        if role == "admin":
            admins = db.collection("admins").where("username", "==", username).stream()
            for a in admins:
                if a.to_dict().get("password") == password:
                    session.clear()
                    session["admin"] = True
                    return redirect("/admin/dashboard")
            return render_template("login.html", error="Invalid admin login")

        # HOSPITAL
        if role == "hospital":
            hospitals = db.collection("hospitals").where("username", "==", username).stream()
            for h in hospitals:
                data = h.to_dict()
                if data.get("password") == password and data.get("active"):
                    session.clear()
                    session["hospital_id"] = h.id
                    return redirect("/hospital/dashboard")
            return render_template("login.html", error="Invalid hospital login")

    return render_template("login.html")

# =========================================================
# ADMIN
# =========================================================
@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect("/")
    hospitals = list(db.collection("hospitals").stream())
    return render_template("admin_dashboard.html", hospitals=hospitals)


@app.route("/admin/add-hospital", methods=["GET", "POST"])
def add_hospital():
    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":
        image_path = ""
        image = request.files.get("image")

        if image and image.filename:
            filename = secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)

        db.collection("hospitals").add({
            "name": request.form["name"],
            "username": request.form["username"],
            "password": request.form["password"],
            "contact": request.form["contact"],
            "latitude": request.form["latitude"],
            "longitude": request.form["longitude"],
            "image": image_path,
            "active": True
        })
        return redirect("/admin/dashboard")

    return render_template("add_hospital.html")

# =========================================================
# HOSPITAL
# =========================================================
@app.route("/hospital/dashboard")
def hospital_dashboard():
    if "hospital_id" not in session:
        return redirect("/")

    hospital_ref = db.collection("hospitals").document(session["hospital_id"])
    hospital = hospital_ref.get().to_dict()

    departments = list(hospital_ref.collection("departments").stream())
    doctors = list(hospital_ref.collection("doctors").stream())

    return render_template(
        "hospital_dashboard.html",
        hospital=hospital,
        departments=departments,
        doctors=doctors,
        profile_percent=100
    )


@app.route("/hospital/add-department", methods=["GET", "POST"])
def add_department():
    if "hospital_id" not in session:
        return redirect("/")

    if request.method == "POST":
        db.collection("hospitals") \
            .document(session["hospital_id"]) \
            .collection("departments") \
            .add({"name": request.form["name"]})
        return redirect("/hospital/dashboard")

    return render_template("add_department.html")


@app.route("/hospital/add-doctor", methods=["GET", "POST"])
def add_doctor():
    if "hospital_id" not in session:
        return redirect("/")

    hospital_ref = db.collection("hospitals").document(session["hospital_id"])

    if request.method == "POST":
        hospital_ref.collection("doctors").add({
            "name": request.form["name"],
            "specialization": request.form["specialization"],
            "department": request.form["department"],
            "timing": request.form["timing"],
            "password": request.form["password"]
        })
        return redirect("/hospital/dashboard")

    departments = list(hospital_ref.collection("departments").stream())
    return render_template("add_doctor.html", departments=departments)

# =========================================================
# DOCTOR LOGIN
# =========================================================
@app.route("/doctor/login/<doctor_id>", methods=["GET", "POST"])
def doctor_login(doctor_id):
    if "hospital_id" not in session:
        return redirect("/")

    hospital_ref = db.collection("hospitals").document(session["hospital_id"])
    doctor_ref = hospital_ref.collection("doctors").document(doctor_id)
    doctor = doctor_ref.get().to_dict()

    if request.method == "POST":
        if request.form["password"] == doctor["password"]:
            session.clear()
            session["doctor_id"] = doctor_id
            session["hospital_id"] = hospital_ref.id
            return redirect("/doctor/dashboard")

        return render_template("doctor_login.html", doctor=doctor, error="Invalid password")

    return render_template("doctor_login.html", doctor=doctor)

# =========================================================
# DOCTOR DASHBOARD (AUTO DUMMY PATIENT)
# =========================================================
@app.route("/doctor/dashboard")
def doctor_dashboard():
    if "doctor_id" not in session or "hospital_id" not in session:
        return redirect("/")

    hospital_ref = db.collection("hospitals").document(session["hospital_id"])
    doctor = hospital_ref.collection("doctors").document(session["doctor_id"]).get().to_dict()
    appointments_ref = hospital_ref.collection("appointments")

    appointments = list(
        appointments_ref.where("doctor_id", "==", session["doctor_id"]).stream()
    )

    # AUTO DUMMY PATIENT (ONLY ONCE)
    if len(appointments) == 0:
        appointments_ref.add({
            "patient_name": "Demo Patient",
            "patient_age": 30,
            "patient_gender": "Male",
            "doctor_id": session["doctor_id"],
            "date": "2026-01-25",
            "time": "10:30 AM",
            "status": "Accepted",
            "is_dummy": True
        })

        appointments = list(
            appointments_ref.where("doctor_id", "==", session["doctor_id"]).stream()
        )

    return render_template(
        "doctor_dashboard.html",
        doctor=doctor,
        appointments=appointments
    )

# =========================================================
# UPDATE APPOINTMENT STATUS
# =========================================================
@app.route("/doctor/update-status/<appointment_id>", methods=["POST"])
def update_appointment_status(appointment_id):
    if "doctor_id" not in session or "hospital_id" not in session:
        return redirect("/")

    new_status = request.form.get("status")

    hospital_ref = db.collection("hospitals").document(session["hospital_id"])
    appointment_ref = hospital_ref.collection("appointments").document(appointment_id)

    appointment_ref.update({
        "status": new_status
    })

    return redirect("/doctor/dashboard")

# =========================================================
# APPOINTMENT ACTIONS
# =========================================================
@app.route("/doctor/appointment/<appointment_id>/accept", methods=["POST"])
def accept_appointment(appointment_id):
    db.collection("hospitals") \
        .document(session["hospital_id"]) \
        .collection("appointments") \
        .document(appointment_id) \
        .update({"status": "Accepted"})
    return redirect("/doctor/dashboard")


@app.route("/doctor/appointment/<appointment_id>/reject", methods=["POST"])
def reject_appointment(appointment_id):
    db.collection("hospitals") \
        .document(session["hospital_id"]) \
        .collection("appointments") \
        .document(appointment_id) \
        .update({"status": "Rejected"})
    return redirect("/doctor/dashboard")


@app.route("/doctor/prescribe/<appointment_id>", methods=["POST", "GET"])
def prescribe(appointment_id):
    hospital_ref = db.collection("hospitals").document(session["hospital_id"])
    appointment_ref = hospital_ref.collection("appointments").document(appointment_id)

    if request.method == "POST":
        appointment_ref.update({
            "prescription": request.form["prescription"],
            "status": "Prescribed"
        })
        return redirect("/doctor/dashboard")

    appointment = appointment_ref.get().to_dict()
    return render_template("prescribe.html", appointment=appointment)

# =========================================================
# MOBILE APP → BOOK APPOINTMENT API
# =========================================================
@app.route("/api/book-appointment", methods=["POST"])
def book_appointment():
    data = request.json

    db.collection("hospitals") \
        .document(data["hospital_id"]) \
        .collection("appointments") \
        .add({
            "patient_name": data["patient_name"],
            "patient_age": data["patient_age"],
            "patient_gender": data["patient_gender"],
            "doctor_id": data["doctor_id"],
            "date": data["date"],
            "time": data["time"],
            "status": "Pending"
        })

    return jsonify({"status": "success"}), 201

# =========================================================
# EDIT DOCTOR
# =========================================================
@app.route("/hospital/edit-doctor/<doctor_id>", methods=["GET", "POST"])
def edit_doctor(doctor_id):
    if "hospital_id" not in session:
        return redirect("/")

    hospital_ref = db.collection("hospitals").document(session["hospital_id"])
    doctor_ref = hospital_ref.collection("doctors").document(doctor_id)

    if request.method == "POST":
        doctor_ref.update({
            "name": request.form["name"],
            "specialization": request.form["specialization"],
            "department": request.form["department"],
            "timing": request.form["timing"],
            "password": request.form["password"]
        })
        return redirect("/hospital/dashboard")

    doctor = doctor_ref.get().to_dict()
    departments = list(hospital_ref.collection("departments").stream())

    return render_template(
        "edit_doctor.html",
        doctor=doctor,
        doctor_id=doctor_id,
        departments=departments
    )


# =========================================================
# DELETE DOCTOR
# =========================================================
@app.route("/hospital/delete-doctor/<doctor_id>")
def delete_doctor(doctor_id):
    if "hospital_id" not in session:
        return redirect("/")

    db.collection("hospitals") \
        .document(session["hospital_id"]) \
        .collection("doctors") \
        .document(doctor_id) \
        .delete()

    return redirect("/hospital/dashboard")

# =========================================================
# LOGOUT
# =========================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
