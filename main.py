from flask import Flask, render_template, request, jsonify, Response
from flask_bootstrap import Bootstrap
import cv2
import socket
import numpy as np
import controller
ip = socket.gethostbyname(socket.gethostname())
print(ip)

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Initialize global variables
slider_value = 50
joystick_direction = 'Not Active'

# OpenCV VideoCapture object
video_capture = cv2.VideoCapture(0)  # Use the appropriate camera index (0 or 1) if you have multiple cameras
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

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
    print("Value 1")
    print(slider_value)
    controller.setspeed1(int(slider_value))
    return jsonify({'value': slider_value})


@app.route('/update_slider2', methods=['GET'])
def update_slider2():
    global slider_value
    new_value = int(request.args.get('value'))
    slider_value = new_value
    print(slider_value)
    print("Value 2")
    controller.setspeed2(int(slider_value))
    return jsonify({'value': slider_value})

@app.route('/update_slider3', methods=['GET'])
def update_slider3():
    global slider_value
    new_value = int(request.args.get('value'))
    slider_value = new_value
    print("Value 3")
    print(slider_value)
    controller.setspeed3(int(slider_value))
    return jsonify({'value': slider_value})
    

# Handle live data from the joystick
@app.route('/joystick_data', methods=['POST'])
def joystick_data():
    data = request.get_json()

    # Extract relevant information
    try:
        joystick_direction = data['direction']
        print(joystick_direction)
        if 'up' in joystick_direction:
            print("Left")
            controller.CarLeft()
        elif 'left' in joystick_direction:
            print("back")
            controller.CarBack()
        elif 'right' in joystick_direction:
            controller.CarForward()
            print("UP")
        elif 'down' in joystick_direction:
            controller.CarRight()
            print("right")


    except:print("Not Active")
    
    # Add your logic to handle joystick and slider data as needed

    return jsonify({'message': 'Data received successfully'})

def generate_frames():
    while True:
        _, frame = video_capture.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host=ip)
