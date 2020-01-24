import sys
import cv2
import asyncio

assert sys.version_info >= (3, 5, 2)

#FRAME_SEPARATOR = b'\xE2\x82\xAC\xE2\x82\xAC'
# (chr(255)+chr(0)+chr(0)+chr(0)+chr(255)+chr(0)+chr(0)+chr(0)+chr(255)).encode('utf-8')

class Camera:
    def __init__(self,
                 server_ip='192.168.1.33', 
                 server_port=8888,
                 video_width=1280,
                 video_height=720,
                 video_color_gray=False):
        self.server_ip = server_ip
        self.server_port = server_port
        self.video_width = video_width
        self.video_height = video_height
        self.video_color_gray = video_color_gray
        self.frame_separator = b'\xc3\xbf\x00\x00\x00\xc3\xbf\x00\x00\x00\xc3\xbf'
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.video_width)  # width
        self.cap.set(4, self.video_height)   # height
        # start camera
    
    async def start(self):
        # connect to server
        self.reader, self.writer = await asyncio.open_connection(self.server_ip, self.server_port)
        while True:
            ret, frame = self.cap.read()
            if self.video_color_gray:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            encoded, buffer = cv2.imencode('.jpg', frame)  # bool, numpy.ndarray 
            data = buffer.tostring()  # class 'bytes'
            self.writer.write(data)
            self.writer.write(self.frame_separator)
            await self.writer.drain()
            # read processed info from server
            #await asyncio.sleep(0)
            data = await self.reader.readline()
            print(data.decode())
            #cv2.waitKey(1)
        await self.close()

    async def close(self):
        print('Close the camera')
        self.cap.release()
        cv2.destroyAllWindows()
        print('Close the connection')
        self.writer.close()
        await self.writer.wait_closed()

#if __name__ == '__main__':
#    asyncio.run(client_camera())
