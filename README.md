# selfdrivingcar

Image recognition with Machine Learning, uses an onboard cam on a RC car 

```bash
sudo apt-get install -y libqt4-test libatlas-base-dev libjasper-dev libqtgui4 python3-pyqt5
sudo pip3 install opencv-python==3.4.6.27 adafruit-circuitpython-servokit evdev
sudo pip3 install tensorflow-1.14.0-cp37-cp37m-linux_armv7l.whl
```

# 
Using XBox control to teach the car how to drive

## start the app on boot

we use systemd to start the app when the system boot

to star the service, we must install following python libs as 'sudo pip3 install'

- adafruit-circuitpython-servokit
- opencv-python
- evdev


```bash
sudo cp drive.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable drive
```
