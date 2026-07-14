# 🏥 Hospital Management System

A web-based Hospital Management System developed using **Python, Flask, Firebase, HTML, and CSS**. The application provides a digital platform for managing hospital operations, healthcare records, and related services.

## 🌐 Live Demo

🔗 https://hospital-management-izbu.onrender.com/

> **Note:** The application is hosted on Render's free instance. The first request may take a few seconds while the server starts.

## ✨ Features

- 🏥 Hospital management dashboard
- 👨‍⚕️ Doctor management
- 🧑‍🤝‍🧑 Patient management
- 📋 Healthcare record management
- 🔥 Firebase integration
- ☁️ Cloud-based data storage
- 📱 Responsive web interface
- 🔐 Secure Firebase Admin SDK integration

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- Gunicorn

### Database & Cloud
- Firebase
- Cloud Firestore
- Firebase Storage

### Frontend
- HTML
- CSS
- Jinja2

### Deployment
- Render

## 📂 Project Structure

```text
hospital-management/
├── static/
│   └── css/
├── templates/
├── app.py
├── firebase_config.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Run Locally

1. Clone the repository:

```bash
git clone https://github.com/aleesha6127/hospital-management.git
```

2. Open the project directory:

```bash
cd hospital-management
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add your Firebase service account key as:

```text
firebase_key.json
```

5. Run the application:

```bash
python app.py
```

6. Open the application in your browser:

```text
http://127.0.0.1:5000
```

## 🔐 Security

Firebase service account credentials are not stored in the repository. During production deployment, the Firebase private key is securely configured using Render Secret Files.

## 👩‍💻 Developer

**Aleesha Anas**

- Portfolio: https://aleesha6127.github.io/portfolio/
- GitHub: https://github.com/aleesha6127
- LinkedIn: https://www.linkedin.com/in/aleesha-anas-a7553533b/

## 📄 License

This project is developed for educational and portfolio purposes.
