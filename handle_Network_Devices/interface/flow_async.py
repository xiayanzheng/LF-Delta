import asyncio
import netdev
from common.data_hub import NdcHub
from handle_Network_Devices.nd_data_processor.pipeline import PackDeviceData


async def task(cfg):
    print("Connecting to {}".format(cfg["host"]))
    connect_param = {
        "username": cfg["username"],
        "password": cfg["password"],
        "device_type": cfg["device_type"],
        "secret": cfg["enablepass"],
        "host": cfg["host"]
    }
    async with netdev.create(**connect_param) as ios:
        # Testing sending simple command
        task_list = cfg['tasks']
        cfg["hostname"] = cfg["desc"]
        dc = PackDeviceData()
        for task_i in task_list:
            for cmd_name in NdcHub.tasks[task_i]['commands']:
                cmd_cfg = NdcHub.commands[cmd_name]
                real_cmd = cmd_cfg['cmd']
                data = await ios.send_command(real_cmd)
                dc.pipeline_flow(cmd_name, cmd_cfg, data, **cfg)
        dc.export_data_to_csv()


async def run(devices):
    tasks = [task(dev) for dev in devices]
    await asyncio.wait(tasks)
