# pylint: disable=C0301
"""
This script allows user to run terraform command for a specific file.

Usage:
    python -m terraform_target.main --tf-files=<tf files for terraform to action> --action=<plan/apply/destroy> --env=<env> --env-id=<env-id>
"""

import os
import subprocess
import argparse
import re
from pathlib import Path
from conflog import Conflog

cfl = Conflog(conf_files=[f"{Path(__file__).parent}/conflog.yaml"])
logger = cfl.get_logger("terraform_target")
REPO_DIR = os.getcwd()


def construct_tf_target(tf_files: str) -> str:
    """
    :param tf_files: Target tf files to run terraform cmd against to
    :return tf_target: Target resource string
    """
    tf_resources = []
    tf_file_list = tf_files.split(",")
    for tf_file in tf_file_list:
        try:
            tf_file_path = f"{REPO_DIR}/terraform/{tf_file}"
            with open(tf_file_path, "r", encoding="utf-8") as f:
                tf_content = f.read()
                tf_resource_pattern = re.compile(
                    r'resource\s+"([^"]+)"\s+"([^"]+)"\s+\{'
                )
                logger.info(f"Identifying resource blocks in {tf_file_path}")
                for match in tf_resource_pattern.finditer(tf_content):
                    resource_type = match.group(1)
                    resource_name = match.group(2)
                    tf_resources.append(f"-target={resource_type}.{resource_name}")

                logger.info(f"Identifying module blocks in {tf_file_path}")
                tf_module_pattern = re.compile(r'module\s+"([^"]+)"\s+\{')
                for match in tf_module_pattern.finditer(tf_content):
                    module_name = match.group(1)
                    tf_resources.append(f"-target=module.{module_name}")

        except FileNotFoundError:
            logger.error(f"Error: File not found at {tf_file_path}")
            raise

    tf_target = " ".join(tf_resources)
    return tf_target


def get_repo_info(env: str) -> tuple[str, str]:
    """
    Get version and aws_profile
    :param env: Target env
    :return repo_version: Version number defined in config/info.yaml
    :return aws_profile: AWS profile defined in config/{env}.yaml
    """
    try:
        with open(f"{REPO_DIR}/config/info.yaml", "r", encoding="utf-8") as f:
            version_info = f.readline().strip()
            repo_version = version_info.rsplit(": ", 1)[1]
        logger.info(f"Current version: {repo_version}")
    except FileNotFoundError:
        logger.error(f"Error: File not found at {REPO_DIR}/config/info.yaml")
        raise

    try:
        with open(f"{REPO_DIR}/config/{env}.tfvars", "r", encoding="utf-8") as f:
            for line in f:
                match = re.match(r'^\s*aws_profile\s*=\s*"(.*)"', line)
                if match:
                    aws_profile = match.group(1)
                    logger.info(f"AWS profile: {aws_profile}")
                    break
    except FileNotFoundError:
        logger.error(f"Error: File not found at {REPO_DIR}/config/{env}.tfvars")
        raise
    return repo_version, aws_profile  # pylint: disable=E0606


def exec_tf_cmd(tf_cmd: str, aws_profile: str) -> None:
    """
    Function to run terraform command
    :param tf_cmd: Terraform command
    :param aws_profile: AWS profile for terraform to use
    """
    logger.info(f"Terraform command: {tf_cmd}")
    exec_cmd = f"""
    export AWS_PROFILE={aws_profile}
    {tf_cmd}
    """
    subprocess.run(exec_cmd, cwd=REPO_DIR, shell=True, check=True)


def main():
    """
    The main entry point for the script.
    """
    parser = argparse.ArgumentParser(
        description="This is a script to run terraform command against a specific file"
    )
    parser.add_argument(
        "--tf-files",
        type=str,
        required=True,
        help="Tf files to run terraform command against.",
    )
    parser.add_argument("--action", type=str, required=True, help="Terraform action")
    parser.add_argument("--env", type=str, required=True, help="Target ENV")
    parser.add_argument("--env-id", type=str, required=True, help="Target ENV_ID")
    args = parser.parse_args()

    version, aws_profile = get_repo_info(env=args.env)
    tf_target = construct_tf_target(tf_files=args.tf_files)
    tf_cmd = f"terraform -chdir=terraform {args.action} -var-file=../config/{args.env}.tfvars -var=env_id={args.env_id} -var=app_version={version} {tf_target}"
    exec_tf_cmd(tf_cmd=tf_cmd, aws_profile=aws_profile)


if __name__ == "__main__":
    main()
