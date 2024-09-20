from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__,template_folder='templates')
app.secret_key = "your_secret_key"  # Needed for flash messages

# Function to establish a connection with MySQL
    
def connect_db():
    return mysql.connector.connect(
        host="localhost", 
        user="root", 
        passwd="shre1234", 
        db="inventory_db"
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO items (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
        db.commit()
        db.close()

        return redirect(url_for('home'))
    return render_template('add_entry.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit_entry():
    if request.method == 'POST':
        entry_id = request.form['id']
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("UPDATE items SET name=%s, quantity=%s, price=%s WHERE id=%s", (name, quantity, price, entry_id))
        db.commit()
        db.close()

        return redirect(url_for('home'))
    return render_template('edit_entry.html')

# Search entry
@app.route('/search', methods=['GET', 'POST'])
def search_entry():
    if request.method == 'POST':
        search_name = request.form['name']

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM items WHERE name=%s", [search_name])
        result = cursor.fetchall()
        db.close()

        return render_template('result.html', result=result)
    return render_template('search_entry.html')

if __name__ == '__main__':
    app.run(debug=True)
