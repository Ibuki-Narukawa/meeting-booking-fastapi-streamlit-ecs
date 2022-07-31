import {
  Stack,
  StackProps,
  aws_ec2 as ec2,
  aws_iam as iam,
  aws_ecs as ecs,
  aws_ecs_patterns as ecsPatterns,
  aws_efs as efs,
  aws_route53 as route53,
  aws_route53_targets as targets,
  aws_elasticloadbalancingv2 as elbv2,
  IgnoreMode,
} from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as environment from '../env/parameters';

export interface MeetingBookingStackProps extends StackProps {
  envName: string;
  projectName: string;
  params: environment.StackParams
}

export class MeetingBookingStack extends Stack {
  constructor(scope: Construct, id: string, props: MeetingBookingStackProps) {
    super(scope, id, props);

    const baseName = `${props.envName}-${props.projectName}`;

    /**
     * Building API
     */

    // create VPC
    const vpc = new ec2.Vpc(this, `vpc-${baseName}`, { 
      maxAzs: 2,
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: 'ingress',
          subnetType: ec2.SubnetType.PUBLIC,
        },
        {
          cidrMask: 24,
          name: 'application',
          subnetType: ec2.SubnetType.PRIVATE_WITH_NAT,
        },
     ]
    });

     // create EcsTaskExecutionRole
     const executionRole = new iam.Role(this, 'ecs-task-execution-role', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonECSTaskExecutionRolePolicy')
      ],
    });

    // create EcsServiceTaskRole
    const serviceTaskRole = new iam.Role(this, 'ecs-service-task-role', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
    });

    // create ECS Cluster
    const cluster = new ecs.Cluster(this, `cluster-${baseName}`, { 
      vpc: vpc,
      containerInsights: true,
    });

    // create EFS
    const fileSystem = new efs.FileSystem(this, `efs-${baseName}`, {
      vpc: vpc,
      removalPolicy: props.params.removalPolicy,
    });

    fileSystem.connections.allowFrom(ec2.Peer.anyIpv4(), ec2.Port.tcp(2049))

    // create EFS Volume
    const efsVolume = {
      // Use an Elastic FileSystem
      name: 'efs',
      efsVolumeConfiguration: {
        fileSystemId: fileSystem.fileSystemId,
      },
    };

    // create TaskDefinition
    const apiTaskDefinition = new ecs.FargateTaskDefinition(this, `task-def-${baseName}`, {
      memoryLimitMiB: 512,
      cpu: 256,
      executionRole: executionRole,
      taskRole: serviceTaskRole,
      volumes: [efsVolume],
    });

    // Add api container definition
    const apiContainer = apiTaskDefinition.addContainer(`api-container-def-${baseName}`, {
      image: ecs.AssetImage.fromAsset(props.params.apiParams.ecs.assetImage.directory, {
        ignoreMode: IgnoreMode.DOCKER,
        exclude: props.params.apiParams.ecs.assetImage.exclude,
      }),
    });

    // Add mount points
    apiContainer.addMountPoints({
      sourceVolume: efsVolume.name,
      containerPath: '/app/data',
      readOnly: false,
    });
    
    // Add a port mapping
    apiContainer.addPortMappings({
      containerPort: 80,
      protocol: ecs.Protocol.TCP,
    });

    // create ECS Service
    const apiService = new ecsPatterns.ApplicationLoadBalancedFargateService(this, `service-${baseName}`, {
      cluster: cluster,
      desiredCount: 1,
      taskDefinition: apiTaskDefinition,
      taskSubnets: { subnets: vpc.privateSubnets },
      protocol: elbv2.ApplicationProtocol.HTTP,
      openListener: false,
    });

    props.params.sourceCidrs.forEach((cidr) => {
      apiService.loadBalancer.connections.allowFrom(ec2.Peer.ipv4(cidr), ec2.Port.tcp(80))
    });

    apiService.service.connections.allowFrom(apiService.loadBalancer, ec2.Port.tcp(80))

    apiService.targetGroup.configureHealthCheck({
      path: '/healthcheck',
    });


    /**
     * Building Frontend
     */


  }
}
