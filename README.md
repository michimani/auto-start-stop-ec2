# About
This is a CDK application for automatically starting / stopping EC2 instances that have specific tag name and value.

# Install and clone

0. Install AWS CDK (If you want to install globally.)

    If you have not installed AWS CDK, please install.

    ```bash
    $ npm install -g aws-cdk
    ```

1. Clone this repository

    ```bash
    $ git clone https://github.com/michimani/auto-start-stop-ec2.git
    $ cd auto-start-stop-ec2.git
    ```

2. Install packages

    ```bash
    $ npm install
    ```

3. Create S3 bucket for CDK application (optional)

    If you use AWS CDK with your AWS account and region in the first time, please run following command to create S3 bucket for CDK application.

    ```bash
    $ cdk bootstrap
    ```

# Usage


1. Add tag to EC2 instances

    Add tag name `AutoStartStop` with value `TRUE` to the target EC2 instances you want to start and stop automatically.
2. Create resources.  

    Create AWS resources using AWS CDK.
    
    1. Create config file.
    
        ```bash
        $ cp stack.config.json.sample stack.config.json
        ```

        - `event.cron.start` and `event.cron.stop` are cron options for Amazon EventBridge schedule rule.  
          *default:*  
          *start: "55 23 ? \* SUN-THU \*" ... it means 8 AM on weekday in Japan time (GMT+0900)*  
          *stop: "0 12 ? \* \* \*" ... it means 9 PM daily in Japan time (GMT+0900)*

        - `targets.ec2region` is a region that has target EC2 instances.  
          *default: ap-northeast-1*
    
    2. Generate CloudFormation template.
    
        ```bash
        $ cdk synth
        ```

    3. Check change set. (optional)
    
        ```bash
        $ cdk diff
        ```
        
    4. Deploy.
    
        ```bash
        $ cdk deploy
        ```

# Test

## Lambda function

1. Install modules.

    ```bash
    $ pip install boto3 moto pytest
    ```
    
2. Run test command.

    ```bash
    $ python -m pytest ./lambda/test/test_start_stop_ec2.py -vv
    ```