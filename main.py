from db_connection import MongoDBConnector, Neo4jConnector


Mongo_conn = MongoDBConnector(host='127.0.0.1', port=27017, db_name='Wycieczki')
Mongo_conn.connect()

if __name__ == "__main__":
    a=2