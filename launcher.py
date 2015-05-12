#!/usr/bin/env python3

import os

from plcclient.netclient import Client
from plc.core.settings import Configuration

client = Client()
conf = Configuration()
conf.load(os.environ.get("PLC_SETTINGS","clientsettings.json"))

if __name__ == "__main__":
    client.launch(conf)
