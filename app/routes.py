from app import app
import mysql.connector

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'plan_pdm'
}

# Route to test the database connection
@app.route('/')
@app.route('/')
def get_data_from_table():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Execute a query to fetch data from the mst_history table with a limit of 10 rows
        cursor.execute("SELECT * FROM mst_history LIMIT 10")

        # Fetch all rows
        rows = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return the data as a string (for simplicity)
        return '\n'.join(str(row) for row in rows)

    except Exception as e:
        return f"Failed to fetch data from the database: {str(e)}"