import sqlite3

# Connect to the SQLite database (create it if it doesn't exist)
conn = sqlite3.connect('database.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Sample data to insert into the table
products = [
    ('Laptop', './static/laptop.jpg', 40000, 'Laptop with 8GB Ram/500 GB SSD'),
    ('Smart Watch', './static/smart_watch.jpg', 1500,'Smart watch with health tracker'),
    ('Headsets', './static/headsets.jpg', 1000, 'Wireless Bluetooth headsets'),
	('Mobile', './static/mobile.jpg', 20000, 'Andriod OS mobile'),
	('iPad', './static/ipad.jpg', 35000, 'iPad Mini with latest iOs')
]

# Define the SQL query to insert records into the table
insert_query = '''
INSERT INTO product (name, url, price, description)
VALUES (?, ?, ?, ?)
'''

# Execute the query to insert records
cursor.executemany(insert_query, products)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
