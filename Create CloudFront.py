import boto3

# Initialize the CloudFront client
cloudfront = boto3.client('cloudfront')

# Define the origin domain (replace with your ELB domain)
origin_domain_name = 'awseb--awseb-xxxxxxxxxxxx-##########.us-east-1.elb.amazonaws.com'

# Create the CloudFront distribution
response = cloudfront.create_distribution(
    DistributionConfig={
        'CallerReference': str(hash(origin_domain_name)),
        'Comment': 'CloudFront distribution for ELB',
        'Enabled': True,
        'Origins': {
            'Quantity': 1,
            'Items': [
                {
                    'Id': 'origin-1',
                    'DomainName': origin_domain_name,
                    'CustomOriginConfig': {
                        'HTTPPort': 80,
                        'HTTPSPort': 443,
                        'OriginProtocolPolicy': 'http-only'
                    }
                }
            ]
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': 'origin-1',
            'ViewerProtocolPolicy': 'allow-all',
            'AllowedMethods': {
                'Quantity': 7,
                'Items': [
                    'GET',
                    'HEAD',
                    'OPTIONS',
                    'PUT',
                    'POST',
                    'PATCH',
                    'DELETE'
                ],
                'CachedMethods': {
                    'Quantity': 2,
                    'Items': [
                        'GET',
                        'HEAD'
                    ]
                }
            },
            'ForwardedValues': {
                'QueryString': False,
                'Cookies': {
                    'Forward': 'none'
                }
            },
            'MinTTL': 0,
            'DefaultTTL': 86400,
            'MaxTTL': 31536000
        }
    }
)

# Output the distribution ID and status
distribution_id = response['Distribution']['Id']
distribution_status = response['Distribution']['Status']

print(f"CloudFront distribution created with ID: {distribution_id}")
print(f"Status: {distribution_status}")
