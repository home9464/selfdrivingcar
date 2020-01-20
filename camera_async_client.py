import sys
import cv2
import asyncio

assert sys.version_info >= (3, 5, 2)

#FRAME_SEPARATOR = b'\xE2\x82\xAC\xE2\x82\xAC'
# (chr(255)+chr(0)+chr(0)+chr(0)+chr(255)+chr(0)+chr(0)+chr(0)+chr(255)).encode('utf-8')
FRAME_SEPARATOR = b'\xc3\xbf\x00\x00\x00\xc3\xbf\x00\x00\x00\xc3\xbf'


async def tcp_echo_client(server_ip='192.168.1.33', 
                          server_port=8888,
                          video_width=1280,
                          video_height=720,
                          video_color_gray=False):
    # connect to server
    reader, writer = await asyncio.open_connection(server_ip, server_port)
    # start camera
    cap = cv2.VideoCapture(0)
    cap.set(3, video_width)  # width
    cap.set(4, video_height)   # height
    while True:
        ret, frame = cap.read()
        if video_color_gray:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        encoded, buffer = cv2.imencode('.jpg', frame)
        data = buffer.tostring()  # class 'bytes'
        writer.write(data)
        writer.write(FRAME_SEPARATOR)
        await writer.drain()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print('Close the camera')
    cap.release()
    cv2.destroyAllWindows()
    print('Close the connection')
    writer.close()
    await writer.wait_closed()

if __name__ == '__main__':
    asyncio.run(tcp_echo_client())
