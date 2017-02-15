This is a CloudFormation Lambda-backed Custom Resource for MySQL Databases living inside RDS MySQL instances. It handles common management tasks such as creating/removing schemas and creating/removing users.

## Testing
Testing this module requires you have a mysql 5.6 database running with admin credentials of `admin` / `test4321`. Use `tests/mysqldatabase.sh` to execute the tests.
<!-- TODO Setup testing  -->
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