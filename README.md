# selfdrivingcar
a self driving car in indoor environment  trained by machine learning, using camera only

# 
Using XBox control to teach the car how to drive

## start the app on boot

we use systemd to start the app when the system boot

```bash
sudo cp car.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable drive.service
```
