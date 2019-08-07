# About
This is a CDK application for automatically starting / stopping EC2 instances that have specific tag name and value.

# Usage

If you have not installed AWS CDK, please install.

```
npm install -g aws-cdk
```

1. Add tag name `AutoStartStop` with value `TRUE` to the target EC2 instances.
2. Create resources.  
    1. run `npm install`
    2. create config file.
        ```
        cp stack.config.json.sample stack.config.json
        ```

        - `event.cron.start` and `event.cron.stop` are cron options for CloudWatch Event schedule.  
          *default:*  
          *start: "55 23 ? \* SUN-THU \*" ... it means 8 AM on weekday in Japan time (GMT+0900)*  
          *stop: "0 12 ? \* \* \*" ... it means 9 PM daily in Japan time (GMT+0900)*

        - `targets.ec2region` is a region that has target EC2 instances.  
          *default: ap-northeast-1*
    3. run `npm run build`
    4. run `cdk deploy`
