import asyncio
import os
import json
from BarcodeScanner import BarcodeScanner
from MQTTClient import mqtt_client
import signal

async def ask_exit():
    print("Got exit signal")
    await asyncio.sleep(1)
    loop.stop()

async def run(loop,cfg):
    loop.add_signal_handler(signal.SIGTERM,lambda: asyncio.create_task(ask_exit()))
    
    q_in = asyncio.Queue()
    q_out = asyncio.Queue()
    bs = BarcodeScanner.BarcodeScanner(cfg['barcode_scanner'],cfg['service'])
    t1 = asyncio.create_task(bs.scan_loop(q_out,q_in))

    ps_task = mqtt_client.AsyncMqttLoop(loop,q_out,q_in,cfg['mqtt_client'])
    t2 = asyncio.create_task(ps_task.run())
    await asyncio.gather(t1,t2)


def main():
    this_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = os.getenv("app_config",'config.json')
    print("Using config file ",config_file)
    with open(os.path.join(this_dir,config_file)) as json_file:
        cfg = json.load(json_file)
    
    loop=asyncio.get_event_loop()
    loop.run_until_complete(run(loop,cfg))

if __name__ == "__main__":
    main()
