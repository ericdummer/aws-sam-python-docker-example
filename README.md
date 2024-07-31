# Tax Monitoring backend

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It also includes a hasura graphql engineA

!!!! I has had proprietary code removed. There are some good exampls and patterns here, but it will not work out of the box. Kept for references.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

## Dependencies

- AWS Account
- VPC with the appropriate subnets
- RDS instances (Postgres)
- Secrets Manager with Endpoint. See VPC Endpoint for Secrets Manager. @todo this can be added to the dam template
- SAM CLI installed. See [https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html] (Installing the AWS SAM CLI)
- Hasura CLI installed. See [https://hasura.io/docs/latest/hasura-cli/install-hasura-cli/] (Install / Uninstall the Hasura CLI
  )
- Docker Desktop - get a license from your manager

### VPC Endpoint for Secrets Manager

Because many of these endpoints must be within a VPC to connect to a RDS and many AWS services are not available within the VPC, you must create VPC endpoints. This is only needed for deployed applications.

#### Security Group Settings

Inbound Rule

- Type: HTTPS (or Custom TCP if you enforce a non-standard port)
- Protocol: TCP
- Port Range: 443 (or your custom port)
- Source: The security group attached to your Lambda functions (or other resources that need access). Only allow specific security groups to limit exposure.

Outbound Rule (Generally)

- Type: All Traffic
- Protocol: All
- Port Range: All
- Destination: 0.0.0.0/0 (This allows general outbound traffic)

See [https://aws.amazon.com/blogs/security/how-to-connect-to-aws-secrets-manager-service-within-a-virtual-private-cloud/
] (VPC endpoint for security group)

# Hasura

## Hasura Production, Stage and Dev 🚀✨✨✨✨

Stage, Production and Dev Hasura instances are hosted by Hasura. Local deployments are possible with a docker compose file in this repository. See [](Using Hasura Locally)

✨There should be no changes made in Production or Stage Hasura consoles. All changes should be made through the CI/CD pipelines. Mitigation of metadata and migration diffs should be done through the CLI.

🔧 The `hasura/stage.sh` facilitates interaction with the stage environment. The script temporarily loads environment variables found in `.env-stage`, which is ignored by git, and then runs the hasura command (any command, really)

## Using Hasura locally

Hasura supplies a docker compose file for local testing. An adapted version is included in this repository. To use it:

```bash
  cd hasura
  docker compose up -d
  hasura deploy
  hasura console
```

`hasura console` will launch the ui at `http://localhost:9695/` and open it in your default browser

All changes to the graphQL need to be done locally first and checked in. You can make them in the localhost console or through hasura cli commands.

CI/CD pipelines will promote these changes to stage and production. Do not deploy them through hasura's cli commands.

### Before you commit Hasura Migrations

Using the Harua console creates a lot of migration files. Please squash your migrations.

1. Get the earliest migration number

```bash
./stage.sh hasura migrate status
```

