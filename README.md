# Flask API with 2FA, JWT Authentication, and CRUD Operations

## 📌 Project Overview
This project is a **secure Flask API** that handles **user authentication, Two-Factor Authentication (2FA)** using **Google Authenticator**, and **JWT-based authentication** to protect CRUD operations on a `Products` table.

## 🚀 Features
- **User Registration** (Password Hashing + Google Authenticator Secret Key)
- **Login with 2FA** (QR Code Generation & Verification)
- **JWT Token Authentication** (Valid for 10 minutes)
- **CRUD Operations** on `Products` (JWT-Secured)

---

## 🛠️ Setup Instructions

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/Flask-Secure-Auth.git
cd Flask-Secure-Auth
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Configure MySQL Database**
```sql
CREATE DATABASE security_db;
USE security_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL,
    twofa_secret VARCHAR(256) NOT NULL
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    price DECIMAL(10,2),
    quantity INT
);
```

### **4️⃣ Set Up Environment Variables**
Create a `.env` file in the project root:
```env
SECRET_KEY=your_secret_key
DATABASE_URI=mysql+pymysql://root:password@localhost/security_db
```

### **5️⃣ Run Database Migrations**
```bash
python
>>> from models import db
>>> from app import app
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

### **6️⃣ Start the Flask Server**
```bash
python app.py
```

---

## 🔑 API Endpoints

### **1️⃣ User Registration**
`POST /register`
```json
{
  "username": "testuser",
  "password": "securepassword"
}
```

### **2️⃣ Generate 2FA QR Code**
`GET /generate-qr/<username>`

### **3️⃣ Verify 2FA Code**
`POST /verify-2fa`
```json
{
  "username": "testuser",
  "code": "123456"
}
```

### **4️⃣ Login & Get JWT Token**
`POST /login`
```json
{
  "username": "testuser",
  "password": "securepassword",
  "code": "123456"
}
```
_Response:_
```json
{
  "token": "your_jwt_token_here"
}
```

### **5️⃣ CRUD Operations on Products (Requires JWT in Headers)**
#### **🔹 Create Product**
`POST /products` (Requires `Authorization: Bearer <JWT>`)
```json
{
  "name": "Laptop",
  "description": "Gaming Laptop",
  "price": 1200.00,
  "quantity": 5
}
```
#### **🔹 Get All Products**
`GET /products` (Requires `Authorization: Bearer <JWT>`)

#### **🔹 Update a Product**
`PUT /products/<id>` (Requires `Authorization: Bearer <JWT>`)

#### **🔹 Delete a Product**
`DELETE /products/<id>` (Requires `Authorization: Bearer <JWT>`)

---

## ✅ Testing with Postman
1. **Register a user**
2. **Generate a QR Code** and scan it in **Google Authenticator**
3. **Verify 2FA Code**
4. **Login & Get JWT Token**
5. **Use JWT Token for CRUD operations**

---

## 🏗️ Built With
- **Flask** (Python Web Framework)
- **Flask-JWT-Extended** (JWT Authentication)
- **PyQRCode** (QR Code Generation for 2FA)
- **MySQL + SQLAlchemy** (Database)
- **Google Authenticator** (2FA Code Verification)

---

## 💡 Future Improvements
- ✅ Role-Based Access Control (RBAC)
- ✅ Password Reset Feature
- ✅ Email Verification
