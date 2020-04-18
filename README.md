# self driving car

Image recognition with Machine Learning, uses an onboard cam on a RC car.
At now it seems the Raspberry Pi 4 is not powerful enough to recognize faces with decent performance (like FPS>20 with 320*240 image size).
Some works used a google coral TPU USB stick to accelerate the inference to reach high FPS, however I want to explore the possibilities from algorithm improvement. 

```bash
sudo apt-get install -y libqt4-test libatlas-base-dev libjasper-dev libqtgui4 python3-pyqt5
sudo pip3 install opencv-python==3.4.6.27 adafruit-circuitpython-servokit evdev quart adafruit_servokit
sudo pip3 install tensorflow-1.14.0-cp37-cp37m-linux_armv7l.whl
sudo pip3 install https://github.com/PINTO0309/Tensorflow-bin/blob/master/tensorflow-2.0.0-cp37-cp37m-linux_armv7l.whl
```

## Auto start the app on booting

Use systemd to start the app when the system (Rasbian) booting

```bash
sudo cp drive.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable drive
sudo systemctl start drive
sudo systemctl status drive

# optional
sudo systemctl stop drive
sudo systemctl disable drive
```
## 
