from infrastructure.create_security_group import create_security_group, allow_orchestrator_to_workers
from infrastructure.destroy_infrastructure import destroy_all
from infrastructure.constants import SG_ORCHESTRATOR_NAME, SG_WORKERS_NAME, IP_PERMISSIONS_ORCHESTRATOR
from tools.instance_discovery import get_vpc_id_from_instances


if __name__ == "__main__":
    """
        Main pipeline of the app. It executes all the necessary steps sequencially
    """

    try:            
        print("--- Creating security group ---")

        vpc_id = get_vpc_id_from_instances();
        orchestrator_id = create_security_group(
            SECURITY_GROUP_NAME=SG_ORCHESTRATOR_NAME,
            PERMISSIONS=IP_PERMISSIONS_ORCHESTRATOR,
            DESCRIPTION="Security group for orchetrator",
            VPC_ID=vpc_id
            )
        
        workers_id = create_security_group(
            SECURITY_GROUP_NAME=SG_WORKERS_NAME,
            PERMISSIONS=[],
            DESCRIPTION="Security Group for Workers",
            VPC_ID=vpc_id
        )

        allow_orchestrator_to_workers(workers_id, orchestrator_id)
        print("Security groups successfully created")

        while True:
            ...


    except KeyboardInterrupt:
        print("CTRL+C Finishing Program ...")
        destroy_all()
        print("Everything erased")
        exit(1)