2. View the earlies file number that is not present in stage and then run: (Notice, don't include `./stage.sh`)

```bash
hasrua migrate squash --from <earliest> --name <optional>
```

3. Select `y` when asked if you should permanently delete the old migrations
4. Commit to source control

# Sam config files

The default sam config file is `samconfig.toml`. See aws docs to fully understand this file. Local development is facilitated by a git ignored `samconfig.local.toml`

There are two helper scripts to invoke functions: `./invoke-local.sh` and `./invoke-stage.sh`. One for local development and one to test on stage. Both commands are wrappers around SAM cli commands and can be used in place of `sam local invoke` or `sam remote invoke`. These script shorten commands and help clean up docker

The scripts does 3 things

1. sam deploy with either `--config-env=stage` or `--config-file=samconfig.local.toml`
2. sam local invoke {the rest of your command}
3. run `docker image prune -f` to clean up dangling images (happens a lot and Docker Desktop will tip over eventually)

Example

```bash
./invoke-local.sh UploadRequestFunction -e events/endpoints/upload_request/get-signed-url.json
```

## Running the api locally.

run (IN TESTING)

```bash
./start-local-api.sh
```

# Deploying

## Manual Deploying Hasura to stage

All deployments should be done through CI/CD pipelines.

To manually deploy:

```bash
cd hasura
./stage.sh hasura deploy
```

## Manually Deploying SAM

All deployments should be done through CI/CD pipelines.

To manually deploy:

````bash
./deploy-stage.sh
```# backend
````

## Naming Conventions

Naming conventions ensure consistency, readability, and maintainability. Consistent naming makes it easier for developers to understand the purpose of variables, functions, and classes, reducing the cognitive load when navigating and modifying the code. It facilitates collaboration, enabling team members to quickly grasp and work with each other's code. Additionally, it helps in avoiding conflicts and errors, promoting a more organized and efficient development process.

### Files and Folders
Each Lambda and the supporting files falls into one of 4 purposes: Authorizer, Consumer, API Enpoint and Schedulers. The below folder strucutre suppors this. All lambdas will follow similar patterns, but with some uniquesnes pases on their purpose.**


### *Authorizers*

* **Dockerfile**: src/Authorizer{*Service*}.dockerfile
  
  - Example: AuthorizerAuth0.dockerfile 
* **Folder and Files**: src/lambdas/authorizers/{*service*}/authorizer_{*service*}_lambda.py (or *.js)

  - Example: src/lambdas/authorizers/auth0/auth0_lambda.js
* **Test Events**: events/authorizer/{*service*}/{*test-name*}.json

  - Example: events/authorizers/auth0/event-post-user-registration.json

### *Consumers*

* **Dockerfile**: src/Consumer{*Resource*}{*Action*}.dockerfile
  
  - Example: Consumer1.dockerfile 
* **Folder and Files**: src/lambdas/consumers/{*resource*}_{*action*}/consumer_{*resource*}_{*action*}_lambda.py (or *.js)

  - Example: src/lambdas/consumers/consumer1/consumer_1_lambda.js
* **Test Events**: events/consumers/{*resource*}_{*action*}/{*test-name*}.json

  - Example: events/consumers/consumer1/event-ses-common.json

### *Endpoints*

* **Dockerfile**: src/Endpoint{*Resource*}{*Action*}.dockerfile
  
  - Example: Endpoint2.dockerfile 
* **Folder and Files**: src/lambdas/endpoints/{*resource*}\_{*action*}/endpoint_{*resource*}\_{*action*}_lambda.py (or *.js)

  - Example: src/lambdas/endpoints/document_get/endpoint_document_get_lambda.js
* **Test Events**: events/endpoints/{*resource*}\_{*action*}/{*test-name*}.json

  - Example: events/endpoints/document_get/account-document-get.json

### *Schedulers*

Frequency Exampes: Daily, Weekly, Monthly, Quarterly, Yearly

* **Dockerfile**: src/{*Frequency*}{*Resource*}{*Action*}.dockerfile
  
  - Example: Scheduler1.dockerfile 
* **Folder and Files**: src/lambdas/schedulers/{*frequency*}\_{*resource*}\_{*action*}/{*frequency*}\_{*resource*}\_{*action*}_lambda.py (or *.js)

  - Example: src/lambdas/schedulers/scheduler_1/scheduler.js
* **Test Events**: events/schedulers/{*frequency*}\_{*resource*}\_{*action*}/{*test-name*}.json

  - Example: events/schedulers/scheduler_1/account-document-get.json



## FOLDER stucture
```
.github/             # Github actions
events/              # Manual test input files for each lambda (Mimics the src of the folder structure)
  └── ...            
hausra/              # Hasrua files 
  └── ...            
tests/               # Directory for unit tests (Mimics the src of the folder structure) └── ...           
src/   
├── *.dockerfile     # All Dockerfiles wich represent a single lambda
├── ...              # Manyny more orchestration scripts and configuration files
├── authorizers/     # Lambda for authorizers
│   └── auth0
│     └── ...
├── consumers/
│   ├── ...  
│   └── scheduler_1/
│     ├── consumer_1_labmda.py # main file for the lambda
│     ├── requirements.txt
│     └── ...
├── endpoints/
│   ├── ... 
│   └── endpoint_1/
│     ├── endpoint_1.py # main file for the lambda
│     ├── requirements.txt
│     └── ...
├── models/
│   └── ...
├── schedulers/
│   ├── ... 
│   └── scheduler_1/
│     ├── scheduler_1_lambda.py # main file for the lambda
│     ├── requirements.txt
│     └── ...
├── services/
│   └── ...
└── utilities/
    ├── date_utils.py  
    ├── json_utils.py  
    ├── string_utils.py  # Data validation utilities
    └── ...
```


### Dockerfiles
Each dockerfile containerizes a lambda. Docker cannot include files in a parent folder. In order to eliminate mutiple copies of models, services and utilities docker files are placed in the root of the application folder (src.) Not all lambdas need the entire application structure. Alter the copy commands to include only the files used when you are looking for a small footprint for a lambda.

### Philosophy of the folder structure
* **Improved code organization**: Each component has a clear purpose, making the codebase easier to understand and maintain.
* **Increased reusability**: Utilities can be reused by multiple services or models, reducing code duplication.
* **Enhanced testability**: You can write focused unit tests for models and services, and integration tests to ensure their interaction with utilities works as expected.

#### Models:

* **Purpose**: Represent the data structures used by your application. They define the attributes and potentially the behavior of your data objects.
* **Focus**: Data attributes and potentially behavior relevant to the data itself.
* **Typical interactions**: Other models, database (via ORM)
* **Example**: A User model might contain attributes like name, email, and password. It could also have methods for basic data validation (e.g., checking if email is formatted correctly).

#### Services:
* **Purpose**: Encapsulate complex business logic and interact with external resources. They typically perform actions on your data models.
* **Focus**: Actions and workflows on data, including complex logic and orchestration.
* **Typical interactions**: Models, databases, external APIs, utilities
* **Example**: An AuthService might handle user registration, login, and password reset functionalities. It might interact with the User model and a database to perform these actions. Additionally, it could utilize a utility function for password hashing before storing it in the database.

#### Utilities:
* **Purpose**: Provide reusable, generic functionalities used across different parts of your application. They are not specific to a particular model or service.
* **Focus**: Common functionalities like file handling, logging, string manipulation, or data validation.
* **Typical interactions**: Any part of your application that needs the specific functionality provided by the utility.
* **Example**: A hash_password function in the utils module that takes a plain text password and returns a secure hash for storage. This function could be used by the AuthService for secure password handling.

### When to Use Each:

Models: Use models when defining the structure of your data or representing data retrieved from external sources.
Services: Use services to implement functionalities involving multiple models, complex logic, or interaction with external resources.
Utilities: Use utilities for any reusable, generic functionalities needed across different parts of your application logic or services.
Benefits of Separation:

Improved code organization: Each component has a clear purpose, making the codebase easier to understand and maintain.
Increased reusability: Utilities can be reused by multiple services or models, reducing code duplication.
Enhanced testability: You can write focused unit tests for models and services, and integration tests to ensure their interaction with utilities works as expected.