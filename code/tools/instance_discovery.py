import json
import boto3
from infrastructure.constants import REGION

ec2 = boto3.client("ec2", region_name=REGION)

def get_vpc_id_from_instances():
    ec2 = boto3.client("ec2", region_name=REGION)
    resp = ec2.describe_vpcs(Filters=[{"Name": "isDefault", "Values": ["true"]}])
    if resp["Vpcs"]:
        vpc_id = resp["Vpcs"][0]["VpcId"]
        print(f"VPC id found: {vpc_id}")
        return vpc_id
    

def save_instance_ips(topology: dict, path: str = "instance_ips.json"):
    payload = {
        "orchestrator" : {
            "public_ip" : topology["orchestrator"]["public_ip"],
            "private_ip" : topology["orchestrator"]["private_ip"]
        },
        "workers": [
            {"public_ip": w["public_ip"], "private_ip": w["private_ip"]}
            for w in topology["workers"]
        ],
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"IP's saved in {path}")
    return path