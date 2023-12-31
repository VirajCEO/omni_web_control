from flask import Flask, render_template, request, jsonify,Response
from flask_bootstrap import Bootstrap
import socket
import camera as Camera
ip = socket.gethostbyname(socket.gethostname())
print(ip)
app = Flask(__name__)
bootstrap = Bootstrap(app)

# Initialize global variables
slider_value = 50
joystick_direction = 'Not Active'

# Define routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run_function_two')
def run_function_two():
    result = "Function Two Executed"
    return result

@app.route('/update_slider', methods=['GET'])
def update_slider():
    global slider_value
    new_value = int(request.args.get('value'))
    slider_value = new_value
    print(slider_value)
    return jsonify({'value': slider_value})

# Handle live data from the joystick
@app.route('/joystick_data', methods=['POST'])
def joystick_data():
    data = request.get_json()

    # Extract relevant information
    joystick_direction = data['direction']
    print(joystick_direction)
    # Add your logic to handle joystick and slider data as needed

    return jsonify({'message': 'Data received successfully'})


def generate_frames():
    camera = Camera()
    while True:
        time.sleep(0.1)  # Adjust sleep time if needed
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(debug=True, host=ip)