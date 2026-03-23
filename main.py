from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
import math

app = FastAPI()

# -------------------- Q1 --------------------
@app.get("/")
def home():
    return {"message": "Welcome to MediCare Clinic"}

# -------------------- DATA --------------------
doctors = [
    {"id": 1, "name": "Dr. A", "specialization": "Cardiologist", "fee": 500, "experience_years": 10, "is_available": True},
    {"id": 2, "name": "Dr. B", "specialization": "Dermatologist", "fee": 300, "experience_years": 5, "is_available": True},
    {"id": 3, "name": "Dr. C", "specialization": "Pediatrician", "fee": 400, "experience_years": 8, "is_available": False},
    {"id": 4, "name": "Dr. D", "specialization": "General", "fee": 200, "experience_years": 3, "is_available": True},
    {"id": 5, "name": "Dr. E", "specialization": "Cardiologist", "fee": 600, "experience_years": 12, "is_available": False},
    {"id": 6, "name": "Dr. F", "specialization": "Dermatologist", "fee": 350, "experience_years": 6, "is_available": True},
]

appointments = [
    {
        "appointment_id": 1,
        "patient": "Riya",
        "doctor": "Dr. A",
        "doctor_id": 1,
        "date": "2026-03-22",
        "type": "video",
        "status": "scheduled"
    },
    {
        "appointment_id": 2,
        "patient": "Rahul",
        "doctor": "Dr. B",
        "doctor_id": 2,
        "date": "2026-03-23",
        "type": "in-person",
        "status": "confirmed"
    }
]

appt_counter = 3

# -------------------- HELPERS  --------------------

def find_doctor(doctor_id: int):
    for doc in doctors:
        if doc["id"] == doctor_id:
            return doc
    return None

def calculate_fee(base_fee: int, appointment_type: str, senior: bool = False):
    if appointment_type == "video":
        fee = base_fee * 0.8
    elif appointment_type == "emergency":
        fee = base_fee * 1.5
    else:
        fee = base_fee

    original_fee = fee

    if senior:
        fee = fee * 0.85   # 15% discount

    return round(original_fee, 2), round(fee, 2)

def filter_doctors_logic(
    specialization=None,
    max_fee=None,
    min_experience=None,
    is_available=None
):
    result = doctors

    if specialization is not None:
        result = [
            d for d in result
            if d["specialization"].lower() == specialization.lower()
        ]

    if max_fee is not None:
        result = [
            d for d in result
            if d["fee"] <= max_fee
        ]

    if min_experience is not None:
        result = [
            d for d in result
            if d["experience_years"] >= min_experience
        ]

    if is_available is not None:
        result = [
            d for d in result
            if d["is_available"] == is_available
        ]

    return result
from pydantic import BaseModel, Field

#  -------------------- Q5 --------------------
@app.get("/doctors/summary")
def doctors_summary():
    total = len(doctors)
    available = [d for d in doctors if d["is_available"]]

    most_exp = max(doctors, key=lambda x: x["experience_years"])
    cheapest = min(doctors, key=lambda x: x["fee"])

    spec_count = {}
    for d in doctors:
        spec = d["specialization"]
        spec_count[spec] = spec_count.get(spec, 0) + 1

    return {
        "total_doctors": total,
        "available_count": len(available),
        "most_experienced_doctor": most_exp["name"],
        "cheapest_fee": cheapest["fee"],
        "specialization_count": spec_count
    }

# -------------------- Q2 --------------------
@app.get("/doctors")
def get_doctors():
    available = [d for d in doctors if d["is_available"]]
    return {
        "total": len(doctors),
        "available_count": len(available),
        "doctors": doctors
    }



# -------------------- Q4 --------------------
@app.get("/appointments")
def get_appointments():
    return {
        "total": len(appointments),
        "appointments": appointments
    }
    


# -------------------- Q6 --------------------
class AppointmentRequest(BaseModel):
    patient_name: str = Field(..., min_length=2)
    doctor_id: int = Field(..., gt=0)
    date: str = Field(..., min_length=8)
    reason: str = Field(..., min_length=5)
    appointment_type: str = "in-person"
    senior_citizen: bool = False

# -------------------- Q8 --------------------
@app.post("/appointments")
def create_appointment(req: AppointmentRequest):
    global appt_counter

    doc = find_doctor(req.doctor_id)
    if not doc:
        raise HTTPException(404, "Doctor not found")

    if not doc["is_available"]:
        raise HTTPException(400, "Doctor not available")

    original_fee, final_fee = calculate_fee(
        doc["fee"], req.appointment_type, req.senior_citizen
    )

    appt = {
        "appointment_id": appt_counter,
        "patient": req.patient_name,
        "doctor": doc["name"],
        "doctor_id": doc["id"],
        "date": req.date,
        "type": req.appointment_type,
        "original_fee": original_fee,
        "final_fee": final_fee,
        "status": "scheduled"
    }

    appointments.append(appt)
    doc["is_available"] = False
    appt_counter += 1

    return appt

# -------------------- Q10 --------------------
@app.get("/doctors/filter", response_model=dict)
def filter_doctors(
    specialization: str = Query(None),
    max_fee: int = Query(None),
    min_experience: int = Query(None),
    is_available: bool = Query(None)
):
    result = filter_doctors_logic(
        specialization,
        max_fee,
        min_experience,
        is_available
    )

    return {"count": len(result), "doctors": result}

