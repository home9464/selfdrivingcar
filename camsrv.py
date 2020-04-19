"""capture and broadcast video (sending to a port)

if the ip is local, then it expose the video stream data to any consumers
if the ip is remote, then it send the video stream data to that remote consumer only

"""
import sys
import cv2
import time
import socket
import asyncio

import uvloop
assert sys.version_info >= (3, 5, 2)

#FRAME_SEPARATOR = b'\xE2\x82\xAC\xE2\x82\xAC'
# (chr(255)+chr(0)+chr(0)+chr(0)+chr(255)+chr(0)+chr(0)+chr(0)+chr(255)).encode('utf-8')
FRAME_SEPARATOR = b'\xc3\xbf\x00\x00\x00\xc3\xbf\x00\x00\x00\xc3\xbf'

FPS_RATE = 5 # frames per second

#video_width, video_height = 1280, 960
video_width, video_height = 640, 480
#video_width, video_height = 480, 320
#video_width, video_height = 320, 240

cap = cv2.VideoCapture(0)
cap.set(3, video_width)  # width
cap.set(4, video_height)  # height

def local_ip():
    ip_addr = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_addr = s.getsockname()[0]
        s.close()
    except:
        ip_addr = socket.gethostbyname(socket.gethostname())
    return ip_addr


async def camera_cb(reader, writer):
    """called whenever a new client connection is established
    """
    print('Connected')
    prev = time.time()
    try:
        while True:
            time_elapsed = time.time() - prev
            ret, frame = cap.read()
            if time_elapsed > 1./FPS_RATE:
                encoded, buffer = cv2.imencode('.jpg', frame)
                data = buffer.tostring()  # class 'bytes'
                writer.write(data)
                writer.write(FRAME_SEPARATOR)
                await writer.drain()
                #if cv2.waitKey(1) & 0xFF == ord('q'):
                #    break
                prev = time.time()
    except (asyncio.IncompleteReadError, ConnectionResetError, ConnectionAbortedError) as e:
        print('Disconnected:', e)
        writer.close()
        #await writer.wait_closed()

async def main2():
    ip_addr = local_ip()
    port = 8888
    server = await asyncio.start_server(camera_cb, host=ip_addr, port=port)
    print('Serving on {}:{}'.format(ip_addr, port))
    try:
        async with server:
            await server.serve_forever()
    except KeyboardInterrupt:
        server.close()
        await server.wait_closed()
    #await asyncio.sleep(600)
    #server.close()
    #await server.wait_closed()

async def broadcast(loop):
    ip_addr = local_ip()
    port = 8888
    server = await asyncio.start_server(camera_cb, host=ip_addr, port=port, loop=loop)
    print('Serving on {}:{}'.format(ip_addr, port))
    try:
        async with server:
            await server.serve_forever()
    except KeyboardInterrupt:
        server.close()
        await server.wait_closed()
    #await asyncio.sleep(600)
    #server.close()
    #await server.wait_closed()

if __name__ == '__main__':
    uvloop.install()
    asyncio.run(broadcast())