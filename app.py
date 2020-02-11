from flask import Flask, render_template

# Specifying __name__ inside Flask creates an app that gets named after the name of this file which is app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', data=[{
        'description': 'Todo 1'
    },{
        'description': 'Todo 2'
    },{
        'description': 'Todo 3'
    }])
