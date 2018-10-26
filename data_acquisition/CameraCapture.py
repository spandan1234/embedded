import cv2
from data_acquisition.logger import logger_variable
import numpy as np
from os import path


class CameraCapture:
    def __init__(self):
        # initialize logger variable
        self.logger = logger_variable(__name__, 'Log_files\\CameraCapture.log')

        # initialize VideoCapture variable
        self.cap = cv2.VideoCapture(-1)
        self.logger.debug('VideoCapture is initialized')

        # initialize Frame height & width
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.logger.debug('Frame dimension is initialized')

    def capture_image(self, frame_no):
        """
        :param: frame_no - the current frame number to be integrated into the image name
        :return: image data
        """
        img = np.zeros((720, 1280, 3), np.uint8)

        # check if the VideoCapture is open
        if self.cap.isOpened():
            # capture Image
            ret, img = self.cap.read()
            self.logger.debug('Image Captured')
            # check if the image capture returned True or False
            if ret is True:
                cv2.imwrite('Images\\live_capture{}.jpg'.format(frame_no))
            else:
                self.logger.error('Image capture problem')
        else:
            self.logger.error('Problem opening Camera port')
        # check if imwrite created the image file
        if path.isfile('Images\\live_capture.jpg'):
            self.logger.debug('Image Capture successful')

        # open the image
        data = open('Images\\live_capture{}.jpg'.format(frame_no), 'rb')

        # opencv mandatory waitKey function
        c = cv2.waitKey(1)
        if c == 27:
            self.cap.release()
            cv2.destroyAllWindows()
        return data
