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
- cd src && touch database.ts target.routes.ts target.ts server.ts
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
- nano .env
Paste:  FOR NOW UNTIL I CAN FIGURE OUT DATABASE PASSWORD SECURITY
'''
MONGO_URI=mongodb://localhost:27017
'''
- nano src/server.ts
paste:
'''
import * as dotenv from "dotenv";
import express from "express";
import cors from "cors";
import { connectToDatabase } from "./database";

// Load environment variables from the .env file, where the MONGO_URI is configured
dotenv.config();

const { MONGO_URI } = process.env;

if (!MONGO_URI) {
  console.error(
    "No MONGO_URI environment variable has been defined in config.env"
  );
  process.exit(1);
}

connectToDatabase(MONGO_URI)
  .then(() => {
    const app = express();
    app.use(cors());

    // start the Express server
    app.listen(5200, () => {
      console.log(`Server running at http://localhost:5200...`);
    });
  })
  .catch((error) => console.error(error));
'''
- do this command and you should see a server running output "npx ts-node src/server.ts"
ctl z and bg it
- nano src/target.routes.ts
Paste
'''
import * as express from "express";
import { ObjectId } from "mongodb";
import { collections } from "./database";

export const targetRouter = express.Router();
targetRouter.use(express.json());

targetRouter.get("/", async (_req, res) => {
    try {
        const targets = await collections?.targets?.find({}).toArray();
        res.status(200).send(targets);
    } catch (error) {
        res.status(500).send(error instanceof Error ? error.message : "Unknown error");
    }
});

targetRouter.get("/:Target", async (req, res) => {
    try {
        const targetID = req?.params?.Target;
        const query = { Target: targetID };
        const Target = await collections?.targets?.findOne(query);

        if (Target) {
            res.status(200).send(Target);
        } else {
            res.status(404).send(`Failed to find a Target: ${targetID}`);
        }
    } catch (error) {
        res.status(404).send(`Failed to find a Target: ${req?.params?.Target}`);
    }
});

targetRouter.post("/", async (req, res) => {
    try {
        const target = req.body;
        const result = await collections?.targets?.insertOne(target);

        if (result?.acknowledged) {
            res.status(201).send(`Created a new target: targetID ${result.insertedId}.`);
        } else {
            res.status(500).send("Failed to create a new target.");
        }
    } catch (error) {
        console.error(error);
        res.status(400).send(error instanceof Error ? error.message : "Unknown error");
    }
});

targetRouter.put("/:Target", async (req, res) => {
    try {
        const targetid = req?.params?.Target;
        const Target = req.body;
        const query = { Target: targetid };
        const result = await collections?.targets?.updateOne(query, { $set: Target });

        if (result && result.matchedCount) {
            res.status(200).send(`Updated a target: ID ${targetid}.`);
        } else if (!result?.matchedCount) {
            res.status(404).send(`Failed to find target: ID ${targetid}`);
        } else {
            res.status(304).send(`Failed to update target: ID ${targetid}`);
        }
    } catch (error) {
        const message = error instanceof Error ? error.message : "Unknown error";
        console.error(message);
        res.status(400).send(message);
    }
});

targetRouter.delete("/:Target", async (req, res) => {
    try {
        const targetid = req?.params?.Target;
        const query = { Target: targetid };
        const result = await collections?.targets?.deleteOne(query);

        if (result && result.deletedCount) {
            res.status(202).send(`Removed an employee: ID ${targetid}`);
        } else if (!result) {
            res.status(400).send(`Failed to remove an employee: ID ${targetid}`);
        } else if (!result.deletedCount) {
            res.status(404).send(`Failed to find an employee: ID ${targetid}`);
        }
    } catch (error) {
        const message = error instanceof Error ? error.message : "Unknown error";
        console.error(message);
        res.status(400).send(message);
    }
});
'''
- nano /src/server.ts
Paste this at the very begenning of file
'''
import { targetRouter } from "./target.routes";
'''
paste this before app.listen()
'''
app.use("/targets", targetRouter);
'''

?? maybe msised something

go to mean stack direcotry
npm install -g @angular/cli

do the npx command to start server, ctlz + bg

ng new client --inline-template --inline-style --minimal --routing --style=css
- said yes to all but data usage
cd client
ng serve -o
ng add @angular/material
ng generate interface target
nano /src/app/target.ts

'''

export interface Target {
  Target: string;
  Description: string;
}

'''

