# Launching from a newly created AWS Account

## Dependancies 
* AWS Account 
* VPC with the appropriate subnets
* RDS instances (Postgres)
* Secrets Manager with Endpoint. See VPC Entpoint for Secrets Manager. @todo this can be added to the dam template

### VPC Entpoint for Secrets Manager

#### Seurity Group Settings

Inbound Rule

* Type: HTTPS (or Custom TCP if you enforce a non-standard port)
* Protocol: TCP
* Port Range: 443 (or your custom port)
* Source: The security group attached to your Lambda functions (or other resources that need access). Only allow specific security groups to limit exposure.

Outbound Rule (Generally)

* Type: All Traffic
* Protocol: All
* Port Range: All
* Destination: 0.0.0.0/0 (This allows general outbound traffic)

See [https://aws.amazon.com/blogs/security/how-to-connect-to-aws-secrets-manager-service-within-a-virtual-private-cloud/
] (VPC endpoint for security group)

## Github actions
Secrets for you repository
* 
