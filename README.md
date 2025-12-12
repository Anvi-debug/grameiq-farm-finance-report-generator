# **GramIQ Farm Finance Report Generator**

GramIQ Farm Finance Report Generator This project provides a **Flask-based** web application that allows farmers to enter crop, expense, and income details and generate a clean, structured PDF finance report. The system supports automatic calculations, dynamic charts, and repeated headers/footers in the final PDF for professional documentation.
---

## **1. Project Overview**

The application collects farmer details, crop information, income entries, and expense records. After submitting the form, the system generates a professionally formatted PDF that includes:

* Repeating header and footer on every page
* Finance summary & calculations
* Income and expense tables
* Auto-generated ledger
* Embedded static chart
* Downloadable PDF file

---

## **2. Features**

### **2.1 Form-Based Data Entry**

The web form accepts all fields required by the assignment:

* Farmer name, crop, season, location, sowing & harvest dates
* Total acres
* Multiple expense entries (category, amount, date, description)
* Multiple income entries (category, amount, date, description)
  (Assignment Ref: Page 1 – “Create a Web Form”) 

### **2.2 Automatic Finance Calculations**

* Total Income
* Total Expense
* Total Production (if provided)
* Profit or Loss
* Cost of cultivation per acre
  *(Formula: Total Expense / Total Acres — as required)* 

### **2.3 PDF Report with Professional Layout**

The PDF includes:

#### **Header (every page)**

* GramIQ logo
* Dynamic report title: **crop_acres_season_year**
* Timestamp
* Farmer name
  (Assignment Ref: Page 1 – PDF Header Requirements) 

#### **Footer (every page)**

* *“Proudly maintained accounting with GramIQ”*
  (Assignment Ref: Page 2 – Footer Requirement) 

### **2.4 Structured Sections in PDF**

Exactly as required in the assignment:

1. **Finance Summary**

2. **Expense Breakdown Table**

3. **Income Breakdown Table**

4. **Ledger (auto-generated)**

   * Date
   * Particulars
   * Type (Income/Expense)
   * Description
   * Amount
     
5. **Embedded Chart**

   * Static chart: Income vs Expense (matplotlib)

---

## **3. Tech Stack**

### **Backend**

* Python 3.9+
* Flask (for routing, form handling)

### **PDF Generation**

* xhtml2pdf (HTML → PDF conversion)
* Jinja2 Templates

### **Charts**

* Matplotlib

### **Frontend**

* HTML/CSS templates
* Basic JavaScript for dynamic entry rows

(All libraries comply with assignment requirements.) 

---

## **4. Project Structure**

```
│── app.py                     # Main Flask application
│── requirements.txt
│
├── templates/
│     ├── form.html            # Form UI for all inputs
│     └── report.html          # PDF layout template
│
├── static/
│     ├── charts/              # Auto-generated chart images
│     ├── style.css            # Styles for PDF + form
│     └── logo.png             # GramIQ logo in header
```

---

## **5. Installation & Setup**

### **Step 1: Create a Virtual Environment**

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### **Step 2: Install Dependencies**

```
pip install -r requirements.txt
```

### **Step 3: Run the Application**

```
python app.py
```

### **Step 4: Open in Browser**

```
http://127.0.0.1:5000
```

---

## **6. How the Application Works (Step-by-Step)**

### **Step 1 — Fill the Form**

Enter farmer, crop, income, and expense details. Multiple rows can be added as required by the assignment.

### **Step 2 — Submit**

Data is sent to the Flask backend for processing.

### **Step 3 — Calculations & Chart Generation**

* Totals are computed.
* Cost per acre is calculated.
* Matplotlib chart (Income vs Expense) is generated and saved in `static/charts/`.

### **Step 4 — PDF Rendering**

* `report.html` is converted to PDF using xhtml2pdf.
* Header/footer repeat on all pages.
* Tables (income, expense, ledger) are auto-generated.

### **Step 5 — Download PDF**

A button appears allowing the user to download the final PDF.

---

## **7. PDF Structure Explanation**

The PDF matches the required format exactly:

1. **Header** with branding + dynamic title
2. **Finance Summary Section**
3. **Static Chart (Income vs Expense)**
4. **Expense Breakdown Table**
5. **Income Breakdown Table**
6. **Auto-generated Ledger**
7. **Footer** (repeated)

---

## **8. Error Handling**

* Invalid inputs return safe defaults
* Empty tables handled gracefully
* Missing fields validated server-side

---

## **10. Author**

**Anvi Ghadge**
B.Tech – Computer Science & Design
Project developed as part of the **GramIQ Backend Developer Internship Technical Assignment**. 

