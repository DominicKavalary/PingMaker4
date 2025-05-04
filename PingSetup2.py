###Imports###
import pymongo
import hashlib
import subprocess

####### Innitializing Database and Adding Default Admin User #######
print("------ Creating default admin user and innitializing database tables ------")
print("Making Default User")
Username = "admin"
Password = "admin"
Password = hashlib.sha256(Password.encode('utf-8')).hexdigest()
AdminUser = { "Username": Username, "Password": Password, "Role": "Admin" }
print("Connecting to mongodb and innitializing tables and admin user")
client = pymongo.MongoClient(host="localhost", port=27017)
db = client["database"]
collection = db["targets"]
collection = db["errors"]
collection.create_index([("createdAt", 1)], expireAfterSeconds=604800)
collection = db["collection"]
collection.create_index([("createdAt", 1)], expireAfterSeconds=604800)
collection = db["users"]
collection.insert_one(AdminUser)
collection = db["traceroutes"]
collection.create_index([("createdAt", 1)], expireAfterSeconds=604800)
collection = db["tracemaps"]
client.close()
