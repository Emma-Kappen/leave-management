from flask import Flask, render_template, send_from_directory
from backend.app import create_app
import os

app = create_app()

@app.route('/')
def index():
    return render_template('login/index.html')

if __name__ == '__main__':
    app.run(debug=True)