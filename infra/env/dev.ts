import { EnvParameters } from './parameters';
import * as path  from "path";
import { RemovalPolicy } from 'aws-cdk-lib';

export const devParams: EnvParameters = {
  account: '313332553193',
  stackParams: {
    sourceCidrs: ['0.0.0.0/0'],
    apiParams: {
      ecs: {
        assetImage: {
          directory: path.join('..', 'backend'),
        }
      },
    },
    frontendParams: {
      ecs: {
        assetImage: {
          directory: path.join('..', 'frontend'),
        }
      },
      route53: {
        customDomain: {
          hostedZoneId: 'Z09238098IGAO4ENOSSG',
          zoneName: 'meeting-booking.net',
          domainName: 'meeting-booking.net',
        },
      }
    },
    cicd: {
      env: 'dev',
      branch: 'main',
    },
  },
  removalPolicy: RemovalPolicy.DESTROY
};
