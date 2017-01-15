#!/usr/bin/env python
import requests
import json

class Session(object):
    BASE_HEADERS = {
        "Content-Type": "application/vnd.alertme.zoo-6.1+json",
        "Accept": "application/vnd.alertme.zoo-6.1+json",
        "X-Omnia-Client": "Hive Web Dashboard",
    }

    BASE_URL = "https://api-prod.bgchprod.info:443/omnia"

    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__token = None
        self.login()
        self.populate_nodes()

    def request(self, method, resource, data=None, include_token=True):
        payload = json.dumps(data)
        url = "%s/%s" % (self.BASE_URL, resource.lstrip("/"))
        headers=self.__headers(include_token=include_token)
        r = requests.request(method.lower(), url, data=payload, headers=self.__headers(include_token=include_token))
        try:
            r.raise_for_status()
        except:
            print r.json()
            raise
        return r.json()

    def __headers(self, include_token=True):
        headers = {}
        headers.update(self.BASE_HEADERS)
        if include_token:
            if not self.__token:
                raise Exception("No token available, need to login first")
            headers['X-Omnia-Access-Token'] = self.__token
        return headers

    def login(self):
        data = {
            "sessions": [{
                "username": self.__username,
                "password": self.__password,
                "caller": "WEB"
            }]
        }
        self.__token = self.request("POST", "/auth/sessions", data=data, include_token=False)['sessions'][0]['sessionId']
    
    def populate_nodes(self):
        nodes = self.request("GET", "/nodes")
        self.__nodes = {}
        for n in nodes['nodes']:
            node = Node(self, n)
            self.__nodes[node.name] = node

    @property
    def nodes(self):
        return self.__nodes

    def get_node(self, node_name):
        return self.nodes[node_name]

class Node(object):
    def __init__(self, session, data):
        self.__session = session
        self.__populate(data)

    def __populate(self, data):
        self.__id = data['id']
        self.__name = data['name']
        self.__attributes = data['attributes']

    def refresh(self):
        data = self.__session.request("GET", "/nodes/%s" % self.id)
        self.__populate(data['nodes'][0])

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    @property
    def attributes(self):
        return self.__attributes

    def get_attribute(self, attribute):    
        return self.attributes[attribute]

    def set_attribute(self, attribute, value):
        data = {
            "nodes": [{
                "attributes": {
                    attribute: {
                        "targetValue": value
                    }
                }
            }]
        }
        self.__session.request("PUT", "/nodes/%s" % self.id, data)
