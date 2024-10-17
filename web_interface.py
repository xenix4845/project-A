from flask import Flask, render_template, request, redirect, url_for
from data_fetcher import fetch_heat_wave_data

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/board', methods=['POST'])
def board():
    year = request.form.get('year')
    sido = request.form.get('sido')
    
    if not year:
        return redirect(url_for('index'))
    
    try:
        year = int(year)
        if year < 1900 or year > 2100:
            raise ValueError
    except ValueError:
        return redirect(url_for('index'))
    
    data = fetch_heat_wave_data(year, sido)
    
    if not data:
        return redirect(url_for('index'))
    
    return render_template('board.html', year=year, sido=sido, data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)