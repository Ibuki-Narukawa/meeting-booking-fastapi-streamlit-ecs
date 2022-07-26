#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { MeetingBookingStack } from '../lib/meeting-booking';

const app = new cdk.App();
new MeetingBookingStack(app, 'MeetingBookingStack', {
  
});
