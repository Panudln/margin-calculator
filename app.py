from decimal import Decimal, ROUND_HALF_UP, InvalidOperation, getcontext
from datetime import datetime
import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

getcontext().rounding = ROUND_HALF_UP

db = SQLAlchemy()
migrate = Migrate()

# Utility: quantize auf 2 Stellen

def q2(d: Decimal) -> Decimal:
    return d.quantize(Decimal("0.01"))


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    items = db.relationship("QuoteItem", backref="quote", cascade="all, delete-orphan")


class QuoteItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey("quote.id"))
    ek_netto = db.Column(db.Numeric(10, 2))
    ek_brutto = db.Column(db.Numeric(10, 2))
    mwst = db.Column(db.Numeric(5, 2))
    aufschlag = db.Column(db.Numeric(10, 2))
    aufschlag_typ = db.Column(db.String(1))
    vk_netto = db.Column(db.Numeric(10, 2))
    vk_brutto = db.Column(db.Numeric(10, 2))


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.setdefault(
        "SQLALCHEMY_DATABASE_URI",
        os.getenv("DATABASE_URL", "sqlite:///quotes.db"),
    )
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/", methods=["GET", "POST"])
    @app.route("/quote/<int:quote_id>", methods=["GET", "POST"])
    def index(quote_id=None):
        quote = Quote.query.get(quote_id) if quote_id else None
        item = quote.items[0] if quote and quote.items else QuoteItem()
        result = None

        ek_netto = request.form.get("ek_netto") or (item.ek_netto or "")
        ek_brutto = request.form.get("ek_brutto") or (item.ek_brutto or "")
        mwst_raw = request.form.get("mwst") or (item.mwst or "19")
        aufschlag = request.form.get("aufschlag") or (item.aufschlag or "")
        aufschlag_typ = request.form.get("aufschlag_typ") or (item.aufschlag_typ or "%")

        try:
            if request.method == "POST":
                if not ek_netto and not ek_brutto:
                    raise ValueError("Bitte EK Netto oder EK Brutto angeben.")
                if ek_netto and ek_brutto:
                    raise ValueError("Bitte nur einen EK-Wert ausfüllen, nicht beide.")

                mwst = Decimal(str(mwst_raw))
                if ek_netto:
                    en = Decimal(str(ek_netto))
                    ek_netto_val = q2(en)
                    ek_brutto_val = q2(ek_netto_val * (Decimal(1) + mwst / Decimal(100)))
                else:
                    eb = Decimal(str(ek_brutto))
                    ek_brutto_val = q2(eb)
                    ek_netto_val = q2(ek_brutto_val / (Decimal(1) + mwst / Decimal(100)))

                vk_netto = None
                vk_brutto = None
                if aufschlag:
                    a = Decimal(str(aufschlag))
                    if aufschlag_typ == "%":
                        vk_netto = q2(ek_netto_val * (Decimal(1) + a / Decimal(100)))
                    else:
                        vk_netto = q2(ek_netto_val + a)
                    vk_brutto = q2(vk_netto * (Decimal(1) + mwst / Decimal(100)))

                result = {
                    "EK Netto": f"{ek_netto_val:.2f} €",
                    "EK Brutto": f"{ek_brutto_val:.2f} €",
                }
                if vk_netto is not None:
                    result["VK Netto (inkl. Marge)"] = f"{vk_netto:.2f} €"
                    result["VK Brutto (inkl. Marge)"] = f"{vk_brutto:.2f} €"

                item.ek_netto = ek_netto_val
                item.ek_brutto = ek_brutto_val
                item.mwst = mwst
                item.aufschlag = Decimal(str(aufschlag or 0))
                item.aufschlag_typ = aufschlag_typ
                item.vk_netto = vk_netto
                item.vk_brutto = vk_brutto

                if not quote:
                    quote = Quote(items=[item])
                db.session.add(quote)
                db.session.commit()
        except (InvalidOperation, ValueError) as e:
            result = {"Fehler": str(e)}

        return render_template(
            "index.html",
            result=result,
            ek_netto=str(ek_netto),
            ek_brutto=str(ek_brutto),
            mwst=str(mwst_raw),
            aufschlag=str(aufschlag),
            aufschlag_typ=aufschlag_typ,
            quote_id=quote.id if quote else None,
        )

    @app.route("/quotes")
    def quotes():
        quotes_list = Quote.query.order_by(Quote.created_at.desc()).all()
        return render_template("quotes.html", quotes=quotes_list)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
