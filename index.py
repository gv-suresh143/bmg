from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://www.livechennai.com/gold_silverrate.asp'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract rows containing date and price information
    data = []
    rows = soup.find_all('tr')
    for row in rows:
        date_col = row.find('td', class_='date-col')
        price_cols = row.find_all('td')[1:]
        if date_col and len(price_cols) >= 3:
            date = date_col.text.strip()
            prices = [int(col.text.strip().replace(',', '')) for col in price_cols]
            # Calculate 8 grams price for 22k and 24k
            price_1g_24k, price_1g_22k = prices[0], prices[2]
            price_8g_24k = price_1g_24k * 8
            price_8g_22k = price_1g_22k * 8
            data.append({
                'date': date,
                'price_1g_24k': price_1g_24k,
                'price_8g_24k': price_8g_24k,
                'price_1g_22k': price_1g_22k,
                'price_8g_22k': price_8g_22k
            })

    # HTML template to display the data
    html_template = """
    <html>
    <head><title>Gold and Silver Prices</title></head>
    <body>
        <h1>Gold and Silver Prices</h1>
        <p>Current Date: {{ current_date }}</p>
        <table border="1">
            <tr>
                <th>Date</th>
                <th>1 Gram (24K)</th>
                <th>8 Grams (24K)</th>
                <th>1 Gram (22K)</th>
                <th>8 Grams (22K)</th>
            </tr>
            {% for entry in data %}
            <tr>
                <td>{{ entry.date }}</td>
                <td>{{ entry.price_1g_24k }}</td>
                <td>{{ entry.price_8g_24k }}</td>
                <td>{{ entry.price_1g_22k }}</td>
                <td>{{ entry.price_8g_22k }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    return render_template_string(html_template, data=data, current_date=datetime.now().strftime('%d-%b-%Y %H:%M'))

if __name__ == '__main__':
    app.run(debug=True) 