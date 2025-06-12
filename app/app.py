from flask import Flask, jsonify, render_template

app = Flask(__name__)

fake_weather_data = [
    {"city": "Sunnyvale", "weather": "Sunny", "temp_c": 25},
    {"city": "Cloudsville", "weather": "Cloudy", "temp_c": 18},
    {"city": "Rainytown", "weather": "Raining", "temp_c": 15}
]

@app.route('/api/weather', methods=['GET'])
def get_weather():
    return jsonify(fake_weather_data)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# For AWS Lambda
try:
    import serverless_wsgi
    def lambda_handler(event, context):
        return serverless_wsgi.handle_request(app, event, context)
except ImportError:
    pass # Allow local execution if serverless_wsgi is not installed

if __name__ == '__main__':
    app.run(debug=True)
