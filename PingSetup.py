#### Setup ####
###Imports###
import pymongo
import hashlib

# Getting Admin User Data from input
Username = input("Enter Web GUI Admin username: ")
Password = input("Enter Web GUI Admin password: ")
Password = hashlib.sha256(Password.encode('utf-8')).hexdigest()
AdminUser = { "Username": Username, "Password": Password, "Role": "Admin" }

# Setting up database and creating Admin User
client = pymongo.MongoClient(host="localhost", port=27017)
db = client["database"]
collection = db["targets"]
collection = db["errors"]
collection.create_index([("createdAt", 1)], expireAfterSeconds=604800)
collection = db["collection"]
collection.create_index([("createdAt", 1)], expireAfterSeconds=604800)
collection = db["users"]
collection.insert_one(AdminUser)
client.close()
