from flask import Flask, send_file
from flask_socketio import SocketIO, emit, send
from PIL import Image
import numpy as np
import io
import random
import threading


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

raw_data = [[[random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)]
                 for x in range(3)] for y in range(3)]

def update_image():
    new_colour = int(input('new_colour: '))
    print(' +++ UPDATING_IMAGE +++ ')
    raw_data = [[[new_colour, new_colour, new_colour]
                 for x in range(3)] for y in range(3)]
    emit('new_image')

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    emit('my response', json)


@app.route('/image.png')
def image():
    print('image.png requested')

    # my numpy array 
    arr = np.array(raw_data)

    # convert numpy array to PIL Image
    img = Image.fromarray(arr.astype('uint8'))

    # create file-object in memory
    file_object = io.BytesIO()

    # write PNG in file-object
    img.save(file_object, 'PNG')

    # move to beginning of file so `send_file()` it will read from start    
    file_object.seek(0)

    return send_file(file_object, mimetype='image/PNG')


@app.route('/')
def home():
    raw_data = [[[random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)]
                 for x in range(3)] for y in range(3)]
    return """
    <h1>MOCK SHEPHERD</h1>
    <script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js" integrity="sha256-yr4fRk/GU1ehYJPAs8P4JlTgu0Hdsp4ZKrx8bDEDC3I=" crossorigin="anonymous"></script>
    <img id="myImg" src="http://localhost:8080/image.png" width=100% height=50%/>
    <script type="text/javascript" charset="utf-8">
        var socket = io();
        i = 0;
        socket.on('connect', function() {
            socket.on('new_image', function(msg){
                i++;    
                document.getElementById("myImg").src = "/image.png?" + String(i);
            });
        });

        
    </script>
    """

if __name__ == "__main__":
    thread = threading.Thread(target=update_image)
    thread.start()
    app.run(debug=True, port=8080)
