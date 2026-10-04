output "account_id" {
  description = "AWS account ID this infrastructure is deployed into"
  value       = data.aws_caller_identity.current.account_id
}

output "aws_region" {
  description = "AWS region of the cluster (needed by the AWS Load Balancer Controller chart)"
  value       = var.aws_region
}

output "cluster_name" {
  description = "Name of the EKS cluster"
  value       = module.eks.cluster_name
}

output "kubeconfig_command" {
  description = "Command to configure kubectl for this cluster"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${module.eks.cluster_name}"
}

output "nat_public_ips" {
  description = "Public IPs of the NAT Gateway(s), useful for allowlisting outbound traffic"
  value       = module.vpc.nat_public_ips
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "aws_lb_controller_role_arn" {
  description = "IAM role ARN for the AWS Load Balancer Controller ServiceAccount annotation"
  value       = module.aws_lb_controller_irsa.role_arn
}

output "ebs_csi_role_arn" {
  description = "IAM role ARN for the EBS CSI driver ServiceAccount annotation"
  value       = module.ebs_csi_irsa.role_arn
}

output "ecr_repository_url" {
  description = "ECR repository URL for the app image, used by CI to push and by the Helm chart as image.repository"
  value       = aws_ecr_repository.container_registry.repository_url
}