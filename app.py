# app.py
import os
import base64
import logging
from io import BytesIO
from datetime import datetime
from flask import Flask, render_template, request, send_file, flash, redirect

# --- Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # ok for local dev only

# Ensure charts dir exists
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CHARTS_DIR = os.path.join(BASE_DIR, 'static', 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

def to_float(x):
    try:
        return float(x)
    except Exception:
        return 0.0

# --- Routes ---
@app.route("/", methods=["GET"])
def index():
    return render_template("form.html")


@app.route("/generate", methods=["POST"])
def generate():
    # --- Parse form fields ---
    farmer_name = request.form.get("farmer_name", "").strip()
    crop_name = request.form.get("crop_name", "").strip()
    season = request.form.get("season", "").strip()
    total_acres = to_float(request.form.get("total_acres", "0"))
    total_production = to_float(request.form.get("total_production", "0"))
    sowing_date = request.form.get("sowing_date", "")
    harvest_date = request.form.get("harvest_date", "")
    location = request.form.get("location", "")

    # Parse expense rows
    expense_categories = request.form.getlist("expense_category[]")
    expense_amounts = request.form.getlist("expense_amount[]")
    expense_dates = request.form.getlist("expense_date[]")
    expense_descs = request.form.getlist("expense_desc[]")
    expenses = []
    for cat, amt, dt, desc in zip(expense_categories, expense_amounts, expense_dates, expense_descs):
        if (cat or amt or dt or desc) and (amt.strip() != ""):
            expenses.append({
                "category": cat.strip(),
                "amount": to_float(amt),
                "date": dt,
                "description": desc.strip()
            })

    # Parse income rows
    income_categories = request.form.getlist("income_category[]")
    income_amounts = request.form.getlist("income_amount[]")
    income_dates = request.form.getlist("income_date[]")
    income_descs = request.form.getlist("income_desc[]")
    incomes = []
    for cat, amt, dt, desc in zip(income_categories, income_amounts, income_dates, income_descs):
        if (cat or amt or dt or desc) and (amt.strip() != ""):
            incomes.append({
                "category": cat.strip(),
                "amount": to_float(amt),
                "date": dt,
                "description": desc.strip()
            })

    # Basic validation
    if not farmer_name or not crop_name or total_acres <= 0:
        flash("Please provide Farmer Name, Crop Name and a positive Total Acres.", "error")
        return redirect("/")

    # --- Calculations ---
    total_expense = sum(e["amount"] for e in expenses)
    total_income = sum(i["amount"] for i in incomes)
    profit_loss = total_income - total_expense
    cost_per_acre = (total_expense / total_acres) if total_acres > 0 else 0.0

    # Ledger (merged)
    ledger = []
    for e in expenses:
        ledger.append({
            "date": e.get("date", ""),
            "particulars": e.get("category", ""),
            "type": "Expense",
            "description": e.get("description", ""),
            "amount": e.get("amount", 0.0)
        })
    for i in incomes:
        ledger.append({
            "date": i.get("date", ""),
            "particulars": i.get("category", ""),
            "type": "Income",
            "description": i.get("description", ""),
            "amount": i.get("amount", 0.0)
        })
    try:
        ledger.sort(key=lambda r: (r["date"] == "", r["date"]))
    except Exception:
        pass

    # --- Chart generation (matplotlib) ---
    chart_path = ""
    chart_path_rel = ""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(4, 3))
        labels = ['Income', 'Expense']
        values = [total_income, total_expense]
        bars = ax.bar(labels, values)
        ax.set_title('Income vs Expense')
        ax.set_ylabel('Amount')
        ax.grid(axis='y', linestyle='--', alpha=0.4)

        for bar in bars:
            h = bar.get_height()
            ax.annotate(f'{h:.2f}', xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 3), textcoords='offset points', ha='center', fontsize=9)

        chart_filename = f"chart_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        chart_path_rel = os.path.join(CHARTS_DIR, chart_filename)
        fig.tight_layout()
        fig.savefig(chart_path_rel, dpi=100)
        plt.close(fig)

        chart_path = 'file://' + os.path.abspath(chart_path_rel).replace('\\', '/')
        logger.info("Chart saved to %s", chart_path_rel)
    except Exception:
        logger.exception("Chart generation failed")
        chart_path = ""
        chart_path_rel = ""

    # --- Logo detection (absolute path) ---
    logo_abs = os.path.join(BASE_DIR, 'static', 'logo.png')
    logo_path = ''
    if os.path.exists(logo_abs):
        logo_path = 'file://' + os.path.abspath(logo_abs).replace('\\', '/')
    else:
        logger.info("Logo not found at %s (optional)", logo_abs)

    # --- Prepare Base64 embedded images (guaranteed to embed in PDF) ---
    logo_b64 = ""
    chart_b64 = ""
    try:
        if os.path.exists(logo_abs):
            with open(logo_abs, "rb") as f:
                logo_b64 = base64.b64encode(f.read()).decode("utf-8")
                logger.info("Logo base64 created (len=%d)", len(logo_b64))
    except Exception:
        logger.exception("Failed to read logo for base64")

    try:
        chart_abs = chart_path_rel if chart_path_rel else ""
        if chart_abs and os.path.exists(chart_abs):
            with open(chart_abs, "rb") as f:
                chart_b64 = base64.b64encode(f.read()).decode("utf-8")
                logger.info("Chart base64 created (len=%d)", len(chart_b64))
    except Exception:
        logger.exception("Failed to read chart for base64")

    # DEBUG lines (helpful)
    print("DEBUG: logo_abs exists?", os.path.exists(logo_abs))
    print("DEBUG: logo_path ->", logo_path)
    print("DEBUG: chart_path ->", chart_path)
    print("DEBUG: logo_b64 length:", len(logo_b64))
    print("DEBUG: chart_b64 length:", len(chart_b64))

    # --- Render HTML to string ---
    rendered = render_template(
        "report.html",
        farmer_name=farmer_name,
        crop_name=crop_name,
        season=season,
        total_acres=total_acres,
        total_production=total_production,
        sowing_date=sowing_date,
        harvest_date=harvest_date,
        location=location,
        total_income=total_income,
        total_expense=total_expense,
        profit_loss=profit_loss,
        cost_per_acre=cost_per_acre,
        expenses=expenses,
        incomes=incomes,
        ledger=ledger,
        generated_on=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        chart_path=chart_path,
        logo_path=logo_path,
        logo_b64=logo_b64,
        chart_b64=chart_b64
    )

    # --- Convert HTML to PDF (xhtml2pdf) and then stamp footer onto every page ---
    try:
        from xhtml2pdf import pisa
        # PyPDF2 and reportlab are used to overlay the footer on each page
        from PyPDF2 import PdfReader, PdfWriter
        from reportlab.pdfgen import canvas

        # Step 1: create initial PDF bytes from HTML
        pdf_io = BytesIO()
        pisa_status = pisa.CreatePDF(src=rendered, dest=pdf_io)
        if pisa_status.err:
            logger.error("xhtml2pdf reported errors: %s", pisa_status.err)
            return rendered  # fallback to HTML for debugging

        pdf_io.seek(0)

        # Step 2: read PDF pages
        reader = PdfReader(pdf_io)
        writer = PdfWriter()

        # Footer text and small style choices
        footer_text = "Proudly maintained accounting with GramIQ"

        # For each page create a ReportLab overlay and merge
        for page in reader.pages:
            media = page.mediabox
            page_width = float(media.right)
            page_height = float(media.top)

            # Create overlay PDF in memory
            packet = BytesIO()
            c = canvas.Canvas(packet, pagesize=(page_width, page_height))

            # Footer coordinates in points (1pt = 1/72 inch). Adjust footer_y for height.
            footer_y = 18  # distance from bottom in points
            c.setFont("Helvetica", 10)

            # draw thin line above footer
            c.setLineWidth(0.3)
            c.setStrokeColorRGB(0.7, 0.7, 0.7)
            c.line(24, footer_y + 14, page_width - 24, footer_y + 14)

            # centered footer
            c.setFillColorRGB(0.35, 0.35, 0.35)
            text_width = c.stringWidth(footer_text, "Helvetica", 10)
            x = (page_width - text_width) / 2.0
            c.drawString(x, footer_y, footer_text)

            c.save()
            packet.seek(0)

            # Merge overlay onto original page
            overlay_pdf = PdfReader(packet)
            overlay_page = overlay_pdf.pages[0]
            try:
                page.merge_page(overlay_page)
            except Exception:
                # fallback to older API name if needed
                try:
                    page.mergePage(overlay_page)
                except Exception:
                    logger.exception("Merge failed for a page")

            writer.add_page(page)

        # Step 3: write final PDF bytes
        final_pdf = BytesIO()
        writer.write(final_pdf)
        final_pdf.seek(0)

        # Send final PDF
        safe_crop = crop_name.replace(" ", "_") if crop_name else "report"
        filename = f"{safe_crop}_{int(total_acres)}_{season}_{datetime.now().strftime('%Y%m%d')}.pdf"
        return send_file(final_pdf, mimetype='application/pdf', as_attachment=True, download_name=filename)

    except Exception:
        logger.exception("PDF generation / footer stamping failed")
        # As a fallback, return HTML so you can debug quickly
        return rendered


if __name__ == "__main__":
    app.run(debug=True)