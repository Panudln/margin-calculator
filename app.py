from flask import Flask, render_template, request, session, send_file, make_response
import csv
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation, getcontext
from io import BytesIO, StringIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Saubere Rundung: immer kaufmännisch auf 2 Nachkommastellen
getcontext().rounding = ROUND_HALF_UP

app = Flask(__name__)
app.secret_key = "dev-key"

# Utility: quantize auf 2 Stellen
def q2(d: Decimal) -> Decimal:
    return d.quantize(Decimal("0.01"))

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    ek_netto = request.form.get("ek_netto", "")
    ek_brutto = request.form.get("ek_brutto", "")
    mwst_raw = request.form.get("mwst", "19")
    aufschlag = request.form.get("aufschlag", "")
    aufschlag_typ = request.form.get("aufschlag_typ", "%")

    try:
        # Basisprüfung: genau ein Einkaufspreis-Feld muss gefüllt sein
        if request.method == "POST":
            if not ek_netto and not ek_brutto:
                raise ValueError("Bitte EK Netto oder EK Brutto angeben.")
            if ek_netto and ek_brutto:
                raise ValueError("Bitte nur einen EK-Wert ausfüllen, nicht beide.")

            # Decimal-Konvertierung
            mwst = Decimal(mwst_raw)
            if ek_netto:
                en = Decimal(ek_netto)
                ek_netto_val  = q2(en)
                ek_brutto_val = q2(ek_netto_val * (Decimal(1) + mwst/Decimal(100)))
            else:
                eb = Decimal(ek_brutto)
                ek_brutto_val = q2(eb)
                ek_netto_val  = q2(ek_brutto_val / (Decimal(1) + mwst/Decimal(100)))

            # Marge anwenden
            vk_netto = None
            if aufschlag:
                a = Decimal(aufschlag)
                if aufschlag_typ == "%":
                    vk_netto = q2(ek_netto_val * (Decimal(1) + a/Decimal(100)))
                else:  # Euro
                    vk_netto = q2(ek_netto_val + a)

            # Ergebnis-Dict mit Ausgabe-Strings
            result = {
                "EK Netto":  f"{ek_netto_val:.2f} €",
                "EK Brutto": f"{ek_brutto_val:.2f} €"
            }
            if vk_netto is not None:
                vk_brutto = q2(vk_netto * (Decimal(1) + mwst/Decimal(100)))
                result["VK Netto (inkl. Marge)"]  = f"{vk_netto:.2f} €"
                result["VK Brutto (inkl. Marge)"] = f"{vk_brutto:.2f} €"

            session['result'] = result
        else:
            session.pop('result', None)

    except (InvalidOperation, ValueError) as e:
        result = {"Fehler": str(e)}
        session['result'] = result

    return render_template(
        "index.html",
        result=result,
        ek_netto=str(ek_netto),
        ek_brutto=str(ek_brutto),
        mwst=str(mwst_raw),
        aufschlag=str(aufschlag),
        aufschlag_typ=aufschlag_typ
    )


@app.route("/export")
def export():
    fmt = request.args.get("format", "csv")
    result = session.get("result")
    if not result:
        return "No result", 400
    if fmt == "pdf":
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        y = 750
        p.setFont("Helvetica", 12)
        p.drawString(100, y, "Berechnungsergebnis")
        y -= 20
        for key, value in result.items():
            p.drawString(100, y, f"{key}: {value}")
            y -= 15
        p.showPage()
        p.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True,
                         download_name="result.pdf", mimetype="application/pdf")
    else:
        buffer = StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["Key", "Value"])
        for k, v in result.items():
            writer.writerow([k, v])
        output = make_response(buffer.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=result.csv"
        output.headers["Content-Type"] = "text/csv"
        return output

if __name__ == "__main__":
    app.run(debug=True)
