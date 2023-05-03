import cv2
import zmq
import imagezmq
import numpy as np


cap = cv2.VideoCapture(4)

#image_server = imagezmq.ImageHub()
#image_client = imagezmq.ImageSender('tcp://10.144.113.225:5555')
#image_client = imagezmq.ImageSender('tcp://10.144.113.199:5555')
#image_client = imagezmq.ImageSender('tcp://10.144.113.189:5555')
image_client = imagezmq.ImageSender('tcp://10.144.113.144:5555')


context = zmq.Context()
msg_server = context.socket(zmq.REQ)
msg_server.bind('tcp://*:5556')

numImages = 0


def sendVideo():
    global numImages
    
    numImages += 1
    
    msg_server.send(b'getVideo')
    message = msg_server.recv()
    print(message)
    
    ret, frame = cap.read()
    
    small_image = cv2.resize(frame, (384, 216)) # make image smaller if huge
    reply = image_client.send_image('Image: ' + str(numImages), small_image)
#    reply = image_client.send_image('Image: ' + str(numImages), frame)

    
    print(type(frame), np.size(frame), np.shape(frame))
    
    if message == "b'stopVid": 
        cap.release()
        cv2.destroyAllWindows()
        

#debug:
print("Server running...")

while True:
    sendVideo()