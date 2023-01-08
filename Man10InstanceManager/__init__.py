import json
import os
import time
from glob import glob
from threading import Thread

import docker
import requests
from flask import Flask

from Man10InstanceManager.methods.instance import InstanceMethod


class Man10InstanceManager:

    def delete_unneeded_bungee(self):
        while True:
            time.sleep(60*5)

            client = docker.from_env()
            current_container_short_ids = [x.short_id for x in client.containers.list(all=True)]

            bungee_registered_servers = requests.get(self.bungee_cord_api_endpoint)
            bungee_registered_servers = json.loads(bungee_registered_servers.text)["data"]
            delete_request_servers = [x["name"] for x in bungee_registered_servers if str(x["name"]).startswith("im-") and x["name"][3:] not in current_container_short_ids]
            for name in delete_request_servers:
                requests.delete(self.bungee_cord_api_endpoint, json={
                    "name": name
                })


    def __init__(self):
        # variables
        self.flask = Flask(__name__)
        self.flask.url_map.strict_slashes = False
        self.templates = {}
        self.config = {}

        self.tcp_ports = []
        self.udp_ports = []

        # load config

        config_file = open("config.json", encoding="utf-8")
        self.config = json.loads(config_file.read())
        config_file.close()

        self.bungee_cord_api_endpoint = self.config["bungeeCordAPI"]["endpoint"]
        self.bungee_cord_api_key = self.config["bungeeCordAPI"]["apiKey"]

        # load templates

        self.load_templates()

        # load available ports

        self.tcp_ports = [x for x in range(self.config["port"]["tcp"]["min"], self.config["port"]["tcp"]["max"]+1) if x not in self.config["port"]["tcp"]["disabled"]]
        self.udp_ports = [x for x in range(self.config["port"]["udp"]["min"], self.config["port"]["udp"]["max"]+1) if x not in self.config["port"]["udp"]["disabled"]]




        # register methods
        self.instance = InstanceMethod(self)

        # start auto delete thread
        Thread(target=self.delete_unneeded_bungee).start()

        self.flask.run("0.0.0.0", self.config["hostPort"])

    def load_templates(self):
        for path in glob("templates/*/*.json"):
            path_params = path[:-len(".json")].split(os.sep)[1:]
            file = open(path, encoding="utf-8")
            json_object = json.loads(file.read())
            file.close()
            self.templates["-".join(path_params)] = json_object
