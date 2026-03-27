from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="flaskuser",
    password="password123",
    database="blogDB"
)

"""
cursor() is a method (a function attached to a database connection object) that creates and returns a cursor object.
cursor = db.cursor() --> Hey database connection, give me a tool I can use to run queries and work with results.
"""
cursor = db.cursor()

# Home page
@app.route('/')
def index():
    return render_template('index.html')


# Handle form submission
@app.route('/add_blog', methods=['POST'])
def add_blog():
    username = request.form['username']
    email = request.form['email']
    title = request.form['title']
    content = request.form['content']

    # Insert user
    cursor.execute(
        "INSERT INTO users (username, email) VALUES (%s, %s)",
        (username, email)
    )
    db.commit()

    #Get the ID of the last row that was inserted into the database, and store it in user_id
    user_id = cursor.lastrowid

    # Insert blog
    cursor.execute(
        "INSERT INTO blog (user_id, title, content) VALUES (%s, %s, %s)",
        (user_id, title, content)
    )
    db.commit()

    return redirect('/blogs')


# Display blogs
@app.route('/blogs')
def blogs():
    # cursor.execute("SELECT blog.id, users.username, blog.title, blog.content, blog.created_at FROM blog JOIN users ON blog.user_id = users.userid")
    cursor.execute("""
    SELECT blog.id, users.username, blog.title, blog.content, blog.created_at
    FROM blog
    JOIN users ON blog.user_id = users.userid
    """)
    #Get all the rows returned by the last query and store them in data
    data = cursor.fetchall()

    return render_template('blogs.html', blogs=data)


# Run app
if __name__ == '__main__':
    app.run(debug=True)