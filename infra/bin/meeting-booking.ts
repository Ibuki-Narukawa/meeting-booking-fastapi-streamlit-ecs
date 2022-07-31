#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { MeetingBookingStack } from '../lib/meeting-booking';
import * as environment from '../env/parameters';

const app = new cdk.App();

const projectName = app.node.tryGetContext('projectName');
const region = app.node.tryGetContext('region');
console.log('Project name is ' + projectName);
console.log('Region is ' + region);
const env: environment.Environments =
  (app.node.tryGetContext('env') as environment.Environments) ||
  environment.Environments.DEV;
  console.log('Current environment is ' + env);
const envParamaters: environment.EnvParameters = environment.getEnvParameters(env);


new MeetingBookingStack(app, 'MeetingBookingStack', {
  env: { account: envParamaters.account, region: region },
  envName: env,
  projectName: projectName,
  params: envParamaters.stackParams
});
