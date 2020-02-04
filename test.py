import time
import cv2
from servo import Servo
from gamepad import XboxController
def test_servo():
    print("Testing servo")
    s = Servo()
    s.angle(0, 90)
    time.sleep(2)
    s.angle(0, 0)
    time.sleep(2)
    s.angle(0, 180)
    time.sleep(2)
    s.angle(0, 90)
    time.sleep(2)
    s.angle(0, 180)
    time.sleep(2)

def test_onboard_cam():
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def test_controller():
    import asyncio
    async def main():
        controller = XboxController()
        try:
            await asyncio.gather(await controller.start())
        except Exception as e:
            print(e)
        finally:
            pass
    asyncio.run(main())

if __name__ == '__main__':
    #test_servo()
    test_controller()