ng generate service target
nano src/app/target.service.ts
'''
import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Target } from './target';

@Injectable({
  providedIn: 'root'
})
export class TargetService {
  private url = 'http://localhost:5200';
  targets$ = signal<Target[]>([]);
  target$ = signal<Target>({} as Target);
 
  constructor(private httpClient: HttpClient) { }

  private refreshTargets() {
    this.httpClient.get<Target[]>(`${this.url}/targets`)
      .subscribe(targets => {
        this.targets$.set(targets);
      });
  }

  getTargets() {
    this.refreshTargets();
    return this.targets$();
  }

  getTarget(Target: string) {
    this.httpClient.get<Target>(`${this.url}/targets/${Target}`).subscribe(target => {
      this.target$.set(target);
      return this.target$();
    });
  }

  createTarget(target: Target) {
    return this.httpClient.post(`${this.url}/targets`, target, { responseType: 'text' });
  }

  updateTarget(id: string, target: Target) {
    return this.httpClient.put(`${this.url}/targets/${Target}`, target, { responseType: 'text' });
  }

  deleteTarget(Target: string) {
    return this.httpClient.delete(`${this.url}/targets/${Target}`, { responseType: 'text' });
  }
}

''

nano src/app/app.config.ts
- add this to top
import { provideHttpClient, withFetch } from '@angular/common/http';
-replace providors
'''
providers: [
    provideRouter(routes),
    provideHttpClient(withFetch()),
    // ...
  ],
'''
ng generate component targets-list

nano src/app/targets-list.component.ts

'''
import { Component, OnInit, WritableSignal } from '@angular/core';
import { Target } from '../target';
import { TargetService } from '../target.service';
import { RouterModule } from '@angular/router';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-targets-list',
  standalone: true,
  imports: [RouterModule, MatTableModule, MatButtonModule, MatCardModule],
  styles: [
    `
      table {
        width: 100%;

        button:first-of-type {
          margin-right: 1rem;
        }
      }
    `,
  ],
  template: `
    <mat-card>
      <mat-card-header>
        <mat-card-title>targets List</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <table mat-table [dataSource]="targets$()">
          <ng-container matColumnDef="col-Target">
            <th mat-header-cell *matHeaderCellDef>Name</th>
            <td mat-cell *matCellDef="let element">{{ element.Target }}</td>
          </ng-container>
          <ng-container matColumnDef="col-Description">
            <th mat-header-cell *matHeaderCellDef>Position</th>
            <td mat-cell *matCellDef="let element">{{ element.Description }}</td>
          </ng-container>
          <ng-container matColumnDef="col-action">
            <th mat-header-cell *matHeaderCellDef>Action</th>
            <td mat-cell *matCellDef="let element">
              <button mat-raised-button [routerLink]="['edit/', element._id]">
                Edit
              </button>
              <button
                mat-raised-button
                color="warn"
                (click)="deleteTarget(element.Target || '')"
              >
                Delete
              </button>
            </td>
          </ng-container>

          <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
          <tr mat-row *matRowDef="let row; columns: displayedColumns"></tr>
        </table>
      </mat-card-content>
      <mat-card-actions>
        <button mat-raised-button color="primary" [routerLink]="['new']">
          Add a New target
        </button>
      </mat-card-actions>
    </mat-card>
  `,
})
export class TargetsListComponent implements OnInit {
  targets$ = {} as WritableSignal<Target[]>;
  displayedColumns: string[] = [
    'col-Target',
    'col-Description',
  ];

  constructor(private targetsService: TargetService) {}

  ngOnInit() {
    this.fetchTargets();
  }

  deleteTarget(Target: string): void {
    this.targetsService.deleteTarget(Target).subscribe({
      next: () => this.fetchTargets(),
    });
  }

  private fetchTargets(): void {
    this.targets$ = this.targetsService.targets$;
    this.targetsService.getTargets();
  }
}

'''

nano src/app/app.routes.ts
'''
import { Routes } from '@angular/router';
import { TargetsListComponent } from './targets-list/targets-list.component';

export const routes: Routes = [
  { path: '', component: TargetsListComponent, title: 'Targets List' },
];

'''

nano src/app/app.component.ts

'''
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { TargetsListComponent } from './targets-list/employees-list.component';
import { MatToolbarModule } from '@angular/material/toolbar';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, TargetsListComponent, MatToolbarModule],
  styles: [
    `
      main {
        display: flex;
        justify-content: center;
        padding: 2rem 4rem;
      }
    `,
  ],
  template: `
    <mat-toolbar>
      <span>Targets Management System</span>
    </mat-toolbar>
    <main>
      <router-outlet />
    </main>
  `,
})
export class AppComponent {
  title = 'client';
}
'''
/client
ng g c target-form

'''
import { Component, effect, EventEmitter, input, Output } from '@angular/core';
import { FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatRadioModule } from '@angular/material/radio';
import { MatButtonModule } from '@angular/material/button';
import { Target } from '../target';

