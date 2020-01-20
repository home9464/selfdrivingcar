import asyncio

import cv2

class Camera:
    def __init__(self, width: int=320, height:int=240, frame_rate:int=10):
        self.frame_width = width
        self.frame_height = height
        self.frame_rate = frame_rate  # per second
        self.started = False
    
    async def onoff(self):
        """turn on / off camera
        """
        await self.start() if not self.started else self.close()

    async def start(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        self.started = True
        print('Camera started')
        """
        while True:
            ret, frame = self.cap.read()
            await asyncio.sleep(1 / self.frame_rate)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        """
    async def close(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.started = False
        print('Camera stopped')

#if __name__ == '__main__':
#    asyncio.run(Camera().start())