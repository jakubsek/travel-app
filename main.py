from db_connection import Neo4jConnector

db_connector = Neo4jConnector("bolt://localhost:7687", "neo4j", "neo4jgraph")
db_connector.connect()

def register_user(username, email, password):
    with db_connector.session() as session:
        existing_user = session.run(
            "MATCH (u:User) WHERE u.username = $username OR u.email = $email RETURN u",
            username=username,
            email=email
        ).single()

        if existing_user:
            return "Użytkownik o podanej nazwie użytkownika lub adresie email już istnieje"

        session.run(
            "CREATE (u:User {username: $username, email: $email, password: $password})",
            username=username,
            email=email,
            password=password
        )
        return "Użytkownik zarejestrowany pomyślnie"


def login_user(username, password):
    with db_connector.session() as session:
        user = session.run(
            "MATCH (u:User) WHERE u.username = $username AND u.password = $password RETURN u",
            username=username,
            password=password
        ).single()

        if user:
            return "Zalogowano pomyślnie"
        else:
            return "Błędna nazwa użytkownika lub hasło"


print(register_user("jan_kowalski", "jan@example.com", "haslo123"))
print(register_user("jan_kowalski", "jan@example.com", "haslo456"))
print(login_user("jan_kowalski", "haslo123"))
print(login_user("jan_kowalski", "haslo456")) 

db_connector.close()
