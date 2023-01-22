import datetime
import time
import DHT11
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    while True:
        return render_template("index.html", date_time = DHT11.DT, temperature = DHT11.T, humidity = DHT11.H)


#def read():
#    while True:
#        sensor_status = request.form['']
#        conditioner_status = request.form['']
#        optional_temperature = request.form['optional_temperature']

if __name__=="__main__":
    app.run(debug=True)