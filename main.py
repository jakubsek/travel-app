from db_connection import Neo4jConnector
from pymongo import MongoClient
import gridfs
from PIL import Image
import json
import io
import matplotlib.pyplot as plt

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

#Nawiazanie polaczenia z mongo
def mongo_conn():
    try:
        conn = MongoClient(host='127.0.0.1', port=27017)
        print('Connected to Database')
        return conn
    except Exception as e:
        print('Error, cannot connect to database')

#Wgranie danych z pliku json -- poki co na sztywno testowa nazwa kolekcji, do zmiany pozniej
def load_data_from_json(file_path):
    db = mongo_conn()
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        db.Wycieczki.Test_insert.insert_many(data)

#wgranie zdjecia do kolekcji
def insert_image(file_name, file_path):
    db = mongo_conn()
    try:
        with open(file_path, "rb") as file_data:
            data = file_data.read()
            fs = gridfs.GridFS(db.Wycieczki)
            fs.put(data, filename=file_name)
            print("Image inserted successfully.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# def display_image_names():
#     db = mongo_conn()
#     fs = gridfs.GridFS(db.zdjecia)
#     files = fs.list()
#     if files:
#         print("Currently stored image names:")
#         for file in files:
#             print(file) 
#     else:
#         print("No images found in the database.")

#wyswietlenei nazw dostepnych wycieczek
def display_trips_names():
    db = mongo_conn()
    wycieczki = db.Wycieczki.zagraniczne.find()
    for wycieczka in wycieczki:
        print(wycieczka['name'])

#Wyswietlenie zdjecia
def display_image(image_id):
    db = mongo_conn()
    fs = gridfs.GridFS(db.zdjecia)
    image_data = fs.find_one({"_id": image_id})
    if image_data:
        img = Image.open(io.BytesIO(image_data.read()))
        img.show()
    else:
        print(f"Image with id '{image_id}' not found in the database.")

#Wyswietlenie zdjec z danej wycieczki
def display_images_of_trip(trip_name):
    db = mongo_conn()
    trip = db.Wycieczki.zagraniczne.find_one({'name': trip_name})
    image_object_ids = trip['images']
    if not image_object_ids:
        print("No images found in the database.")
        return
    fs = gridfs.GridFS(db.zdjecia)
    display_image(image_object_ids)
    current_index = 0
    while True:
        display_image(image_object_ids[current_index])
        user_input = input("Press 'n' for next image, 'p' for previous image, or 'q' to quit: ")
        if user_input.lower() == 'n':
            current_index = (current_index + 1) % len(image_object_ids)
        elif user_input.lower() == 'p':
            current_index = (current_index - 1) % len(image_object_ids)
        elif user_input.lower() == 'q':
            break
        else:
            print("Invalid input. Please try again.")

# Example usage:
# file_name = 'barcelona2.jpeg'
# file_path = 'C:/Users/filip/Desktop/barcelona2.jpeg'
# insert_image(file_name, file_path)
file_path = 'C:/Users/filip/Desktop/wycieczki.json'
load_data_from_json(file_path)

#display_image_names()
# display_trips_names('C:/Users/filip/Desktop/barcelona2.jpeg')
# trip_images_to_display = input("Enter the name of trip you want to see images of: ")
# display_images_of_trip(trip_images_to_display)


#image_to_display = input("Enter the name of the image you want to display: ")
# display_image('barcelona2.jpeg')
