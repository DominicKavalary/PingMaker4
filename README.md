# PingMaker4
pingmaker3 but attempted to add database stuff and maybe web stuff



## MongoDB Installation For Monitoring Database
### Ubuntu Server (Tested on Noble)
- sudo apt-get install gnupg curl
- curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg  --dearmor
- echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
- sudo apt-get update
- sudo apt-get install -y mongodb-org
- sudo systemctl enable mongod
- sudo systemctl start mongod

####Possibly i dunno yet well see
go to /etc/security/limits.conf and add:
mongodb soft nofile 64000
mongodb hard nofile 64000

set to 100000

sudo nano /etc/sysctl.conf
fs.file-max = 2097152
sudo sysctl -p

sudo nano /etc/pam.d/common-session
session required pam_limits.so


## PingMaker Monitoring Script Setup
### Ubuntu Server (Tested on Noble)
- sudo su
- mkdir /home/PingMaker
- cd /home/PingMaker
- wget https://raw.githubusercontent.com/DominicKavalary/PingMaker4/refs/heads/main/PingMaker.py
- nano /etc/systemd/system/PingMaker.service
  Copy paste the contents of the PingMaker.service file in the repository
- systemctl enable PingMaker.service
- systemctl daemon-reload
- systemctl start PingMaker.service

## MEAN Stack Setup
### Ubuntu Server (Tested on Noble)
We will be largely following a tutorial made by mongodb on hwo to create a MEAN stack, except modifying it to fit our databases needs
https://www.mongodb.com/resources/languages/mean-stack-tutorial

- apt install npm
- mkdir /home/PingMaker/MEAN_Stack
- cd /home/PingMaker/MEAN_Stack
- mkdir server && mkdir server/src
- cd server
- npm init -y
- touch tsconfig.json .env
GET READY TO CHANGE THE BELOW NAMES TO FIT YOUR STUFF
- cd src && touch database.ts employee.routes.ts target.ts server.ts
- cd ..
- npm install cors dotenv express mongodb
SOMETHING ABOUT NOT HAVING THESE IN FULL PRODUCTION
- npm install --save-dev typescript @types/cors @types/express @types/node ts-node
- nano tsconfig.json
Paste:
'''
{
  "include": ["src/**/*"],
  "compilerOptions": {
    "target": "es2016",
    "module": "commonjs",
    "esModuleInterop": true,  
    "forceConsistentCasingInFileNames": true,
    "strict": true,    
    "skipLibCheck": true,
    "outDir": "./dist"
  }
}
'''
- nano src/target.ts
Paste:
'''
import * as mongodb from "mongodb";

export interface Target {
    Target: string;
    Description: string;
}
'''

- nano src/database.ts
Paste:
'''
import * as mongodb from "mongodb";
import { Target } from "./target";

export const collections: {
    targets?: mongodb.Collection<Target>;
} = {};

export async function connectToDatabase(uri: string) {
    const client = new mongodb.MongoClient(uri);
    await client.connect();

    const db = client.db("database");
    await applySchemaValidation(db);

    const targetsCollection = db.collection<Target>("targets");
    collections.targets = targetsCollection;
}

// Update our existing collection with JSON schema validation so we know our documents will always match the shape of our Employee model, even if added elsewhere.
// For more information about schema validation, see this blog series: https://www.mongodb.com/blog/post/json-schema-validation--locking-down-your-model-the-smart-way
async function applySchemaValidation(db: mongodb.Db) {
    const jsonSchema = {
        $jsonSchema: {
            bsonType: "object",
            required: ["Target", "Description"],
            additionalProperties: false,
            properties: {
                _id: {},
                Target: {
                    bsonType: "string",
                    description: "'Target' is required and is a string in the form of a hostname or ipv4 address",
                },
                Description: {
                    bsonType: "string",
                    description: "'Description' is required and is a string",
                    minLength: 5
                },
                
            },
        },
    };

    // Try applying the modification to the collection, if the collection doesn't exist, create it
   await db.command({
        collMod: "targets",
        validator: jsonSchema
    }).catch(async (error: mongodb.MongoServerError) => {
        if (error.codeName === "NamespaceNotFound") {
            await db.createCollection("targets", {validator: jsonSchema});
        }
    });
}
'''

# TODO
- css
- security
- update target info
- - uniform web design
  - maybe use javascript and node js instread of php
