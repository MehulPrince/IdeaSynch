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
    role = user[1]
    
    # Fetch student startups
    cur.execute("SELECT id, startup_name, description, funding_goal, current_funding, sector, founder_info FROM startups")
    startups = cur.fetchall()
    cur.close()
    
    if role == 'Founder':
        return render_template('founder_dashboard.html', user=user, startups=startups)
    else:
        return "Access Denied", 403


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/list_startup', methods=['POST'])
def list_startup():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    startup_name = request.form['startup_name']
    description = request.form['description']
    funding_goal = request.form['funding_goal']
    sector = request.form['sector']
    founder_info = request.form['founder_info']
    existing_funding = request.form.get('existing_funding', 0)

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO startups (startup_name, description, funding_goal, sector, founder_info, existing_funding, founder_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (startup_name, description, funding_goal, sector, founder_info, existing_funding, user_id)
    )
    conn.commit()
    cur.close()

    return redirect(url_for('dashboard'))

@app.route('/user')
def user():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    cur = conn.cursor()
    cur.execute("SELECT name, email, username FROM users WHERE id = %s", (user_id,))
    user_details = cur.fetchone()
    
    # Fetch existing startups by the user
    cur.execute("SELECT id, startup_name, description FROM startups WHERE founder_info = %s", (user_details[0],))
    startups = cur.fetchall()
    
    cur.close()
    return render_template('user.html', user=user_details, startups=startups)

@app.route('/list_company', methods=['POST'])
def list_company():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO startups (startup_name, description, sector, funding_goal, founder_info, education, current_funding) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (data['name'], data['description'], data['sector'], data['funding_required'], 
          data['founder_details'], data['education'], data['existing_funding']))
    
    conn.commit()
    cur.close()
    return jsonify({"message": "Company listed successfully"})



if __name__ == '__main__':
    app.run(debug=True)
