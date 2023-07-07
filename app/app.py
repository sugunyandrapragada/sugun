# import necessary libraries
import requests
from bs4 import BeautifulSoup
import mysql.connector
from fastapi import FastAPI

# Initialize the FastAPI app
app = FastAPI()

# Define the MySQL connection parameters
mysql_host = '127.0.0.1'
mysql_user = 'root'
mysql_password = 'P@ssw0rd-1'
mysql_db = 'users'

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_db
)

# Create a MySQL cursor object
cursor = connection.cursor()

# Create a table in the MySQL database for storing user data
create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL
    )
"""
cursor.execute(create_table_query)

# Define the scraping function to retrieve data from the website
def scrape_website():
    url = 'https://www.bseindia.com/markets/equity/EQReports/bulk_deals.aspx'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Scrape the required data from the website
    # Replace this code with your own web scraping logic

    # Insert the scraped data into the MySQL database
    insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    values = [("John Doe", "johndoe@example.com"), ("Jane Smith", "janesmith@example.com")]

    cursor.executemany(insert_query, values)
    connection.commit()

# Define the API endpoints for performing CRUD operations on the user table
@app.get("/users")
def get_users():
    select_query = "SELECT * FROM users"
    cursor.execute(select_query)
    result = cursor.fetchall()
    return {"users": result}

@app.post("/users")
def create_user(name: str, email: str):
    insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    values = (name, email)
    cursor.execute(insert_query, values)
    connection.commit()
    return {"message": "User created successfully"}

@app.put("/users/{user_id}")
def update_user(user_id: int, name: str, email: str):
    update_query = "UPDATE users SET name = %s, email = %s WHERE id = %s"
    values = (name, email, user_id)
    cursor.execute(update_query, values)
    connection.commit()
    return {"message": "User updated successfully"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    delete_query = "DELETE FROM users WHERE id = %s"
    values = (user_id,)
    cursor.execute(delete_query, values)
    connection.commit()
    return {"message": "User deleted successfully"}

# Run the web scraper
scrape_website()

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
