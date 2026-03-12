from flask import Flask, render_template, jsonify
import pandas as pd
import os
app = Flask(__name__)
LOG_FILE = 'network_log.csv'

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/data')
def get_data():
    if not os.path.isfile(LOG_FILE):
        return jsonify([])
    df = pd.read_csv(LOG_FILE)
    df = df.tail(50)  # Only return the last 50 readings
    df = df.fillna('null')  # Replace missing values with null for JSON
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
