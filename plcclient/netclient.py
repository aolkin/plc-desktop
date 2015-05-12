from plc.network.messages import *
from plc.network.protocols import ClientProtocol

from plc.core.errors import *
from plc.core.logging import *
from plc.core.settings import conf

from .interface import Screen

import asyncio, sys, os
from traceback import print_exc

class Client:
    def launch(self, conf=conf):
        self.loop = asyncio.get_event_loop()    
        self.screen = Screen(self.loop)

        print(conf["server"])
        coro = self.loop.create_connection(lambda: ClientProtocol(
            conf["user"], conf["password"], self.screen),
                                           conf["server"]["address"], conf["server"]["port"])
        log("Connecting to {}:{} as '{}'...".format(conf["server"]["address"],
                                                    conf["server"]["port"], conf["user"]))
        self.socket, self.protocol = self.loop.run_until_complete(coro)
        log("Connected.")
        
        self.loop.call_soon(self.screen.update)
        try:
            self.screen.wrapper(self.loop.run_forever, self.protocol)
        except BaseException as err:
            print_exc()
