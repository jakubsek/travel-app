from neo4j_functions import login_user, register_user, import_cities_from_file

print(register_user('jakubsek','test@test.pl','haslo1234'))
print(register_user('jakubsek','test@test.pl','haslo124'))
print(login_user('jakubsek','haslo1234'))
print(login_user('jakubsek','haslo12534'))
import_cities_from_file()