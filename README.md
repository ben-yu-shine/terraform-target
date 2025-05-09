# terraform-target
 
A command-line utility to simplify running Terraform commands against a single Terraform configuration file within a larger project. This helps in isolating changes and reducing the risk of unintended modifications to other resources.
 
## Table of Contents
 
- [Purpose](#purpose)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
 
## Purpose
 
When working with large Terraform projects, you might want to apply or plan changes for resources defined in a specific file without affecting or processing the entire configuration. `terraform-target` allows you to do just that by intelligently identifying resources within the specified file and using Terraform's `-target` option.
 
This tool is particularly useful for:
* Making granular changes in a complex environment.
* Refactoring parts of your infrastructure piece by piece.
* Speeding up development workflows by focusing only on relevant resources.
* Applying hotfixes to specific resources.
 
## Prerequisites
 
* **Terraform:** Must be installed and configured in your system's PATH. (Typically version 0.12+ for `-target` to work reliably with modules, though core functionality is older).
* **Understanding of Terraform's `-target` option:** While this tool simplifies its usage, knowing the implications and potential pitfalls of `-target` is crucial. (See [Terraform's official documentation on `-target`](https://developer.hashicorp.com/terraform/cli/commands/plan#resource-targeting)).
* **Python virtual environment:** Building and installing `terraform-target` depends on pipenv. (See [Pipenv installatrion guild](https://pipenv.pypa.io/en/latest/installation.html#))
 
## Installation
 
**Installation**
 
Download or clone the `terraform-target` script/repository.
```bash
make build-venv
make install
```
 
**Uninstallation**
```bash
make uninstall
```
 
Ensure the `terraform-target` executable or script is in your system's PATH.
 
## Usage
 
Run below command in terraform project repo:
 
```bash
terraform-target --tf-file <file_name.tf> --action <plan/apply/destroy> --env <ENV> --env-id <ENV_ID>