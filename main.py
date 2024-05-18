from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)


# Check Login and Password true or wrong in Login Page
def check_login(username, password):
    try:
        df = pd.read_excel("UserLogin.xlsx", dtype={'Password': str})
        return ((df['User'] == username) & (df['Password'] == password)).any()
    except Exception as e:
        print("Error:", e)
        return False


# Check Invalid Email in SignUp page
def is_valid_email(email):
    if '@' not in email:
        return False
    username, domain = email.split('@', 1)
    if '.' not in domain:
        return False
    if not username or not domain.split('.')[0]:
        return False
    return True


# Create browser
@app.route('/')
def home():
    return redirect(url_for('signin'))


# Main Page
@app.route('/main_page')
def main_page():
    return render_template('MainPage.html')


# Login Page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_login(username, password):
            return redirect(url_for('main_page'))
        else:
            error = "Invalid username or password. Please try again!"
    return render_template('SignIn.html', error=error)


# SignUp page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if not is_valid_email(email):
            error = "Invalid email format. Please enter a valid email."
            return render_template('SignUp.html', error=error)

        try:
            df = pd.read_excel("UserLogin.xlsx", dtype={'Password': str})
        except Exception as e:
            error = f"Error reading the User file: {e}"
            return render_template('SignUp.html', error=error)

        # Check if the email or Username already exists
        if ((df['Email'].str.lower() == email.lower()).any() or
                (df['User'].str.lower() == username.lower()).any()):
            error = 'Email or Username already exists. Please try another one.'
            return render_template('SignUp.html', error=error)

        # Add new user if not exist
        new_user = pd.DataFrame(
            {'id': [df['id'].max() + 1], 'Email': [email], 'User': [username], 'Password': [password]})
        df = pd.concat([df, new_user], ignore_index=True)

        try:
            df.to_excel("UserLogin.xlsx", index=False)
        except Exception as e:
            error = f"Error saving the User file: {e}"
            return render_template('SignUp.html', error=error)

        return redirect(url_for('main_page'))
    return render_template('SignUp.html', error=error)


# Create module control url
if __name__ == '__main__':
    app.run(debug=True)
