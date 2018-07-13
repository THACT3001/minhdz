from threading import Thread
import cv2


class webcam:

    def __init__(self, name):
        self.cap = cv2.VideoCapture(0)
        self.currentframe = self.cap.read()
        self.name = name

    def getimagefromcam(self):
        while True:
            ret, self.currentframe = self.cap.read()
            cv2.imshow(str(self.name), self.currentframe)
            k = cv2.waitKey(30)
            if k == 27:
                cv2.imwrite("zed.jpg", self.currentframe)
                self.cap.release()
                break

    def update(self):
        Thread(None, self.getimagefromcam).start()

