# EvTrain 
A project based on OverflowTrainV2 (https://github.com/np-overflow/OverflowTrainV2), it uses Computer Vision(CV) to allow people to select where an Ev3 robot goes to on a map. 

CV is carried out by using Object Detection to detect the number of humans in each side of the frame. 

To allow the computer running CV to let the Ev3 robot know the selected location, a MQTT broker is ran on the computer, where the selected destination is sent to a topic and the Ev3 robot receives the destination published to the topic.

![overview of process](/overview.jpg)

## Set-up guide
### 1. Computer
1. Install the MQTT broker ([Downloads](https://mosquitto.org/download/))
2. Configure the broker to be accessible within the local network, add the following lines to **mosquitto.conf**
```  
listener 1883 0.0.0.0 
allow_anonymous true
```
3. Open up a terminal and run mosquitto with the **mosquitto.conf** file
``` bash
# MacOS
/usr/local/opt/mosquitto/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf
```
4. Clone this repository and go to the backend directory in a terminal
``` bash
# MacOS 
git clone <https_clone_of_repository>
cd EvTrain
cd backend
```
5. (Optional) Create a virtual environment 
``` bash
# MacOS
python -m venv venv
source venv/bin/activate
```
6. Install the modules in requirements.txt
``` bash
# MacOS 
pip install -r requirements.txt
```
7. (Optional) If you are running the broker on a seperate computer on the network, open the destination.py file and edit the HOST variable to the IP of the computer running the broker.
8. Run destination.py
``` bash
# MacOS
python destination.py
```

### 2. Ev3
1. Install **ev3dev** ([Getting Started](https://www.ev3dev.org/docs/getting-started/)) on a micro sd card, follow the guide till 'Step 4: Boot ev3dev'
2. Plug in a Wifi dongle into the USB slot (request from school if neccessary)
3. Follow the guide on networking 'With a Wi-Fi dongle' ([Networking Guide](https://www.ev3dev.org/docs/networking/))
4. When the Ev3 has joined the network, ssh into the Ev3 ([Connecting to Ev3 Using SSH](https://www.ev3dev.org/docs/tutorials/connecting-to-ev3dev-with-ssh/))
5. When you have successfully ssh'ed into the Ev3, install pip
``` bash
wget https://bootstrap.pypa.io/pip/3.5/get-pip.py
python get-pip.py
```
6. Install Ev3Dev Browser in VSCode ([ev3dev-browser](https://marketplace.visualstudio.com/items?itemName=ev3dev.ev3dev-browser))
7. Open up a new terminal and go to the ev3 directory
``` bash 
cd EvTrain
cd ev3
code . # Open up VSCode in this directory
```
8. Open up the 'EV3DEV DEVICE BROWSER' tab in VSCode and connect to the Ev3
9. Transfer the workspace into the Ev3
10. Using the Ev3, navigate to the ev3 folder and select **main.py**, make sure that the broker is running. 
11. When the Ev3 *beeps* run destination.py on the computer and off you go!