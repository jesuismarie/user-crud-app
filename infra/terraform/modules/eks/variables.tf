variable "project_name" {
  description = "Name of the project (used for resource naming and tagging)"
  type        = string
}

variable "environment" {
  description = "Environment name (e.g. dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string

  validation {
    condition     = can(regex("^[a-zA-Z][a-zA-Z0-9-]{0,98}[a-zA-Z0-9]$", var.cluster_name))
    error_message = "cluster_name must start with a letter and contain only alphanumeric characters and hyphens."
  }
}

variable "cluster_version" {
  description = "Kubernetes version for the EKS cluster"
  type        = string
  default     = "1.36"

  validation {
    condition     = can(regex("^1\\.(2[8-9]|3[0-7])$", var.cluster_version))
    error_message = "cluster_version must be a supported EKS version (e.g. 1.28, 1.29, 1.30, 1.31, 1.32, 1.33, 1.34, 1.35, 1.36, 1.37)."
  }
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs for the worker nodes"
  type        = list(string)
}

variable "public_subnet_ids" {
  description = "List of public subnet IDs (used for control plane ENIs when public endpoint is enabled)"
  type        = list(string)
  default     = []
}

variable "public_access_cidrs" {
  description = "List of CIDR blocks that can access the public API endpoint"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "node_instance_types" {
  description = "List of instance types for the managed node group"
  type        = list(string)
  default     = ["t3.small"]

  validation {
    condition     = length(var.node_instance_types) >= 1
    error_message = "At least one instance type must be specified."
  }
}

variable "node_ami_type" {
  description = "EKS managed node group AMI type"
  type        = string
  default     = "AL2023_x86_64_STANDARD"

  validation {
    condition = contains([
      "AL2_x86_64",
      "AL2_x86_64_GPU",
      "AL2_ARM_64",
      "AL2023_x86_64_STANDARD",
      "AL2023_ARM_64_STANDARD",
      "AL2023_x86_64_NVIDIA",
      "BOTTLEROCKET_x86_64",
      "BOTTLEROCKET_ARM_64",
    ], var.node_ami_type)
    error_message = "node_ami_type must be a valid EKS AMI type (e.g. AL2023_x86_64_STANDARD, AL2_x86_64)."
  }
}

variable "node_desired_size" {
  description = "Desired number of worker nodes"
  type        = number
  default     = 2

  validation {
    condition     = var.node_desired_size >= 1 && var.node_desired_size <= 10
    error_message = "node_desired_size must be between 1 and 10."
  }
}

variable "node_min_size" {
  description = "Minimum number of worker nodes"
  type        = number
  default     = 1

  validation {
    condition     = var.node_min_size >= 1 && var.node_min_size <= 10
    error_message = "node_min_size must be between 1 and 10."
  }
}

variable "node_max_size" {
  description = "Maximum number of worker nodes"
  type        = number
  default     = 3

  validation {
    condition     = var.node_max_size >= 1 && var.node_max_size <= 10
    error_message = "node_max_size must be between 1 and 10."
  }
}

variable "node_disk_size" {
  description = "Disk size in GiB for worker nodes"
  type        = number
  default     = 20

  validation {
    condition     = var.node_disk_size >= 20 && var.node_disk_size <= 100
    error_message = "node_disk_size must be between 20 and 100 GiB."
  }
}

variable "eks_security_group_id" {
  description = "The ID of the security group to associate with the EKS cluster"
  type        = string
  default     = null
}

variable "eks_nodes_security_group_id" {
  description = "SG attached to worker nodes via launch template"
  type        = string
}

variable "tags" {
  description = "Tags applied to all resources"
  type        = map(string)
  default     = {}
}
