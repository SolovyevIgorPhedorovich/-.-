import time
import DHT11
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html", date_time = DHT11.DT, temperature = DHT11.T, humidity = DHT11.H)


def read():
    sensor_status = request.form['sensor_status']
    conditioner_status = request.form['conditioner_status']
    optional_temperature = request.form['optional_temperature']

app.run(debug=True)
