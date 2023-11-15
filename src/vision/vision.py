import cv2
import numpy as np
from cscore import CameraServer as CS


def start_camera():
    CS.enableLogging()
    usb_camera = CS.startAutomaticCapture()
    usb_camera.setResolution(320, 420)

    cv_sink = CS.getVideo()

    output_stream = CS.putVideo("Rectangle", 320, 420)

    img = np.zeros(shape=(420, 320, 3), dtype=np.uint8)

    while True:
        time, img = cv_sink.grabFrame(img)
        if time == 0:
            output_stream.notifyError(cv_sink.getError())
            continue
        cv2.rectangle(img, (100, 100), (300, 300), (255, 255, 255), 5)
        output_stream.putFrame(img)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)

    # You should uncomment these to connect to the RoboRIO
    # import ntcore
    # nt = ntcore.NetworkTableInstance.getDefault()
    # nt.setServerTeam(XXXX)
    # nt.startClient4(__file__)

    start_camera()
