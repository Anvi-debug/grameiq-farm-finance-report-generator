# GramIQ Farm Finance Report Generator

This project provides a Flask-based web application that allows farmers to enter crop, expense, and income details and generate a clean, structured PDF finance report. The system supports automatic calculations, dynamic charts, and repeated headers/footers in the final PDF for professional documentation.

## Features

* Form-based data entry for crop, farmer, income, and expense details
* Automatic calculations:

  * Total income
  * Total expense
  * Profit/Loss
  * Cost of cultivation per acre
* Auto-generated charts (Income vs Expense) embedded inside the PDF
* Repeating header with GramIQ branding on all PDF pages
* Repeating footer on all pages
* Clean and print-ready PDF layout built using `xhtml2pdf`
* Structured tables for Expense Breakdown, Income Breakdown, and Ledger

## Project Structure

```
app.py
requirements.txt

static/
   charts/
   style.css
   logo.png

templates/
   form.html
   report.html
```

## Installation & Setup

1. Create and activate a virtual environment:

   ```
   python -m venv venv
   venv\Scripts\activate   # Windows
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the application:

   ```
   python app.py
   ```

4. Open the application in a browser:

   ```
   http://127.0.0.1:5000
   ```

## Usage

1. Fill in crop, farmer, expense, and income details in the form.
2. Submit the form to generate a structured finance report.
3. The system automatically produces:

   * Summary calculations
   * Categorized tables
   * Ledger entries
   * A chart image
4. A downloadable PDF file is generated with professional formatting.

## Requirements

* Python 3.9+
* Flask
* xhtml2pdf
* matplotlib
* Jinja2

(All required packages are included in `requirements.txt`.)

Author

This project was developed by Anvi Ghadge,
B.Tech student in Computer Science and Design, YCCE,
as part of the GramIQ Internship Assignment focused on building an automated farm finance report generator.
