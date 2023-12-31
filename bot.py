from flask import Flask, render_template, request, jsonify, Response
from flask_bootstrap import Bootstrap
import socket
import numpy as np
import controller
try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except:camera_connected=False
import time
import os
from PIL import Image
os.system("hostname -I")
ip = socket.gethostbyname(socket.gethostname())
print(ip)

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Initialize global variables
slider_value = 50
joystick_direction = 'Not Active'
camera_connected = False
# Initialize Raspberry Pi camera
try:
    camera = PiCamera()
    camera.resolution = (640, 480)
    raw_capture = PiRGBArray(camera, size=(640, 480))
    camera_connected = True
except:camera_connected = False

# Allow the camera to warm up
time.sleep(0.1)
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
    
def generate_random_image():
    # Generate a random image using NumPy
    random_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    # Convert the NumPy array to a PIL Image
    pil_image = Image.fromarray(random_image)

    # Save the PIL Image to a BytesIO buffer
    image_buffer = io.BytesIO()
    pil_image.save(image_buffer, format='JPEG')

    return image_buffer.getvalue()
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


    except:
        controller.CarStop()
        print("Not Active")
    
    # Add your logic to handle joystick and slider data as needed

    return jsonify({'message': 'Data received successfully'})

def generate_frames():
    if camera_connected:
        for frame in camera.capture_continuous(raw_capture, format="jpeg", use_video_port=True):
            image = frame.array.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
            raw_capture.truncate(0)
    
    else:
        while True:
            # If the camera is not connected, generate a random image
            random_image_bytes = generate_random_image()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + random_image_bytes + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host=ip)

if __name__ == '__main__':
    app.run(debug=True, host=ip)
