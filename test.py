from neo4j_functions import *

def print_list(list):
    col_width = max(len(value) for value in list) + 6
    for index, value in enumerate(list):
        if (index+1)%3==0 and index!=0:
            print(f"{index}) {value}".ljust(col_width))
        else:
            print(f"{index}) {value}".ljust(col_width),end=" ")

# print(register_user('jakubsek','test@test.pl','haslo1234'))
# print(register_user('jakubsek','test@test.pl','haslo124'))
# print(login_user('jakubsek','haslo1234'))
# print(login_user('jakubsek','haslo12534'))
# import_country_from_file()
# import_cities_from_file()
# add_relations()
# print(get_countries())
countries = get_countries()
print_list(countries)
countryIndex = input("\n\nPodaj numer państwa:")
selected_country = countries[int(countryIndex)]
cities = get_cities_in(selected_country)
print_list(cities)
cityIndex = input("\n\nPodaj numer miasta:")
selected_city = cities[int(cityIndex)]
print(selected_country,selected_city)