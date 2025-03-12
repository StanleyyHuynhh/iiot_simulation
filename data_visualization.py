import threading
import time
import json
import random
from datetime import datetime

import paho.mqtt.client as mqtt
import pandas as pd
import matplotlib.pyplot as plt

# aiocoap and asyncua are async libraries
import asyncio
from aiocoap import Context, Message, GET
from asyncua import Client

# ------------------------------------------------------------------------------
# 1. Global Data Structure
#    We'll store all incoming data here: a list of dicts with fields:
#    {"timestamp": ..., "temperature": ..., "humidity": ..., "source": ...}
# ------------------------------------------------------------------------------
data = []

# A simple lock to prevent race conditions when multiple threads modify 'data'
from threading import Lock
data_lock = Lock()

# ------------------------------------------------------------------------------
# 2. MQTT Setup (Background Thread)
# ------------------------------------------------------------------------------
def on_mqtt_message(client, userdata, message):
    """Handle incoming MQTT messages."""
    try:
        payload = message.payload.decode("utf-8")
        sensor_data = json.loads(payload)  # safer than eval
        with data_lock:
            data.append({
                "timestamp": datetime.now(),
                "temperature": sensor_data["temperature"],
                "humidity": sensor_data["humidity"],
                "source": "MQTT"
            })
    except Exception as e:
        print("MQTT parse error:", e)

def mqtt_thread():
    """Runs in a background thread, connects to the MQTT broker, and subscribes."""
    client = mqtt.Client()
    client.on_message = on_mqtt_message
    client.connect("localhost", 1883)
    client.subscribe("sensor/data")
    client.loop_forever()  # Blocking call, runs until script ends

# ------------------------------------------------------------------------------
# 3. CoAP Setup (Background Thread)
#    We will poll the CoAP server by sending GET requests periodically.
# ------------------------------------------------------------------------------
async def coap_polling():
    """Async function to periodically get data from CoAP server."""
    protocol = await Context.create_client_context()
    while True:
        try:
            # Adjust the URI as needed (some servers might need a POST or a different path)
            request = Message(code=GET, uri="coap://localhost/sensor/data")
            response = await protocol.request(request).response
            # The server might return JSON data or something else
            # Example: {"temperature": 23.4, "humidity": 45.6}
            sensor_data = json.loads(response.payload.decode("utf-8"))
            with data_lock:
                data.append({
                    "timestamp": datetime.now(),
                    "temperature": sensor_data["temperature"],
                    "humidity": sensor_data["humidity"],
                    "source": "CoAP"
                })
        except Exception as e:
            print("CoAP error:", e)
        await asyncio.sleep(1)  # Poll every 1 second

def coap_thread():
    """Wrapper to run the coap_polling coroutine in a separate thread."""
    asyncio.run(coap_polling())

# ------------------------------------------------------------------------------
# 4. OPC UA Setup (Background Thread)
#    We will poll an OPC UA server by reading node values periodically.
# ------------------------------------------------------------------------------
async def opcua_polling():
    """Async function to periodically read data from OPC UA server."""
    url = "opc.tcp://localhost:4840/freeopcua/server/"
    async with Client(url=url) as client:
        # Adjust node IDs as needed; these are from your simulation
        temperature_node = client.get_node("ns=2;i=2")  # Example node ID
        humidity_node = client.get_node("ns=2;i=3")     # Example node ID
        while True:
            try:
                temp_value = await temperature_node.read_value()
                hum_value = await humidity_node.read_value()
                with data_lock:
                    data.append({
                        "timestamp": datetime.now(),
                        "temperature": temp_value,
                        "humidity": hum_value,
                        "source": "OPC UA"
                    })
            except Exception as e:
                print("OPC UA error:", e)
            await asyncio.sleep(1)  # Poll every 1 second

def opcua_thread():
    """Wrapper to run the opcua_polling coroutine in a separate thread."""
    asyncio.run(opcua_polling())

# ------------------------------------------------------------------------------
# 5. Main Thread: Matplotlib Visualization
#    We'll run our data plotting in the main thread so that Tkinter/Matplotlib
#    doesn't conflict with background threads.
# ------------------------------------------------------------------------------
def main():
    # Start background threads for MQTT, CoAP, and OPC UA
    t_mqtt = threading.Thread(target=mqtt_thread, daemon=True)
    t_coap = threading.Thread(target=coap_thread, daemon=True)
    t_opcua = threading.Thread(target=opcua_thread, daemon=True)
    
    t_mqtt.start()
    t_coap.start()
    t_opcua.start()

    # Set up Matplotlib in interactive mode
    plt.ion()
    fig, ax = plt.subplots()

    while True:
        time.sleep(1)  # Update the plot every second

        # Copy data under lock to avoid concurrency issues
        with data_lock:
            if not data:
                continue
            # Convert the data list to a DataFrame
            df = pd.DataFrame(data)

        # We'll create separate lines for each source
        # (MQTT, CoAP, OPC UA) so we can compare them on one plot.
        ax.clear()
        for source in df["source"].unique():
            subset = df[df["source"] == source]
            ax.plot(subset["timestamp"], subset["temperature"], label=f"{source} Temp")
            ax.plot(subset["timestamp"], subset["humidity"], label=f"{source} Hum")
        
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.set_title("Combined Sensor Data (MQTT, CoAP, OPC UA)")
        ax.legend()
        plt.pause(0.01)  # Allow the GUI to update

if __name__ == "__main__":
    main()
