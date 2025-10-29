import boto3
from infrastructure.constants import REGION

ec2 = boto3.resource("ec2", region_name=REGION)

def create_instance(instance_type, sg_id, user_data, role_tag):
    """
    Creates an EC2 instance with:
    - Type instance_type
    - Security Group sg_id
    - Startup script user_data (may be empty for now)
    - Tag Role=orchestrator / Role=worker
    """
    instances = ec2.create_instances(
        ImageId="ami-00ca32bbc84273381",   # Ubuntu 22 in us-east-1 (valid)
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[sg_id],
        UserData=user_data,
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [{"Key": "Role", "Value": role_tag}]
            }
        ],
        KeyName="lab_key_2025_10_29"   # Debes tenerla creada
    )

    instance = instances[0]
    instance.wait_until_running()
    instance.reload()
    print(f"{role_tag} instance running → Public IP: {instance.public_ip_address}")
    return {
        "id": instance.id,
        "public_ip": instance.public_ip_address,
        "private_ip": instance.private_ip_address,
        "role": role_tag
    }


def create_orchestrator_and_workers(orchestrator_sg_id, workers_sg_id):
    print("Creating orchestrator instance...")
    orch = create_instance(
        instance_type="t2.large",
        sg_id=orchestrator_sg_id,
        user_data="",   
        role_tag="orchestrator"
    )

    print("Creating 4 worker instances...")
    workers = [ 
        create_instance(
            instance_type="t2.large",
            sg_id=workers_sg_id,
            user_data="",   
            role_tag="worker"
        ) for _ in range(4)
    ]

    return {"orchestrator" : orch, "workers" : workers}
