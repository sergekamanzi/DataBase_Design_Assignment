# DataBase_Design_Assignment

- **Database Design** (SQL & MongoDB)  
- **API Implementation** (FastAPI)  
- **Prediction Script** (ML Model)  

---

### **Bank Deposit Prediction System**  

A Machine Learning-backed system that predicts whether a client will deposit in a bank based on given features. The project involves **database design (SQL & MongoDB), CRUD API implementation (FastAPI) and a prediction script using ML**.  

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
📦 Bank Deposit Prediction API
├── 📂 Fetch_Predict            # Task 3 - Prediction script
├── 📂 MONGO                    # MongoDB setup and scripts
│   ├── mongodb_insert.py      # Script to insert data into MongoDB
├── 📂 Mongo_api                # API for MongoDB operations
│   ├── routes.py              # Routes for MongoDB-based CRUD operations
├── 📂 SQL                      # SQL database setup
│   ├── db                     # MySQL Database Scripts
├── 📂 mySQL_api                # API for MySQL operations
│   ├── api                    # MySQL CRUD operations
├── .gitignore                  # Git ignore file
├── README.md                   # Project Documentation
├── bank.csv                    # Dataset used for training and testing
├── banking.ipynb                # Jupyter Notebook for ML model training
```


## **Database Design**  

We implemented **two databases**:  

### **SQL Relational Database (MySQL)**  

- **Tables:**
  - `clients `
  - `contacts`
  - `deposits`
  - `balance_logs`

- **Primary & Foreign Keys:**
 Primary Keys (PKs):
clients: client_id (PK)
contacts: contact_id (PK)
balance_logs: log_id (PK)
deposits: deposit_id (PK)

 Foreign Keys (FKs):
contacts: client_id → References clients(client_id)
balance_logs: client_id → References clients(client_id)
deposits: client_id → References clients(client_id)
- **Stored Procedure:**  

  - A procedure to **automatically insert data** into the `transactions` table.  


### **MongoDB Schema**  

- Collection: `bank_customers`
  ```json
  {
  "_id": ObjectId(),
  "client_id": 123,
  "features": {
    "age": 45,
    "job": "technician",
    "balance": 1500,
    "duration": 300,
    "campaign": 2,
    "pdays": -1,
    "previous": 0,
    "housing": "yes",
    "loan": "no"
  },
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
git clone https://github.com/sergekamanzi/DataBase_Design_Assignment.git
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
 - Serge - Database design & implementation
 - Willy - FastAPI CRUD API
 - Geofrey - Data fetching & predictions


---
