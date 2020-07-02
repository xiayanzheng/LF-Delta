import asyncio
import netdev


async def task(param):
    print("Connecting to {}".format(param["host"]))
    try:
        connect_param = {
            "username": param["username"],
            "password": param["password"],
            "device_type": param["device_type"],
            "host": param["host"]
        }
        async with netdev.create(**connect_param) as ios:
            # Testing sending simple command
            print(param)
            out = await ios.send_command("show ver")
            print(out)
    except Exception as e:
        print("[!]Can not connect to device... Err-Msg:{}".format(e))


async def run(devices):
    tasks = [task(dev) for dev in devices]
    await asyncio.wait(tasks)
