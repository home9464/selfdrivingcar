import asyncio

import cv2

class Camera:
    def __init__(self, width: int=320, height:int=240, frame_rate:int=10):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.frame_rate = frame_rate
        
    async def start(self):
        while True:
            ret, frame = self.cap.read()
            await asyncio.sleep(1 / self.frame_rate)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()
