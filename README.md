# AWS Lambda + Serverless Framework: Hello World

## Requirements
* [Serverless Framework](https://github.com/serverless/serverless)

## Deploy

```sh
sls deploy [--aws-profile PROFILE]
```

## Execute

Any of these command will run the Lambda function.

```sh
sls invoke --log --function hello [--data "{\"name\":\"${USER}\"}"] [--aws-profile PROFILE]
curl -X POST https://[api-id].execute-api.us-east-1.amazonaws.com
curl -d "name=${USER}" https://[api-id].execute-api.us-east-1.amazonaws.com
curl -H "Content-Type: application/json" -d "{\"name\":\"${USER}\"}" https://[api-id].execute-api.us-east-1.amazonaws.com
```

## Run / Test Locally

```sh
serverless invoke local --function hello
```

## Created from template

```sh
sls create --template aws-python3
```

## References

* https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html
* https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html
* https://serverless.com/framework/docs/providers/aws/examples/hello-world/python/

# License
Copyright 2020 digitalr00ts

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
