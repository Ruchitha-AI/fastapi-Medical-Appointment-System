
Got it 👍 — you want **same type README but for YOUR project (Doctor + Appointment system)**.

Here is your **perfect README (ready to copy & submit) ✅**

---

# 📚 FastAPI MediCare Clinic Management System

## 🚀 Project Overview

The **MediCare Clinic Management System** is a backend application built using FastAPI that allows managing doctors and appointment workflows efficiently.

This project was developed as part of the FastAPI Internship Program where key backend concepts such as API design, data validation, CRUD operations, workflows, search, sorting, and pagination were implemented.

The system simulates a real-world clinic backend by allowing users to:

* View doctors
* Add, update, and delete doctors
* Book appointments
* Manage appointment status (confirm, cancel, complete)
* Search and filter doctors
* Browse data using sorting and pagination

All APIs are tested using Swagger UI.

---

## 🛠 Technologies Used

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Core programming language |
| FastAPI    | Backend API framework     |
| Pydantic   | Data validation           |
| Uvicorn    | ASGI server               |
| Swagger UI | API testing               |

---

## 📂 Project Structure

```
fastapi-medicare-system
│
├── main.py
├── requirements.txt
├── README.md
└── screenshots
      ├── Q1_home.png
      ├── Q2_get_doctors.png
      ├── Q3_get_doctor_by_id.png
      ├── ...
      └── Q20_browse.png
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```
git clone <https://github.com/Ruchitha-AI/fastapi-Medical-Appointment-System/tree/main>
```

### 2️⃣ Navigate to Folder

```
cd fastapi-medicare-system
```

### 3️⃣ Create Virtual Environment

```
python -m venv venv
```

### 4️⃣ Activate Environment

**Windows:**

```
venv\Scripts\activate
```

**Mac/Linux:**

```
source venv/bin/activate
```

### 5️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 6️⃣ Run Server

```
uvicorn main:app --reload
```

### 7️⃣ Open Swagger Docs

```
http://127.0.0.1:8000/docs
```

---

## 📌 API Features Implemented

### 🔹 Doctor Management

* Get all doctors
* Get doctor by ID
* Add new doctor
* Update doctor details
* Delete doctor
* Duplicate name validation

---

### 🔹 Appointment Management

* Create appointment
* View appointments
* Confirm appointment
* Cancel appointment
* Complete appointment

---

### 🔹 Helper Functions

* `find_doctor()`
* `calculate_fee()`
* `filter_doctors_logic()`

---

## 🔍 Advanced API Features

### 🔎 Search

Search doctors by:

* Name
* Specialization

Example:

```
/doctors/search?keyword=cardio
```

---

### 🔃 Sorting

Sort doctors by:

* fee
* name
* experience_years

Example:

```
/doctors/sort?sort_by=fee
```

---

### 📄 Pagination

Browse doctors page by page.

Example:

```
/doctors/page?page=1&limit=3
```

---

### 🔥 Combined Browse Endpoint

Filter + Sort + Pagination combined.

Example:

```
/doctors/browse?keyword=cardio&sort_by=fee&order=asc&page=1&limit=2
```

---

## 📸 Screenshots

Swagger UI outputs for all APIs are included in the `screenshots` folder.

