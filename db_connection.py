from neo4j import GraphDatabase

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