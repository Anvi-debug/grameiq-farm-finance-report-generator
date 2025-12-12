**GramIQ Farm Finance Report Generator**

This project implements a Flask-based backend application that collects farm financial data and generates a structured PDF report following GramIQ’s reporting format. The system processes crop details, income entries, expense entries, and automatically produces a finance summary, ledger, and embedded chart.

## Features

* Form-based data collection for farmer, crop, income, and expense details
* Automatic calculations: total income, total expense, profit/loss, and cost of cultivation per acre
* Auto-generated ledger combining income and expense entries
* Income vs. Expense bar chart embedded directly in the PDF
* Repeating header with GramIQ logo
* Repeating footer on each page
* Clean, print-ready PDF layout with margins (1 inch top/bottom, 1.25 inches left/right)

## Project Structure

```
app.py
requirements.txt
static/
   ├── style.css
   ├── logo.png
   └── charts/
templates/
   ├── form.html
   └── report.html
```

## Setup Instructions

1. Clone the repository:

   ```
   git clone <repository-link>
   cd gramiq-farm-finance-report-generator
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   venv\Scripts\activate       (Windows)
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run the application:

   ```
   python app.py
   ```

5. Open the local server in a browser:

   ```
   http://127.0.0.1:5000
   ```

Fill the form and generate the PDF report.

## Requirements

The project uses the following main packages:

* Flask
* xhtml2pdf
* matplotlib

(All dependencies are listed in `requirements.txt`.)

## Author

Anvi Ghadge
B.Tech, Computer Science and Design
