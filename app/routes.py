from app import app
import mysql.connector
import pandas as pd
import mysql.connector
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import numpy as np 
from flask import jsonify

db_config = {
    'host': 'localhost',
    'user': 'root', 
    'password': '',
    'database': 'plan_pdm'
}

@app.route('/')
def get_data_from_table():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM mst_history LIMIT 10")

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return '\n'.join(str(row) for row in rows) 

    except Exception as e:
        return f"Failed to fetch data from the database: {str(e)}"

@app.route('/arimatest')
def fetch_data_from_database_and_predict():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT do_date, device_name, mst_history.value FROM mst_history WHERE area_name = 'OCI1' AND device_name = 'CAP - FEEDER C/V 1' AND test_name = '2H'")

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        if not rows:
            return jsonify({'error': 'No data found in the database'})

        df = pd.DataFrame(rows, columns=['Date', 'Device_Name', 'Value'])  
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

        df['Diff'] = df['Value'].diff()  # Calculate the differences

        response_data = {
            'fetched_data': df.to_dict(orient='records')
        }

        return jsonify(response_data)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Failed to fetch data from the database'})

if __name__ == "__main__":
    app.run(debug=True)