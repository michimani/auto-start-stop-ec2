import events = require('@aws-cdk/aws-events');
import iam = require('@aws-cdk/aws-iam');
import lambda = require('@aws-cdk/aws-lambda');
import targets = require('@aws-cdk/aws-events-targets');
import cdk = require('@aws-cdk/core');

import fs = require('fs');

export class AutoStartStopEc2Stack extends cdk.Stack {
  constructor (app: cdk.App, id: string) {
    super(app, id);

    const stackConfig = JSON.parse(fs.readFileSync('stack.config.json', {encoding: 'utf-8'}));

    const lambdaFn = new lambda.Function(this, 'singleton', {
      code: new lambda.InlineCode(fs.readFileSync('lambda/auto-start-stop-ec2.py', {encoding: 'utf-8'})),
      handler: 'index.main',
      timeout: cdk.Duration.seconds(300),
      runtime: lambda.Runtime.PYTHON_3_7,
    });

    lambdaFn.addToRolePolicy(new iam.PolicyStatement({
      actions: [
        'ec2:DescribeInstances',
        'ec2:StartInstances',
        'ec2:StopInstances'
      ],
      resources: ['*']
    }));

    // STOP EC2 instances rule
    const stopRule = new events.Rule(this, 'StopRule', {
      schedule: events.Schedule.expression(`cron(${stackConfig.events.cron.stop})`)
    });

    stopRule.addTarget(new targets.LambdaFunction(lambdaFn, {
      event: events.RuleTargetInput.fromObject({Region: stackConfig.targets.ec2region, Action: 'stop'})
    }));

    // START EC2 instances rule
    const startRule = new events.Rule(this, 'StartRule', {
      schedule: events.Schedule.expression(`cron(${stackConfig.events.cron.start})`)
    });

    startRule.addTarget(new targets.LambdaFunction(lambdaFn, {
      event: events.RuleTargetInput.fromObject({Region: stackConfig.targets.ec2region, Action: 'start'})
    }));
  }
}
