
from flask import Flask, render_template, request, jsonify
from pytrends.request import TrendReq
import time

app = Flask(__name__)

# Configuration de PyTrends
pytrends = TrendReq(hl='fr-FR', tz=360)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trends', methods=['GET'])
def get_trends():
    product = request.args.get('product')
    if not product:
        return render_template('index.html', error_message="Le paramètre 'produit' est requis.")

    try:
        # Ajouter une pause pour éviter les erreurs 429
        time.sleep(5)

        # Effectuer la requête PyTrends
        pytrends.build_payload([product], timeframe='today 12-m', geo='')
        data = pytrends.interest_by_region()

        if product in data.columns and not data.empty:
            data = data.sort_values(by=[product], ascending=False).head(10)
            trends = []

            for country, value in data[product].items():
                trends.append({
                    'country': country,
                    'demande': f"{value:.0f}%",
                    'opportunite': "Forte demande" if value > 50 else "Demande modérée"
                })

            return render_template('index.html', trends=trends, product=product)
        else:
            return render_template('index.html', error_message="Aucune donnée trouvée pour ce produit.")

    except Exception as e:
        return render_template('index.html', error_message=f"Une erreur s'est produite: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
