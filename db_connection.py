from neo4j import GraphDatabase, basic_auth

class Neo4jConnector:
    def __init__(self, uri, username, password):
        self._uri = uri
        self._username = username
        self._password = password
        self._driver = None

    def connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=basic_auth(self._username, self._password))

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def session(self):
        return self._driver.session()