# -------------------- Q11 --------------------
class NewDoctor(BaseModel):
    name: str = Field(..., min_length=2)
    specialization: str = Field(..., min_length=2)
    fee: int = Field(..., gt=0)
    experience_years: int = Field(..., gt=0)
    is_available: bool = True

@app.post("/doctors", status_code=201)
def add_doctor(doc: NewDoctor):
    for d in doctors:
        if d["name"].lower() == doc.name.lower():
           raise HTTPException(status_code=400, detail="Duplicate doctor")

    new_doc = doc.dict()
    new_doc["id"] = len(doctors) + 1
    doctors.append(new_doc)
    return new_doc

# -------------------- Q12 --------------------
@app.put("/doctors/{doctor_id}")
def update_doctor(
    doctor_id: int,
    fee: Optional[int] = None,
    is_available: Optional[bool] = None
):
    doc = find_doctor(doctor_id)

    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if fee is not None:
        doc["fee"] = fee

    if is_available is not None:
        doc["is_available"] = is_available

    return doc

# -------------------- Q13 --------------------
@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    doc = find_doctor(doctor_id)

    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")

    for a in appointments:
        if a["doctor_id"] == doctor_id and a["status"] == "scheduled":
            raise HTTPException(status_code=400, detail="Doctor has active appointments")

    doctors.remove(doc)
    return {"message": "Deleted successfully"}

# -------------------- Q14 --------------------
@app.post("/appointments/{appointment_id}/confirm")
def confirm(appointment_id: int):
    for a in appointments:
        if a["appointment_id"] == appointment_id:
            a["status"] = "confirmed"
            return a
    raise HTTPException(status_code=404, detail="Appointment not found")


@app.post("/appointments/{appointment_id}/cancel")
def cancel(appointment_id: int):
    for a in appointments:
        if a["appointment_id"] == appointment_id:
            a["status"] = "cancelled"
            doc = find_doctor(a["doctor_id"])
            if doc:
                doc["is_available"] = True
            return a
    raise HTTPException(status_code=404, detail="Appointment not found")

# -------------------- Q15 --------------------
@app.post("/appointments/{appointment_id}/complete")
def complete(appointment_id: int):
    for a in appointments:
        if a["appointment_id"] == appointment_id:
            a["status"] = "completed"
            return a
    raise HTTPException(status_code=404, detail="Appointment not found")


@app.get("/appointments/active")
def active():
    result = [a for a in appointments if a["status"] in ["scheduled", "confirmed"]]
    return result


@app.get("/appointments/by-doctor/{doctor_id}")
def by_doctor(doctor_id: int):
    result = [a for a in appointments if a["doctor_id"] == doctor_id]
    return result
# -------------------- Q16 --------------------
@app.get("/doctors/search")
def search(keyword: str):
    result = [
        d for d in doctors
        if keyword.lower() in d["name"].lower()
        or keyword.lower() in d["specialization"].lower()
    ]
    if not result:
        return {"message": "No matches found"}
    return {"total_found": len(result), "results": result}

# -------------------- Q17 --------------------
@app.get("/doctors/sort")
def sort(sort_by: str = "fee", order: str = "asc"):

    if sort_by not in ["fee", "name", "experience_years"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order")

    reverse = True if order == "desc" else False

    result = sorted(doctors, key=lambda x: x[sort_by], reverse=reverse)

    return {
        "sorted_by": sort_by,
        "order": order,
        "data": result
    }

# -------------------- Q18 --------------------
@app.get("/doctors/page")
def paginate(page: int = 1, limit: int = 3):
    total = len(doctors)
    total_pages = math.ceil(total / limit)

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "total_pages": total_pages,
        "data": doctors[start:end]
    }

# -------------------- Q19 --------------------
@app.get("/appointments/search")
def search_appt(patient_name: str):
    result = [
        a for a in appointments
        if patient_name.lower() in a["patient"].lower()
    ]

    return {
        "total_found": len(result),
        "results": result
    }


@app.get("/appointments/sort")
def sort_appt(by: str = "date"):
    if by not in ["date", "fee"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    result = sorted(appointments, key=lambda x: x.get(by, ""))

    return {
        "sorted_by": by,
        "data": result
    }


@app.get("/appointments/page")
def page_appt(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "data": appointments[start:end]
    }

# -------------------- Q20 --------------------
@app.get("/doctors/browse")
def browse(
    keyword: Optional[str] = None,
    sort_by: str = "fee",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = doctors

    # 🔍 FILTER (name + specialization)
    if keyword:
        result = [
            d for d in result
            if keyword.lower() in d["name"].lower()
            or keyword.lower() in d["specialization"].lower()
        ]

    # ⚠ VALIDATION
    if sort_by not in ["fee", "name", "experience_years"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order")

    # 🔃 SORT
    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # 📄 PAGINATION
    total = len(result)
    total_pages = math.ceil(total / limit)

    start = (page - 1) * limit
    end = start + limit

    return {
        "total": total,
        "total_pages": total_pages,
        "page": page,
        "limit": limit,
        "sort_by": sort_by,
        "order": order,
        "data": result[start:end]
    }
# -------------------- Q3  --------------------
@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    doc = find_doctor(doctor_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doc
