# Deployment of a Scalable Application: The Cloud Bootcamp Conference Raffle

![Image](https://i.imgur.com/D7voTti.png)

![Image](https://i.imgur.com/Hy9ed3X.png)

## Project Description
In this AWS cloud project, we will make an application that will need to support the high demand of a large number of users accessing it simultaneously. The application in this instance will be used by The Cloud Bootcamp Conference, which will have up to 10,000 participants from all over the world. The application will need to be able to handle all this volume.

During the event, 10 vouchers will be drawn for 3 prizes. The audience will register their email to enter the raffle. The objective of the project is to create an application for participants to access the page and enter the raffle. We will use various services within AWS to achieve this.

We will use Elastic Beanstalk to deploy a web application and DynamoDB to store the email addresses. CloudFront will be used to cache static and dynamic files to an Edge Location close to the user.

[![Watch on YouTube](https://img.youtube.com/vi/k8JchGmqOSI/0.jpg)](https://www.youtube.com/watch?v=k8JchGmqOSI)

## Part 1: Creating DynamoDB Table
The DynamoDB table will later house all of the email addresses of entrants in the raffle. Creating one is simple. We’ll create a table called `users`, set our partition key to `email` with type `String`, and have the table at default settings.

If you’d rather create it with code, we can run this Python script in VSCode: [Create DynamoDB.py](https://github.com/Rashon5/AWS-Cloud-Scalable-Application/blob/main/Create%20DynamoDB.py)

![Image](https://i.imgur.com/FgTIzcE.png)

Either way, we see it’s created. We’ll go into it later.

![Image](https://i.imgur.com/xW3CGhV.png)

## Part 2: Creating Elastic Beanstalk Application
In order to have our raffle, we’ll need to deploy our application and website on Elastic Beanstalk. The code to provision the application is here, but we will go through how to do it on the GUI. [Create Elastic Beanstalk.py](https://github.com/Rashon5/AWS-Cloud-Scalable-Application/blob/main/Create%20Elastic%20Beanstalk.py)

### Step 1: 
- **Environment tier**:
  - Application name: `tcb-conference`
- **Environment information**:
  - Environment name: `tcb-conference-env` (Automatic)
- **Platform**:
  - Platform: Python
  - Platform branch: Python 3.11 running on 64bit Amazon Linux 2023 (or recommended)
  - Platform version: 4.1.0 (or recommended)
- **Application code**:
  - Upload your code
  - Version label: `tcb-conference-source`
  - Public S3 URL: `https://tcb-bootcamps.s3.amazonaws.com/bootcamp-aws/en/module4/tcb-conf-app-EN.zip`

### Step 2:
- Create and use new service roles (If not already created)
- **Service Role**:
  - `aws-elasticbeanstalk-service-role` (Policies below)
    - `AWSElasticBeanstalkEnhancedHealth`
    - `AWSElasticBeanstalkManagedUpdatesCustomerRolePolicy`
- Create a new or existing key pair (Required)
- **EC2 Instance Profile**:
  - `aws-elasticbeanstalk-ec2-role` (Policies below)
    - `AmazonDynamoDBFullAccess`
    - `AWSElasticBeanstalkMulticontainerDocker`
    - `AWSElasticBeanstalkWebTier`
    - `AWSElasticBeanstalkWorkerTier`

### Step 3:
- VPC: Use default VPC
- **Instance settings**:
  - Activate check for Public IP address and check all Instance subnets

### Step 4: 
- **Instances**:
  - Root volume type: General Purpose (SSD)
  - Size: 10 GB
- **Capacity**:
  - Environment type: Load balanced
  - Instances: 2-4
  - Instance types: t2.micro
- **Scaling triggers**:
  - Metric: CPUUtilization
  - Statistic: Average
  - Unit: Percent
  - Period: 1 minute
  - Breach duration: 1 minute
  - Upper threshold: 50
  - Lower threshold: 40
- **Load balancer network settings**:
  - Check all subnets

### Step 5:
- **Platform software**:
  - **Container options**:
    - Environment properties (Add environment property):
      - Name: `AWS_REGION`
      - Value: `us-east-1`

Validate the Elastic Beanstalk resource has been properly created, then go to the supplied Domain website.

![Image](https://i.imgur.com/5j5Ol8Q.png)

Enter an email inside the user input area, then press Register.

![Image](https://i.imgur.com/WELoWVz.png)
![Image](https://i.imgur.com/Z608Fz4.png)

Return to DynamoDB, click your `users` table, and click on `Explore table items`.

![Image](https://i.imgur.com/M6NfXfR.png)

The email address has populated in the table.

![Image](https://i.imgur.com/EQP59sF.png)

## Part 3: Content Delivery with CloudFront
Open CloudFront and create a distribution. Click on `Origin domain` and click what is under the Elastic Load Balancer. To deploy using Python in VSCode: [Create CloudFront.py](https://github.com/Rashon5/AWS-Cloud-Scalable-Application/blob/main/Create%20CloudFront.py)

![Image](https://i.imgur.com/HkWO1id.png)

A domain will be generated which will be needed if this distribution is created through code. Set the Protocol to `HTTP only`.

![Image](https://i.imgur.com/CAIkh0c.png)

At Default cache behavior, under `Allowed HTTP methods`, select `GET HEAD OPTIONS PUT POST PATCH DELETE`.

![Image](https://i.imgur.com/kPpLjLz.png)

Under Web Application Firewall (WAF), set it to `Enable security protections`, then create.

![Image](https://i.imgur.com/dtQVTXn.png)

When the Distribution deploys (Last modified will have a date below), copy and paste the domain name into a browser and visit it.

![Image](https://i.imgur.com/FbXBHUH.png)

Try entering another email and it will go through and be added to the DynamoDB table.

![Image](https://i.imgur.com/FCc0dMj.png)
![Image](https://i.imgur.com/Onu5wHW.png)
![Image](https://i.imgur.com/wo6bja2.png)

## Part 4: Stress-Testing EC2 Instances to trigger ELB (Elastic Load Balancer)
Go to EC2 and find the public IP for one of the EC2 instances and SSH into it using GitBash or VSCode.

![Image](https://i.imgur.com/INsdbJ2.png)
![Image](https://i.imgur.com/C1r77XR.png)

When SSH’d in, install the stress test program with `sudo yum install stress -y`, then run the stress test with `stress -c 4` to stress all 4 CPU threads.

![Image](https://i.imgur.com/TRdv0kZ.png)

Open another GitBash instance and SSH into that as well, then run the `top` command to see the CPU usage, to see it’s adding up to 100%.

![Image](https://i.imgur.com/d4IDcUQ.png)

Elastic Beanstalk sees the high CPU usage and changes the Health status to Warning.

![Image](https://i.imgur.com/LYkCoXv.png)

After a few minutes, EC2 provisions a 3rd instance to manage the load.

![Image](https://i.imgur.com/PI2rbzM.png)

And now our raffle site has been made! Best of luck to the staff that gets chosen as the winner! Not too sure if there’s an AWS service for that; we can use a random generator to pick the winner.
