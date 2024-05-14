from neo4j import GraphDatabase
from pymongo import MongoClient

class Neo4jConnector:
    _uri = "bolt://127.0.0.1:7687"
    _username = "neo4j"
    _password = "neo4jgraph"
    
    def __init__(self):
        self._driver = None
        self.connect()

    def connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._username, self._password))

    def close(self):
        if self._driver is not None:
            self._driver.close()
            self._driver = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def session(self):
        return self._driver.session()
    

class MongoDBConnector:
    def __init__(self, host, port, db_name):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        self.client = MongoClient(self.host, self.port)
        if self.db_name:
            self.db = self.client[self.db_name]
        else:
            raise ValueError("Nazwa bazy danych nie została podana.")

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
            self.db = None

    def session(self):
        if not self.client:
            raise ValueError("Brak aktywnego połączenia z bazą danych.")
        return self.client