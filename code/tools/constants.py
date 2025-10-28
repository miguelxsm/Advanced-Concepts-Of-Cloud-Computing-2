REGION = "us-east-1"
SECURITY_GROUP_NAME = "lab01-security-group"
REQUIRED_METRICS = [
    "HealthyHostCount",
    "UnHealthyHostCount",
    "RequestCount",
    "TargetResponseTime",
    "HTTPCode_Target_2XX_Count"
]

IP_PERMISIONS=[
            {
                "IpProtocol": "tcp",
                "FromPort": 80,
                "ToPort": 80,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
            },
            {
                "IpProtocol": "tcp",
                "FromPort": 22,
                "ToPort": 22,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
            },
            {
                'FromPort': 80,
                'ToPort': 80,
                'IpProtocol': 'tcp',
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            },
        ]