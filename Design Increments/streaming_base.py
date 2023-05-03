import cv2
import zmq
import imagezmq


#image_client = imagezmq.ImageSender("tcp://10.144.113.199:5555")
#image_client = imagezmq.ImageSender('tcp://:5555')
image_server = imagezmq.ImageHub()

context = zmq.Context()
msg_client = context.socket(zmq.REP)
# msg_client.connect("tcp://10.144.113.199:5554")
msg_client.connect("tcp://10.144.113.225:5556")

stream = True

def getVideo():
    global stream

    if stream:
        msg_client.send(b'stream')
        ret, frame = image_server.recv_image()
        image_server.send_reply(b'OK')
        cv2.imshow('client-side stream of host', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stream = False

    else:
        msg_client.send(b'stopVid')
        ret, frame = image_server.recv_image()
        image_server.send_reply(b'stream suspended')
        cv2.destroyAllWindows()

        print("Press q, then enter, to restart stream:")
        if (input().lower() ==  'q'):
            stream = True

while True:
    print("Stream starting...")
    instruction = msg_client.recv()
    print(instruction)

    getVideo()

cv2.destroyAllWindows()