import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';

import * as environment from '../env/parameters';

export interface MeetingBookingStackProps extends StackProps {
  envName: string;
  projectName: string;
  params: environment.StackParams
}

export class MeetingBookingStack extends Stack {
  constructor(scope: Construct, id: string, props?: MeetingBookingStackProps) {
    super(scope, id, props);
  }
}
