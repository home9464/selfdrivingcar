"""
Python>3.5.2
"""
import sys
import socket
import asyncio
import numpy as np
import cv2


assert sys.version_info >= (3, 5, 2)  # for reader.readuntil

#FRAME_SEPARATOR = b'\xE2\x82\xAC\xE2\x82\xAC'
# (chr(255)+chr(0)+chr(0)+chr(0)+chr(255)+chr(0)+chr(0)+chr(0)+chr(255)).encode('utf-8')
FRAME_SEPARATOR = b'\xc3\xbf\x00\x00\x00\xc3\xbf\x00\x00\x00\xc3\xbf'
LOCAL_IP = socket.gethostbyname(socket.gethostname())
LOCAL_PORT = 8888


async def _handle_cam(reader, writer):
    sep_len = len(FRAME_SEPARATOR)
    while True:
        img = None
        frame = await reader.readuntil(separator=FRAME_SEPARATOR)  # blocked until read something
        # truncate the separator
        frame = frame[:-sep_len]
        frame = np.asarray(bytearray(frame), dtype=np.uint8)
        img = cv2.imdecode(frame, -1)
        if img is not None:
            cv2.imshow('jpg', img)
            cv2.waitKey(1)
        await asyncio.sleep(0)


async def camera_cb(reader, writer):
    """called whenever a new client connection is established
    """
    try:
        await _handle_cam(reader, writer)
    except asyncio.IncompleteReadError:
        print('Client failed')
        cv2.destroyAllWindows()


async def main():
    server = await asyncio.start_server(camera_cb,
                                        LOCAL_IP,
                                        LOCAL_PORT,
                                        limit=1024*1204*8)
    print('Serving on {}:{}'.format(LOCAL_IP, LOCAL_PORT))
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
