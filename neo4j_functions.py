from db_connection import Neo4jConnector
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    hashed_password = hash_password(password)
    with Neo4jConnector() as db_connector:
        with db_connector.session() as session:
            existing_user = session.run(
                "MATCH (u:User) WHERE u.name = $username OR u.email = $email RETURN u",
                username=username,
                email=email
            ).single()

            if existing_user:
                return "Użytkownik o podanej nazwie użytkownika lub adresie email już istnieje"

            session.run(
                "CREATE (u:User {name: $username, email: $email, password: $password})",
                username=username,
                email=email,
                password=hashed_password 
            )
            return "Użytkownik zarejestrowany pomyślnie"



def login_user(username, password):
    hashed_password = hash_password(password)
    with Neo4jConnector() as db_connector:
        with db_connector.session() as session:
            user = session.run(
                "MATCH (u:User) WHERE u.name = $username AND u.password = $password RETURN u",
                username=username,
                password=hashed_password 
            ).single()

            if user:
                return "Zalogowano pomyślnie"
            else:
                return "Błędna nazwa użytkownika lub hasło"
            
def add_city(tx, city, country, latitude, longitude):
    result = tx.run("MATCH (c:City {name: $name, latitude: $latitude, longitude: $longitude}) RETURN c", 
                    name=city, latitude=latitude, longitude=longitude)
    if result.single() is None:
        tx.run("CREATE (c:City {name: $name, country: $country, latitude: $latitude, longitude: $longitude})", 
               name=city, country=country, latitude=latitude, longitude=longitude)
        print(f"Dodano miasto: {city}, {country}")
    else:
        print(f"Miasto {city}, {country} już istnieje w bazie danych.")
        
def add_country(tx, country, currency, code):
    result = tx.run("MATCH (c:Country {name: $name, currency: $currency, code: $code}) RETURN c", 
                    name=country, currency=currency, code=code)
    if result.single() is None:
        tx.run("CREATE (c:Country {name: $name, currency: $currency, code: $code})", 
                name=country, currency=currency, code=code)
        print(f"Dodano państwo: {country}, {country}")
    else:
        print(f"Państwo {country} już istnieje w bazie danych.")
        
def add_city_to_country_relationship(tx):
    tx.run("MATCH (c:City), (cc:Country {code: c.country}) "
           "MERGE (c)-[:IN]->(cc)")
    print("Dodano relacje między miastami a krajami.")
    
    
def add_relations():
    with Neo4jConnector() as db_connector:
        with db_connector.session() as session:
            session.write_transaction(add_city_to_country_relationship)
            
def import_cities_from_file():
    with open("cities15000.txt", "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("#"):
                continue
            data = line.split("\t")
            city = data[1]
            country = data[8]
            latitude = float(data[4])
            longitude = float(data[5])
            population = int(data[14])
            if population > 50000:
                print(city, country, latitude, longitude)
                with Neo4jConnector() as db_connector:
                    with db_connector.session() as session:
                        session.write_transaction(add_city, city, country, latitude, longitude)
                    
def import_country_from_file():
    with open("countryinfo.txt", "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("#"):
                continue
            data = line.split("\t")
            code = data[0]
            name = data[4]
            currency = data[10]
            print(code, name, currency)
            with Neo4jConnector() as db_connector:
                with db_connector.session() as session:
                    session.write_transaction(add_country, name, currency, code)