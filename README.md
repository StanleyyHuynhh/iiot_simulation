# iiot_simulation

# README

## Overview
This repository demonstrates a simple **Industrial IoT (IIoT) simulation** using three different communication protocols: **MQTT**, **CoAP**, and **OPC UA**. The goal is to simulate sensor data (temperature and humidity), publish that data using each protocol, and then visualize it in real time. We also provide a combined visualization that shows all three protocols’ data on a single plot.

## Repository Structure

```
iiot_simulation/
├── README.md
├── mqtt_sensor_simulation.py
├── coap_sensor_simulation.py
├── opcua_sensor_simulation.py
├── data_visualization_mqtt.py
├── data_visualization_coap.py
├── data_visualization_opcua.py
├── combined_visualization.py
├── visualizations/
│   ├── mqtt_visualization.png
│   ├── coap_visualization.png
│   ├── opcua_visualization.png
│   └── combined_visualization.png
└── comparison_report.pdf
```

- **`mqtt_sensor_simulation.py`**  
  Simulates a sensor that publishes random temperature and humidity data over MQTT.

- **`coap_sensor_simulation.py`**  
  Simulates a sensor that sends random temperature and humidity data to a CoAP server endpoint.

- **`opcua_sensor_simulation.py`**  
  Simulates a sensor using an OPC UA server that updates temperature and humidity nodes.

- **`data_visualization_mqtt.py`**  
  Subscribes to the MQTT topic, receives data, and plots temperature/humidity in real time.

- **`data_visualization_coap.py`**  
  (Example) Would act as a CoAP client or server-side logger that collects data and plots temperature/humidity.

- **`data_visualization_opcua.py`**  
  (Example) Connects to the OPC UA server, reads temperature/humidity, and plots in real time.

- **`combined_visualization.py`**  
  Combines data from all three protocols into a single chart, showing temperature and humidity lines for MQTT, CoAP, and OPC UA together.

- **`visualizations/`**  
  Folder containing saved plot images (e.g., `mqtt_visualization.png`, `coap_visualization.png`, `opcua_visualization.png`, and `combined_visualization.png`).

- **`comparison_report.pdf`**  
  A report comparing the three protocols (MQTT, CoAP, and OPC UA).

## Requirements
- Python 3.9+ (or compatible)
- `paho-mqtt` (for MQTT)
- `aiocoap` (for CoAP)
- `asyncua` (for OPC UA)
- `pandas`
- `numpy`
- `matplotlib`

You can install the dependencies using:
```bash
pip install -r requirements.txt
```
*(If you create a `requirements.txt` file with all your dependencies.)*

## Setup & Usage

1. **Install Mosquitto (MQTT Broker)**  
   - [Mosquitto Installation](https://mosquitto.org/download/)  
   - Start Mosquitto on port 1883 (default).

2. **Run the MQTT Sensor Simulation**  
   ```bash
   python mqtt_sensor_simulation.py
   ```
   This publishes random sensor data to the topic `sensor/data`.

3. **Run the CoAP Sensor Simulation**  
   ```bash
   python coap_sensor_simulation.py
   ```
   This sends random sensor data via CoAP to a local server endpoint.

4. **Run the OPC UA Sensor Simulation**  
   ```bash
   python opcua_sensor_simulation.py
   ```
   This hosts an OPC UA server that updates temperature/humidity nodes with random values.

5. **Run the Visualization Scripts**  
   - For MQTT:  
     ```bash
     python data_visualization_mqtt.py
     ```  
   - For CoAP:  
     ```bash
     python data_visualization_coap.py
     ```  
   - For OPC UA:  
     ```bash
     python data_visualization_opcua.py
     ```  
   - For Combined Visualization:  
     ```bash
     python combined_visualization.py
     ```

6. **Observe the Plots**  
   You should see a real-time graph of temperature and humidity. Each script may open its own plotting window.

## Notes
- This project is intended as a demonstration of how to integrate multiple IIoT protocols rather than a production-ready solution.
- Feel free to modify the random data generation to use actual sensor inputs if you have real hardware.
