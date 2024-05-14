from db_connection import Neo4jConnector

def register_user(username, email, password):
    with Neo4jConnector() as conn:
        with conn.session() as session:
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
    with Neo4jConnector() as conn:
        with conn.session() as session:
            user = session.run(
                "MATCH (u:User) WHERE u.username = $username AND u.password = $password RETURN u",
                username=username,
                password=password
            ).single()

            if user:
                return "Zalogowano pomyślnie"
            else:
                return "Błędna nazwa użytkownika lub hasło"