from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection
conn = psycopg2.connect(
    dbname="IdeaSynch",
    user="postgres",
    password="Kallan",
    host="localhost"
)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[4], password):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            return "Invalid username or password", 401  # Error if login fails

    return render_template('login.html')  # Show login page

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        role = request.form['role']
        password = generate_password_hash(request.form['password'])

        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, username, role, password) VALUES (%s, %s, %s, %s, %s)",
            (name, email, username, role, password)
        )
        conn.commit()
        cur.close()

        return redirect(url_for('login'))  # Redirect to login after successful registration

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    cur = conn.cursor()
    cur.execute("SELECT name, role FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    
    # Fetch student startups (Example: Modify based on your DB)
    cur.execute("SELECT startup_name, description, funding_goal, current_funding, team_details, founder_info FROM startups")
    startups = cur.fetchall()
    cur.close()

    return render_template('dashboard.html', user=user, startups=startups)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
