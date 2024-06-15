import boto3

# Initialize the Elastic Beanstalk client
eb_client = boto3.client('elasticbeanstalk', region_name='us-east-1')

# Define application and environment details
application_name = 'tcb-conference'
environment_name = 'tcb-conference-env'
version_label = 'tcb-conference-source'
s3_url = 'https://tcb-bootcamps.s3.amazonaws.com/bootcamp-aws/en/module4/tcb-conf-app-EN.zip'

# Create the application
eb_client.create_application(
    ApplicationName=application_name,
    Description='tcb-conference application'
)

# Create the application version
eb_client.create_application_version(
    ApplicationName=application_name,
    VersionLabel=version_label,
    SourceBundle={
        'S3Bucket': 'tcb-bootcamps',
        'S3Key': 'bootcamp-aws/en/module4/tcb-conf-app-EN.zip'
    }
)

# Specified VPC and subnets
vpc_id = 'vpc-0eae10351618b86ca'
subnet_ids = [
    'subnet-009ab6c82e19820f7',
    'subnet-0f597a4249f1c9d7e',
    'subnet-0ef6cdb796fdaabdd',
    'subnet-06d7d4ef742b85a60',
    'subnet-027db9206c790e858',
    'subnet-01b0c7f162a9694d8'
]

# Create the environment
response = eb_client.create_environment(
    ApplicationName=application_name,
    EnvironmentName=environment_name,
    PlatformArn='arn:aws:elasticbeanstalk:us-east-1::platform/Python 3.11 running on 64bit Amazon Linux 2023/4.1.0',
    OptionSettings=[
        {
            'Namespace': 'aws:elasticbeanstalk:environment',
            'OptionName': 'EnvironmentType',
            'Value': 'LoadBalanced'
        },
        {
            'Namespace': 'aws:autoscaling:launchconfiguration',
            'OptionName': 'InstanceType',
            'Value': 't2.micro'
        },
        {
            'Namespace': 'aws:autoscaling:launchconfiguration',
            'OptionName': 'EC2KeyName',
            'Value': 'beanstalk-key'  # Replace with your key pair name
        },
        {
            'Namespace': 'aws:autoscaling:asg',
            'OptionName': 'MinSize',
            'Value': '2'
        },
        {
            'Namespace': 'aws:autoscaling:asg',
            'OptionName': 'MaxSize',
            'Value': '4'
        },
        {
            'Namespace': 'aws:autoscaling:trigger',
            'OptionName': 'MeasureName',
            'Value': 'CPUUtilization'
        },
        {
            'Namespace': 'aws:autoscaling:trigger',
            'OptionName': 'Statistic',
            'Value': 'Average'
        },
        {
            'Namespace': 'aws:autoscaling:trigger',
            'OptionName': 'Unit',
            'Value': 'Percent'
        },
        {
            'Namespace': 'aws:autoscaling:trigger',
            'OptionName': 'UpperThreshold',
            'Value': '50'
        },
        {
            'Namespace': 'aws:autoscaling:trigger',
            'OptionName': 'LowerThreshold',
            'Value': '40'
        },
        {
            'Namespace': 'aws:autoscaling:trigger',
            'OptionName': 'Period',
            'Value': '60'  # 1 minute (60 seconds)
        },
        {
            'Namespace': 'aws:autoscaling:trigger',
            'OptionName': 'BreachDuration',
            'Value': '60'  # 1 minute (60 seconds)
        },
        {
            'Namespace': 'aws:elasticbeanstalk:environment:process:default',
            'OptionName': 'StickinessEnabled',
            'Value': 'true'
        },
        {
            'Namespace': 'aws:elasticbeanstalk:environment:process:default',
            'OptionName': 'StickinessLBCookieDuration',
            'Value': '60'
        },
        {
            'Namespace': 'aws:elasticbeanstalk:environment:process:default',
            'OptionName': 'HealthCheckPath',
            'Value': '/'
        },
        {
            'Namespace': 'aws:elasticbeanstalk:environment',
            'OptionName': 'ServiceRole',
            'Value': 'arn:aws:iam::654654634038:role/service-role/aws-elasticbeanstalk-service-role'
        },
        {
            'Namespace': 'aws:elasticbeanstalk:environment',
            'OptionName': 'LoadBalancerType',
            'Value': 'application'
        },
        {
            'Namespace': 'aws:elasticbeanstalk:application:environment',
            'OptionName': 'AWS_REGION',
            'Value': 'us-east-1'
        },
        {
            'Namespace': 'aws:elasticbeanstalk:application:environment',
            'OptionName': 'PYTHONPATH',
            'Value': '/var/app/venv/staging-LQM1lest/bin'
        },
        {
            'Namespace': 'aws:ec2:vpc',
            'OptionName': 'VPCId',
            'Value': vpc_id
        },
        {
            'Namespace': 'aws:ec2:vpc',
            'OptionName': 'Subnets',
            'Value': ','.join(subnet_ids)  # Instance subnets
        },
        {
            'Namespace': 'aws:ec2:vpc',
            'OptionName': 'ELBSubnets',
            'Value': ','.join(subnet_ids)  # Load balancer subnets
        },
        {
            'Namespace': 'aws:ec2:vpc',
            'OptionName': 'AssociatePublicIpAddress',
            'Value': 'true'
        },
        {
            'Namespace': 'aws:autoscaling:launchconfiguration',
            'OptionName': 'IamInstanceProfile',
            'Value': 'aws-elasticbeanstalk-ec2-role'  # Ensure you have this role created
        }
    ],
    VersionLabel=version_label
)

print("Elastic Beanstalk environment creation initiated.")
print(response)
