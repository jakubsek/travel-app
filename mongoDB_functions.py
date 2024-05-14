from pymongo import *
from db_connection import MongoDBConnector
import gridfs
from PIL import Image
import json
import io

Mongo_conn = MongoDBConnector(host='127.0.0.1', port=27017, db_name='Wycieczki')
Mongo_conn.connect()

def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    Mongo_conn.db.zagraniczne.insert_many(data)

def insert_image(file_name, file_path):
    try:
        with open(file_path, "rb") as file_data:
            data = file_data.read()
            fs = gridfs.GridFS(Mongo_conn.db.zdjecia)
            fs.put(data, filename=file_name)
            print("Image inserted successfully.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


#wyswietlenei nazw dostepnych wycieczek
def display_trips_names():
    wycieczki = Mongo_conn.db.zagraniczne.find()
    for wycieczka in wycieczki:
        print(wycieczka['name'])


#Wyswietlenie zdjecia
def display_image(image_id):
    fs = gridfs.GridFS(Mongo_conn.db.zdjecia)
    image_data = fs.find_one({"_id": image_id})
    if image_data:
        img = Image.open(io.BytesIO(image_data.read()))
        img.show()
    else:
        print(f"Image with id '{image_id}' not found in the database.")


#Wyswietlenie zdjec z danej wycieczki
def display_images_of_trip(trip_name):
    trip = Mongo_conn.db.zagraniczne.find_one({'name': trip_name})
    image_object_ids = trip['images']
    if not image_object_ids:
        print("No images found in the database.")
        return
    fs = gridfs.GridFS(Mongo_conn.db.zdjecia)
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
file_path = 'wycieczki.json'
load_data_from_json(file_path)
Mongo_conn.close
#display_image_names()
# display_trips_names('C:/Users/filip/Desktop/barcelona2.jpeg')
# trip_images_to_display = input("Enter the name of trip you want to see images of: ")
# display_images_of_trip(trip_images_to_display)


#image_to_display = input("Enter the name of the image you want to display: ")
# display_image('barcelona2.jpeg')