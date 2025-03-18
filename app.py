from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Keep this secure

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname="IdeaSynch",
        user="postgres",
        password="Kallan",
        host="localhost"
    )

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if not user:
            print(f"Login failed: No user found for username '{username}'")  # Debugging
            return jsonify({"error": "Invalid username or password"}), 401

        stored_hash = user[4]  # Assuming password is stored in the 5th column

        print(f"Stored Hash: {stored_hash}")  # Debugging
        print(f"Entered Password: {password}")  # Debugging

        if check_password_hash(stored_hash, password):
            session['user_id'] = user[0]
            print(f"Login successful for user: {username}")  # Debugging
            return jsonify({"redirect": url_for('dashboard')})
        else:
            print(f"Password mismatch for user: {username}")  # Debugging
            return jsonify({"error": "Invalid username or password"}), 401

    return render_template('login.html')




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')  
        email = request.form.get('email')  
        username = request.form.get('username')  
        role = request.form.get('role')  
        password = request.form.get('password')  

        if not (name and email and username and role and password):
            return jsonify({"error": "All fields are required"}), 400

        hashed_password = generate_password_hash(password)  # Hash the password

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (name, email, username, role, password) VALUES (%s, %s, %s, %s, %s)",
                (name, email, username, role, hashed_password)
            )
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            return jsonify({"error": str(e)}), 500  # Return error if DB insert fails

        return redirect(url_for('login'))  # ✅ Redirect to login page instead of dashboard

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        print("❌ Debug: User not in session")
        return redirect(url_for('login'))

    user_id = session['user_id']
    print(f"🔍 Debug: Logged-in User ID: {user_id}")

    conn = get_db_connection()
    cur = conn.cursor()
    
    # Fetch user details
    cur.execute("SELECT name, role FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    
    if not user:
        print("❌ Debug: User not found in database")
        cur.close()
        conn.close()
        return redirect(url_for("login"))

    role = user[1]
    print(f"✅ Debug: User Found - Name: {user[0]}, Role: {role}")

    # Fetch startups data
    cur.execute("SELECT id, startup_name, description, funding_goal, COALESCE(current_funding, 0), sector, founder_info FROM startups")
    startups = cur.fetchall()

    cur.close()
    conn.close()

    print(f"📊 Debug: {len(startups)} startups found")

    if role == 'Founder':
        return render_template('founder_dashboard.html', user=user, startups=startups)
    else:
        print("❌ Debug: Access Denied (User is not a Founder)")
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

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO startups (startup_name, description, funding_goal, sector, founder_info, existing_funding, founder_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (startup_name, description, funding_goal, sector, founder_info, existing_funding, user_id)
    )
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/user')
def user():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, email, username FROM users WHERE id = %s", (user_id,))
    user_details = cur.fetchone()

    if not user_details:
        cur.close()
        conn.close()
        return redirect(url_for("login"))

    # Fetch startups owned by the user
    cur.execute("SELECT id, startup_name, description FROM startups WHERE founder_info = %s", (user_details[0],))
    startups = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('user.html', user=user_details, startups=startups)

@app.route('/list_company', methods=['POST'])
def list_company():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO startups (startup_name, description, sector, funding_goal, founder_info, education, current_funding) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (data['name'], data['description'], data['sector'], data['funding_required'], 
          data['founder_details'], data['education'], data['existing_funding']))
    
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Company listed successfully"})

if __name__ == '__main__':
    app.run(debug=True)
