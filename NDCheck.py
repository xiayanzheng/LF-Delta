from handle_Network_Devices.interface.flow import Interface
import asyncio

dc = Interface()
loop = asyncio.get_event_loop()
loop.run_until_complete(dc.flow())