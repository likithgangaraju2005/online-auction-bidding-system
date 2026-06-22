from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "auction123"

try:
    db = mysql.connector.connect(
        host="localhost",
        user="auction",        # Change if needed
        password="auction123", # Change if needed
        database="auction_db"
    )

    cursor = db.cursor()
    print("Database Connected Successfully!")

except mysql.connector.Error as err:
    print("Database Connection Error:", err)
    exit()

@app.route('/')
def home():
    cursor.execute("""
        SELECT p.id,
               p.product_name,
               p.base_price,
               IFNULL(MAX(b.bid_amount),0)
        FROM products p
        LEFT JOIN bids b
        ON p.id = b.product_id
        GROUP BY p.id
    """)

    products = cursor.fetchall()

    return render_template("index.html", products=products)


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
            (name, email, password)
        )

        db.commit()

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cursor.fetchone()

        if user:
            session['user'] = user[1]
            return redirect('/')

        return "Invalid Login"

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():

    if request.method == 'POST':
        product = request.form['product']
        price = request.form['price']

        cursor.execute(
            "INSERT INTO products(product_name,base_price) VALUES(%s,%s)",
            (product, price)
        )

        db.commit()

        return redirect('/')

    return render_template('add_product.html')


@app.route('/bid/<int:id>', methods=['POST'])
def bid(id):

    amount = request.form['amount']

    cursor.execute(
        "INSERT INTO bids(product_id,bid_amount) VALUES(%s,%s)",
        (id, amount)
    )

    db.commit()

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)