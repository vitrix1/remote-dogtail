# Remote dogtail server
The server allows you to run [dogtail](https://gitlab.com/dogtail/dogtail) on a remote machine and returns an Atspi object, similar to a local launch. This allows you to interact with the remote application as with a native one.
## Important notes
The server runs in an environment with a graphical user interface (GUI). The client must also be running a Linux OS with a GUI for proper processing and interaction with the Atspi object.  
## Before Running the Server
1. Install the required libraries (example for Debian-based systems):
```bash
sudo apt update
sudo apt install -y python3-venv git build-essential pkg-config libcairo2-dev python3-dev libgirepository1.0-dev python3-pyatspi at-spi2-core 
```
2. Clone `pyatspi` repository
```bash
cd ~ && git clone https://gitlab.gnome.org/GNOME/pyatspi2.git 
```
3. Check your at-spi2-core version:
```bash
sudo apt-cache policy at-spi2-core 
```
4. If necessary, switch the pyatspi repository to the corresponding version of at-spi2-core (e.g., version 2.46.1):
```bash
cd pyatspi
git checkout PYATSPI_2_46_1
```
Available tags can be found at: [pyatspi2 history](https://gitlab.gnome.org/GNOME/pyatspi2/-/commits/master/?ref_type=HEADS)  
5. Copy the `pyatspi` module to Python's library directory:
```bash
sudo cp -r ~/pyatspi2/pyatspi /usr/lib/python3/dist-packages/
```
6. Enable desktop interaction:
```bash
gsettings set org.gnome.desktop.interface toolkit-accessibility true 
```
7. Make the launch file executable:
```bash
chmod +x start_dogtail_server
```

## Running the Server
To start the server, use the following command:
```bash
./start_dogtail_server 4723
```
Where `4723` is the port on which the server will listen. The default port is `8080`.

## Client side
To use the service from a remote client, you need to connect to the server via RPyC and call the Dogtail startup method.     
Example:
```python
import rpyc

conn = rpyc.connect("10.10.10.10", 4723)

opts = {
    'app_path': '/path/to/application',
    'app_name': 'ApplicationName',
    'timeout': 30,
    'dumb': False
}

driver = conn.root.remote(opts, debug=True)
```

The `driver` will represent an absolutely identical Atspi object that is running on the remote machine.
