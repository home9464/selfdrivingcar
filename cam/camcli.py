import os
import sys
import multiprocessing
import random
import time
from datetime import datetime

assert sys.version_info >= (3, 5, 2), 'python version is too low. Must be > 3.5.2'  # for using asyncio

import asyncio
import uvloop

import cv2
import numpy as np



async def read_video_stream(image_queue, result_queue, server_ip='192.168.1.45', server_port=8888):
    draw_image = True
    print('connect to server')
    reader, writer = await asyncio.open_connection(server_ip, server_port, limit=1024*1024*8)  # 8MB buffer
    index = 0
    start = time.time()
    while True:
        img = None
        frame = await reader.readuntil(separator=FRAME_SEPARATOR)  # blocked until read something
        # truncate the separatorpyt
        frame = frame[:-FRAME_SEPARATOR_LEN]
        frame = np.asarray(bytearray(frame), dtype=np.uint8)
        img = cv2.imdecode(frame, -1)
        #img = cv2.flip(img, 0)
        if img is not None:
            while image_queue.full():
                image_queue.get()  # discard FIFO
            timestamp = time.time()
            image_queue.put((img, timestamp))
            index += 1
            if index % 100 == 0:
                print(index, '{:.2f} FPS'.format(index / (time.time() - start)))
            k = cv2.waitKey(1)
            if k % 256 == 27: # ESC pressed
                print("Escape hit, closing...")
                #image_queue.put(None)
                break
        # reponse to server
        #addr = writer.get_extra_info('peername')
        #data = str.encode("accepted"+'\n')
        #writer.write(data)
        #await writer.drain()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    num_cpus = multiprocessing.cpu_count()
    image_queue = multiprocessing.Queue(maxsize=num_cpus)
    result_queue = multiprocessing.Queue(maxsize=num_cpus)
    multiprocessing.Pool(2, authenticate, (image_queue, result_queue, ))
    server_ip = '192.168.1.45'
    server_port = 8888
    # final result rendering process
    p = multiprocessing.Process(target=execute_action, args=(result_queue, ))
    p.start()
    uvloop.install()
    asyncio.run(read_video_stream(image_queue, result_queue, server_ip, server_port))
    p.join()
