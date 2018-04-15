import time
import cv2
import serial
import os

ser = serial.Serial("/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_DA00UH3T-if00-port0", 9600)
temp = 0

while 1:
    print("taking picture...")
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    time.sleep(0.05)  # If you don't wait, the image will be dark
    
    return_value, image = camera.read()
    cv2.imwrite("opencv.png", image)
    print("picture taken...")
    
    del(camera)  # so that others can use the camera as soon as possible

    print("uploading picture...")
    os.system("scp -i CrimsonHacks18.pem opencv.png ubuntu@18.219.98.0:/home/ubuntu/Pictures")

    print("checking if home...")
    for x in range(ser.in_waiting):
        temp = ser.read()
        print(temp)
    if temp is '1':
        print("owner is NOT home. Updating server...")
        os.system("ssh -i CrimsonHacks18.pem ubuntu@18.219.98.0 'touch /home/ubuntu/Pictures/vacant.txt'")
    elif temp is '0':
        print("owner is home. Updating server...")
        os.system("ssh -i CrimsonHacks18.pem ubuntu@18.219.98.0 'rm -r /home/ubuntu/Pictures/vacant.txt'")
    print("checking for object and notifying owner")
    os.system("ssh -i CrimsonHacks18.pem ubuntu@18.219.98.0 'cd /home/ubuntu/Pictures && python object-detect.py'")

    time.sleep(5)
