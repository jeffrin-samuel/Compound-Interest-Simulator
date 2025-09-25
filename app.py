from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for Flask
import matplotlib.pyplot as plt
import io, base64
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    balances = []
    img = None

    if request.method == "POST":
        # Get form data
        principal = float(request.form["principal"])
        monthly_contribution = float(request.form["monthly_contribution"])
        annual_rate = float(request.form["annual_rate"])
        years = int(request.form["years"])

        monthly_rate = annual_rate / 100 / 12
        total = principal

        # Calculate balances
        for year in range(1, years + 1):
            for month in range(12):
                total += monthly_contribution
                total += total * monthly_rate
            balances.append(total)

        # Create graph
        plt.figure()
        plt.plot(range(1, years + 1), balances, marker='o', color='blue')
        plt.title("Compound Interest Growth")
        plt.xlabel("Years")
        plt.ylabel("Balance (₹)")
        plt.grid(True)

        # Save plot as base64 to embed in HTML
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img = base64.b64encode(buf.getvalue()).decode("utf-8")
        buf.close()

    return render_template("index.html", balances=balances, img=img)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