@Component({
  selector: 'app-target-form',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatRadioModule,
    MatButtonModule,
  ],
  styles: `
    .target-form {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      padding: 2rem;
    }
    .mat-mdc-radio-button ~ .mat-mdc-radio-button {
      margin-left: 16px;
    }
    .mat-mdc-form-field {
      width: 100%;
    }
  `,
  template: `
    <form
      class="target-form"
      autocomplete="off"
      [formGroup]="targetForm"
      (submit)="submitForm()"
    >
      <mat-form-field>
        <mat-label>Target</mat-label>
        <input matInput placeholder="Target" formControlName="target" required />
        @if (target.invalid) {
        <mat-error>Name must be at least 3 characters long.</mat-error>
        }
      </mat-form-field>

      <mat-form-field>
        <mat-label>Description</mat-label>
        <input
          matInput
          placeholder="Description"
          formControlName="Description"
          required
        />
        @if (Description.invalid) {
        <mat-error>Position must be at least 5 characters long.</mat-error>
        }
      </mat-form-field>

      <br />
      <button
        mat-raised-button
        color="primary"
        type="submit"
        [disabled]="targetForm.invalid"
      >
        Add
      </button>
    </form>
  `,
})
export class TargetFormComponent {
  initialState = input<Target>();

  @Output()
  formValuesChanged = new EventEmitter<Target>();

  @Output()
  formSubmitted = new EventEmitter<Target>();

  targetForm = this.formBuilder.group({
    Target: ['', [Validators.required, Validators.minLength(3)]],
    Description: ['', [Validators.required, Validators.minLength(5)]],
  });

  constructor(private formBuilder: FormBuilder) {
    effect(() => {
      this.targetForm.setValue({
        Target: this.initialState()?.Target || '',
        Description: this.initialState()?.Description || '',
      });
    });
  }

  get target() {
    return this.targetForm.get('Target')!;
  }
  get description() {
    return this.targetForm.get('Description')!;
  }

  submitForm() {
    this.formSubmitted.emit(this.targetForm.value as Target);
  }
}

'''

ng generate component add-target

nano src/app/add-target/add-target.component.ts

'''

import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { TargetFormComponent } from '../target-form/target-form.component';
import { Target } from '../target';
import { TargetService } from '../target.service';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-add-target',
  standalone: true,
  imports: [TargetFormComponent, MatCardModule],
  template: `
    <mat-card>
      <mat-card-header>
        <mat-card-title>Add a New Employee</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <app-target-form
          (formSubmitted)="addTarget($event)"
        ></app-target-form>
      </mat-card-content>
    </mat-card>
  `,
  styles: ``,
})
export class AddTargetComponent {
  constructor(
    private router: Router,
    private targetService: TargetService
  ) {}

  addTarget(target: Target) {
    this.targetService.createTarget(target).subscribe({
      next: () => {
        this.router.navigate(['/']);
      },
      error: (error) => {
        alert('Failed to create target');
        console.error(error);
      },
    });
    this.targetService.getTargets();
  }
}


'''

ng generate component edit-target
nano src/app/edit-target/edit-target.component.ts

'''
import { Component, OnInit, WritableSignal } from '@angular/core';
import { TargetFormComponent } from '../target-form/target-form.component';
import { ActivatedRoute, Router } from '@angular/router';
import { Target } from '../target';
import { TargetService } from '../target.service';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-edit-target',
  standalone: true,
  imports: [TargetFormComponent, MatCardModule],
  template: `
    <mat-card>
      <mat-card-header>
        <mat-card-title>Edit a target</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <app-target-form
          [initialState]="target()"
          (formSubmitted)="editTarget($event)"
        ></app-target-form>
      </mat-card-content>
    </mat-card>
  `,
  styles: ``,
})
export class EditTargetComponent implements OnInit {
  target = {} as WritableSignal<Target>;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private targetService: TargetService
  ) {}

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('Target');
    if (!id) {
      alert('No id provided');
    }

    this.targetService.getTarget(Target!);
    this.target = this.targetService.target$;
  }

  editTarget(target: Target) {
    this.targetService
      .updateTarget(this.target()._id || '', target)
      .subscribe({
        next: () => {
          this.router.navigate(['/']);
        },
        error: (error) => {
          alert('Failed to update target');
          console.error(error);
        },
      });
  }
}

'''

nano src/app/app-routing.module.ts

'''
import { Routes } from '@angular/router';
import { TargetsListComponent } from './targets-list/targets-list.component';
import { AddTargetComponent } from './add-target/add-target.component'; // <-- add this line
import { EditTargetComponent } from './edit-target/edit-target.component'; // <-- add this line

export const routes: Routes = [
  { path: '', component: TargetsListComponent, title: 'Target List' },
  { path: 'new', component: AddTargetComponent }, // <-- add this line
  { path: 'edit/:id', component: EditTargetComponent }, // <-- add this line
];

'''


# TODO
- css
- security
- update target info
- - uniform web design
  - maybe use javascript and node js instread of php
