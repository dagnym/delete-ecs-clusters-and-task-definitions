import boto3
import subprocess

def extract_family_revision(task_def_arn):
    parts = task_def_arn.split('/')
    return ':'.join(parts[-1].split(':')[-2:])

def delete_ecs_resources_in_region(region_name):
    print(f"Processing region: {region_name}")
    ecs_client = boto3.client('ecs', region_name=region_name)

    # Deleting ECS Services
    print("Deleting ECS Services...")
    clusters = ecs_client.list_clusters()['clusterArns']
    for cluster in clusters:
        services = ecs_client.list_services(cluster=cluster)['serviceArns']
        for service in services:
            print(f"Deleting Service: {service}")
            ecs_client.update_service(cluster=cluster, service=service, desiredCount=0)
            ecs_client.delete_service(cluster=cluster, service=service)

    # Deleting ECS Task Definitions
    print("Deleting ECS Task Definitions...")
    task_defs = ecs_client.list_task_definitions(status='INACTIVE')['taskDefinitionArns']
    for task_def in task_defs:
        task_def_family_revision = extract_family_revision(task_def)
        try:
            result = subprocess.run(["aws", "ecs", "delete-task-definitions", 
                            "--task-definitions", task_def_family_revision, 
                            "--region", region_name], 
                           capture_output=True, text=True, timeout=30)
            print(f"Delete command sent for Task Definition: {task_def_family_revision}")
            print("Output:", result.stdout)
            print("Error:", result.stderr)
        except subprocess.TimeoutExpired:
            print(f"Timeout expired for task definition {task_def_family_revision}")

    # Deleting ECS Clusters
    print("Deleting ECS Clusters...")
    for cluster in clusters:
        print(f"Deleting Cluster: {cluster}")
        ecs_client.delete_cluster(cluster=cluster)

def delete_ecs_resources_all_regions():
    regions = [
            "ap-northeast-1",  # Asia Pacific (Tokyo)
            "ap-northeast-2",  # Asia Pacific (Seoul)
            "ap-northeast-3",  # Asia Pacific (Osaka)
            "ap-south-1",      # Asia Pacific (Mumbai)
            "ap-southeast-1",  # Asia Pacific (Singapore)
            "ap-southeast-2",  # Asia Pacific (Sydney)     
            "ca-central-1",    # Canada (Central)
            "eu-central-1",    # Europe (Frankfurt)
            "eu-north-1",      # Europe (Stockholm)
            "eu-west-1",       # Europe (Ireland)
            "eu-west-2",       # Europe (London)
            "eu-west-3",       # Europe (Paris)
            "sa-east-1",       # South America (São Paulo)
            "us-east-1",       # US East (N. Virginia)
            "us-east-2",       # US East (Ohio)
            "us-west-1",       # US West (N. California)
            "us-west-2"        # US West (Oregon)
        ]

    for region in regions:
        try:
            print(f"Starting deletion in region: {region}")
            delete_ecs_resources_in_region(region)
        except Exception as e:
            print(f"Error processing region {region}: {e}")

if __name__ == "__main__":
    delete_ecs_resources_all_regions()
