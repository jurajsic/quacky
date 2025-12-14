from pathlib import Path
import subprocess
import sys
import shutil

path_to_samples = Path("../samples/")
path_to_created_smt_files = Path("../smt-files/")

def create_aws_files(benchmark):
    full_path_to_benchmark = path_to_samples/benchmark/"exp_single"
    for policy in full_path_to_benchmark.rglob("*.json"):
        print(f"Processing {policy}")
        full_path_to_smt_directory = path_to_created_smt_files / policy.relative_to(path_to_samples).parent
        full_path_to_smt_directory.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, "translator.py", "-p1", f"{policy}", "-s", "-o", f"{full_path_to_smt_directory}/{policy.stem}"])
        subprocess.run([sys.executable, "translator.py", "-p1", f"{policy}", "-s", "-c", "-o", f"{full_path_to_smt_directory}/{policy.stem + "_resourcetypeconstraints"}"])
        subprocess.run([sys.executable, "translator.py", "-p1", f"{policy}", "-s", "-c", "-e", "-o", f"{full_path_to_smt_directory}/{policy.stem + "_resourcetypeconstraints_actionencoding"}"])

def create_azure_file(role_assignment, role_definitions):
    full_path_to_smt_directory = path_to_created_smt_files/"azure"
    full_path_to_smt_directory.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, "translator.py", "-ra1", f"{role_assignment}", "-rd", f"{role_definitions}", "-s", "-c", "-o", f"{full_path_to_smt_directory}/{role_assignment.stem + "_resourcetypeconstraints"}"])

def create_gcp_file(role_assignment, role_definitions):
    full_path_to_smt_directory = path_to_created_smt_files/"gcp"
    full_path_to_smt_directory.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, "translator.py", "-rb1", f"{role_assignment}", "-r", f"{role_definitions}", "-s", "-c", "-o", f"{full_path_to_smt_directory}/{role_assignment.stem + "_resourcetypeconstraints"}"])


print("Processing aws benchmark iam")
create_aws_files("iam")
print("Processing aws benchmark s3")
create_aws_files("s3")
print("Processing aws benchmark ec2")
create_aws_files("ec2")
print("Processing azure files")
create_azure_file(path_to_samples/"azure/role_assignments/compute_admin_login.json", path_to_samples/"azure/role_definitions/compute.json")
create_azure_file(path_to_samples/"azure/role_assignments/compute_user_login.json", path_to_samples/"azure/role_definitions/compute.json")
create_azure_file(path_to_samples/"azure/role_assignments/storage_data_contributor.json", path_to_samples/"azure/role_definitions/storage.json")
create_azure_file(path_to_samples/"azure/role_assignments/storage_data_owner.json", path_to_samples/"azure/role_definitions/storage.json")
create_azure_file(path_to_samples/"azure/role_assignments/storage_data_reader.json", path_to_samples/"azure/role_definitions/storage.json")
print("Processing gcp files")
create_gcp_file(path_to_samples/"gcp/role_bindings/compute_os_login.json", path_to_samples/"gcp/roles/compute.json")
create_gcp_file(path_to_samples/"gcp/role_bindings/compute_os_admin_login.json", path_to_samples/"gcp/roles/compute.json")
create_gcp_file(path_to_samples/"gcp/role_bindings/storage_object_admin.json", path_to_samples/"gcp/roles/storage.json")
create_gcp_file(path_to_samples/"gcp/role_bindings/storage_object_creator.json", path_to_samples/"gcp/roles/storage.json")
create_gcp_file(path_to_samples/"gcp/role_bindings/storage_object_viewer.json", path_to_samples/"gcp/roles/storage.json")
