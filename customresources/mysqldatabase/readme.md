This is a CloudFormation Lambda-backed Custom Resource for MySQL Databases living inside RDS MySQL instances. It handles common management tasks such as creating/removing schemas and creating/removing users. Used in `templates/drupal-environment.yaml`.

## Usage
`````
  "MySQLDatabase" : {
    "Type" : "AWS::CloudFormation::CustomResource",
    "Version" : "1.0",
    "Properties" : {
       "ServiceToken" : "This lambda function's ARN",
       "KMSKeyARN" : "",
       "Hostname" : "mysql.example",
       "Port" : "3306",
       "Username" : "",
       "password" : "",
       "Database" : "some-StackName"
       "RetainDatabase" : true
    }
  }
 `````