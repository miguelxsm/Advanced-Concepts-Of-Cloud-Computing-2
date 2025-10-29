REGION = "us-east-1"
SG_ORCHESTRATOR_NAME = "orchestrator"

IP_PERMISSIONS_ORCHESTRATOR = [
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
    }
]

SG_WORKERS_NAME = "workers"


REQUIRED_METRICS = [
    "HealthyHostCount",
    "UnHealthyHostCount",
    "RequestCount",
    "TargetResponseTime",
    "HTTPCode_Target_2XX_Count"
]