# Setting up the DB Proxy

Using this guyd
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy-setup.html

## Step 1: Create an AWS Secret

You can use the console, too.

```
aws secretsmanager create-secret \
  --name "tm-stage-db-proxy-credentials" \
  --description "tm Stage DB Proxy Credentials" \
  --region us-west-2 \
  --secret-string '{"username":"postgres","password":"<need to lookup>"}'
```

> DON'T change the secret-string keys, "username" and "password" are required key names

### Step2: Create a IAM policy

_example name:_ tm-stage-db-procy-for-lambdas-policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": [
        "arn:aws:secretsmanager:us-west-2:242761325242:secret:tm-stage-db-proxy-credentials-oOO7lO"
      ]
    },
    {
      "Sid": "VisualEditor1",
      "Effect": "Allow",
      "Action": "kms:Decrypt",
      "Resource": "arn:aws:kms:us-west-2:242761325242:key/5d03607a-b464-4505-a0ed-d0888c4b4592",
      "Condition": {
        "StringEquals": {
          "kms:ViaService": "secretsmanager.us-east-2.amazonaws.com"
        }
      }
    }
  ]
}
```

## Step 3: Create an IAM Role

1. Create a new IAM Role

- Skip the add resources step
- Save the role
- Go back in and add the policy you created above

2. Add the following trust relationships:

### Trust relationships

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "rds.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

## Step 3: Create the Proxy

1. Login into the AWS RDS console
2. Choose create proxy
3. Follow steps on [Getting started with RDS Proxy](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy-setup.html)
4. Add the Role you created in step 2
5. Add the secret you created in step 1
