variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"

  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-[0-9]$", var.aws_region))
    error_message = "aws_region must be a valid AWS region format (e.g. eu-central-1, us-east-1)."
  }
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "user-crud-app"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{1,30}[a-z0-9]$", var.project_name))
    error_message = "project_name must be 3-32 chars, lowercase letters, numbers, hyphens, start with a letter."
  }
}

variable "environment" {
  description = "Environment name (dev, staging or prod)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be one of: dev, staging, prod."
  }
}

# VPC
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "azs" {
  description = "Availability zones (must belong to aws_region)"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24"]
}

variable "single_nat_gateway" {
  description = "Use a single NAT Gateway (cheaper for non-production)"
  type        = bool
  default     = true
}

# EKS
variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "user-crud-eks"
}

variable "cluster_version" {
  description = "Kubernetes version of the EKS cluster"
  type        = string
  default     = "1.36"
}

variable "node_instance_types" {
  description = "EC2 instance types for the node group"
  type        = list(string)
  default     = ["t3.small"]
}

variable "node_ami_type" {
  description = "EKS managed node group AMI type"
  type        = string
  default     = "AL2023_x86_64_STANDARD"
}

variable "node_desired_size" {
  description = "Desired number of worker nodes"
  type        = number
  default     = 3
}

variable "node_min_size" {
  description = "Minimum number of worker nodes"
  type        = number
  default     = 2
}

variable "node_max_size" {
  description = "Maximum number of worker nodes"
  type        = number
  default     = 4
}

variable "node_disk_size" {
  description = "Disk size in GiB for worker nodes"
  type        = number
  default     = 20
}

# ALB
variable "lb_controller_service_account" {
  description = "Name of the Kubernetes ServiceAccount used by the AWS Load Balancer Controller (in kube-system)"
  type        = string
  default     = "aws-load-balancer-controller"
}

# EBS
variable "ebs_controller_service_account" {
  description = "Name of the Kubernetes ServiceAccount used by the EBS CSI Controller (in kube-system)"
  type        = string
  default     = "ebs-csi-controller-sa"
}
