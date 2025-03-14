# DataBase_Design_Assignment

- **Database Design** (SQL & MongoDB)  
- **API Implementation** (FastAPI)  
- **Prediction Script** (ML Model)  

---

### **Bank Deposit Prediction System**  

A Machine Learning-backed system that predicts whether a client will deposit in a bank based on given features. The project involves **database design (SQL & MongoDB), CRUD API implementation (FastAPI), and a prediction script using ML**.  

---

## **Project Overview**    

1. **Database Design & Implementation**  
   - Databases  **SQL & MongoDB**  
   -  **ERD Diagram**  
   - **Stored Procedures & Triggers were employed**  
2. **FastAPI CRUD API**  
   - **Create, Read, Update, Delete (CRUD)** endpoints  
   - APIs interacting with the **Relational Database**  
3. **Prediction Script**  
   - The script fetches the latest entry  
   - It prepares the input for ML Model  
   - It predicts whether a client will deposit in a bank or not   

---

## **Project Structure**  

```
📦 Bank-Deposit-Prediction
│── 📂 database
│   ├── erd_diagram.png
│   ├── sql_schema.sql
│   ├── mongodb_schema.json
│   ├── stored_procedures.sql
│   ├── triggers.sql
│── 📂 api
│   ├── main.py  # FastAPI app
│   ├── models.py  # SQLAlchemy ORM models
│   ├── database.py  # DB connection
│   ├── routes.py  # CRUD endpoints
│── 📂 ml_model
│   ├── model.pkl  # Trained ML model
│   ├── predict.py  # Prediction script
│── 📂 data
│   ├── bank.csv  # Dataset
│── 📜 requirements.txt
│── 📜 README.md
```

---

## **Database Design**  

We implemented **two databases**:  

### **SQL Relational Database (MySQL)**  

- **Tables:**
  - `clients (client_id, name, age, job, balance, deposit_status)`
  - `transactions (transaction_id, client_id, amount, type, date)`
  - `accounts (account_id, client_id, account_type, created_at)`

- **Primary & Foreign Keys:**
  - `client_id` in `clients` is **Primary Key**  
  - `client_id` in `transactions` is a **Foreign Key**  

- **Stored Procedure:**  
  - A procedure to **automatically insert data** into the `transactions` table.  

- **Trigger:**  
  - A trigger to **log balance updates** when a transaction occurs.  

### ✅ **MongoDB Schema**  

- Collection: `bank_customers`
  ```json
  {
    "_id": "ObjectId",
    "name": "serge kamanzi",
    "age": 30,
    "job": "software Engineer",
    "balance": 5000,
    "deposit_status": "Yes"
  }
  ```

---

## **FastAPI - CRUD Endpoints**  

### **Create (POST)**
```python
@app.post("/clients/")
def create_client(client: ClientSchema, db: Session = Depends(get_db)):
```

###  **Read (GET)**
```python
@app.get("/clients/{client_id}")
def read_client(client_id: int, db: Session = Depends(get_db)):
```

### **Update (PUT)**
```python
@app.put("/clients/{client_id}")
def update_client(client_id: int, client: ClientSchema, db: Session = Depends(get_db)):
```

###  **Delete (DELETE)**
```python
@app.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
```

---

##  **Prediction Script (ML Model)**  

1. **Fetching the latest data from the API**  
2. **Prepares input for the model**  
3. **Makes prediction (Yes/No for deposit)**  

---

## **Setup & Installation**  

 **Clone the Repository**  
```bash
git clone https://github.com/yourrepo/bank-deposit-prediction.git
cd bank-deposit-prediction
```

 **Install Dependencies**  
```bash
pip install -r requirements.txt
```

 **Run FastAPI Server**  
```bash
uvicorn api.main:app --reload
```

 **Test API Endpoints**  
Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  

 **Run Prediction Script**  
```bash
python ml_model/predict.py
```

---

##  **Contributors**  

 **Team Members:**  
- Geofrey  
- Serge  
- Willy  
---
