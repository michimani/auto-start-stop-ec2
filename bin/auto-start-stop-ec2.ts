#!/usr/bin/env node
import 'source-map-support/register';
import cdk = require('@aws-cdk/core');
import { AutoStartStopEc2Stack } from '../lib/auto-start-stop-ec2-stack';

const app = new cdk.App();
new AutoStartStopEc2Stack(app, 'AutoStartStopEc2Stack');
