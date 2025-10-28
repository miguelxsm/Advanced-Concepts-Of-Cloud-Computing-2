import boto3
from botocore.exceptions import ClientError
from infrastructure import constants as c

# Resource is a high-level API
# Client is a low-level API
ec2_resource = boto3.resource("ec2", region_name=c.REGION)
ec2_client = boto3.client("ec2", region_name=c.REGION)

def allow_orchestrator_to_workers(workers_sg_id, orchestrator_sg_id):
    ec2_client.authorize_security_group_ingress(
        GroupId=workers_sg_id,
        IpPermissions=[{
            "IpProtocol": "tcp",
            "FromPort": 5000,
            "ToPort": 5003,
            "UserIdGroupPairs": [{"GroupId": orchestrator_sg_id}]
        }]
    )

def security_group_exists(SECURITY_GROUP_NAME):
    try:
        resp = ec2_client.describe_security_groups(
            Filters=[{"Name": "group-name", "Values": [SECURITY_GROUP_NAME]}]
        )
        return len(resp.get("SecurityGroups", [])) > 0
    except ClientError as e:
        print("Error checking SG:", e)
        return False

def create_security_group(SECURITY_GROUP_NAME, PERMISSIONS, DESCRIPTION, VPC_ID):
    resp = ec2_client.describe_security_groups(
        Filters=[{"Name": "group-name", "Values": [SECURITY_GROUP_NAME]}]
    )
    if resp.get("SecurityGroups"):
        return resp["SecurityGroups"][0]["GroupId"]

    # Create SG
    sg_resp = ec2_client.create_security_group(
        GroupName=SECURITY_GROUP_NAME,
        Description=DESCRIPTION,
        VpcId=VPC_ID
    )
    sg_id = sg_resp["GroupId"]
    print("Security group creation started. Security group id:", sg_id)

    if PERMISSIONS:
        try:
            ec2_client.authorize_security_group_ingress(
                GroupId=sg_id,
                IpPermissions=PERMISSIONS
            )
        except ClientError as e:
            if e.response["Error"]["Code"] != "InvalidPermission.Duplicate":
                raise

    print("Security group creation finished")
    return sg_id
