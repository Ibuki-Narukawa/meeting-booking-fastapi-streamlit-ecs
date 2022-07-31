import { devParams } from './dev';
import { RemovalPolicy } from 'aws-cdk-lib';

export enum Environments {
  PROD = 'prod',
  STG = 'stg',
  DEV = 'dev',
}

export interface EcsParams {
  assetImage: {
    directory: string;
    dockerfilePath?: string;
    exclude?: string[];
  };
}

export interface Route53Params {
  customDomain: {
    hostedZoneId: string;
    zoneName: string;
    domainName: string;
  };
}

export interface StackParams {
  sourceCidrs: string[];
  apiParams: {
    ecs: EcsParams;
    route53?: Route53Params;
  };
  frontendParams: {
    ecs: EcsParams;
    route53: Route53Params;
  };
  cicd?: {
    env: string;
    branch: string;
  };
  removalPolicy: RemovalPolicy;
}

export interface EnvParameters {
  account: string;
  stackParams: StackParams;
}

const parameters: { [key: string]: EnvParameters } = {
  [Environments.DEV]: devParams,
  // [Environments.STG]: stgParams,
  // [Environments.PROD]: prodParams,
};

export const getEnvParameters = (env: Environments) => parameters[env];
