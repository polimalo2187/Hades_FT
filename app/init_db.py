# app/init_db.py

from pymongo import MongoClient
import os
from datetime import datetime, timedelta

# =========================
# CONFIGURACIÓN MONGODB
# =========================
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

if not MONGODB_URI or not DATABASE_NAME:
    raise RuntimeError("MONGODB_URI o DATABASE_NAME no están definidos")

client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

# =========================
# COLECCIONES PRINCIPALES
# =========================
collections = ["users", "signals", "user_signals"]
for col in collections:
    if col not in db.list_collection_names():
        db.create_collection(col)
        print(f"✅ Colección creada: {col}")
    else:
        print(f"ℹ️ Colección ya existe: {col}")

# =========================
# USUARIO DE PRUEBA
# =========================
users_col = db["users"]

test_user_id = 123456789  # Cambia por tu ID de prueba o deja así
existing = users_col.find_one({"user_id": test_user_id})
if not existing:
    users_col.insert_one({
        "user_id": test_user_id,
        "username": "test_user",
        "plan": "PREMIUM",
        "trial_end": datetime.utcnow() + timedelta(days=7),
        "plan_end": datetime.utcnow() + timedelta(days=30),
        "referred_by": None,
        "ref_code": f"ref_{test_user_id}",
        "ref_plus_valid": 0,
        "ref_premium_valid": 0,
        "ref_plus_total": 0,
        "ref_premium_total": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    print(f"✅ Usuario de prueba insertado: {test_user_id}")
else:
    print(f"ℹ️ Usuario de prueba ya existe: {test_user_id}")
