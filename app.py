from flask import Flask, render_template, request
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation, getcontext

# Saubere Rundung: immer kaufmännisch auf 2 Nachkommastellen
getcontext().rounding = ROUND_HALF_UP

app = Flask(__name__)

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
            if mwst < 0 or mwst > 100:
                raise ValueError("MwSt muss zwischen 0 und 100 liegen.")
            if ek_netto:
                en = Decimal(ek_netto)
                if en < 0:
                    raise ValueError("EK Netto darf nicht negativ sein.")
                ek_netto_val  = q2(en)
                ek_brutto_val = q2(ek_netto_val * (Decimal(1) + mwst/Decimal(100)))
            else:
                eb = Decimal(ek_brutto)
                if eb < 0:
                    raise ValueError("EK Brutto darf nicht negativ sein.")
                ek_brutto_val = q2(eb)
                ek_netto_val  = q2(ek_brutto_val / (Decimal(1) + mwst/Decimal(100)))

            # Marge anwenden
            vk_netto = None
            if aufschlag:
                a = Decimal(aufschlag)
                if a < 0:
                    raise ValueError("Aufschlag darf nicht negativ sein.")
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

    except (InvalidOperation, ValueError) as e:
        result = {"Fehler": str(e)}

    return render_template(
        "index.html",
        result=result,
        ek_netto=str(ek_netto),
        ek_brutto=str(ek_brutto),
        mwst=str(mwst_raw),
        aufschlag=str(aufschlag),
        aufschlag_typ=aufschlag_typ
    )

if __name__ == "__main__":
    app.run(debug=True)
