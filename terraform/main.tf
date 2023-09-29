provider "aws" {
  region = "us-east-2" # Change to your preferred AWS region
}

module "eks_cluster" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "my-eks-cluster"
  cluster_version = "1.21"
  subnets         = ["subnet-019704555729f17b6", "subnet-0e4a3d27b5ead3ed2","subnet-0094fa87353eb25a7"] # Specify your subnets
  vpc_id          = "vpc-092d195c361c950d6" # Specify your VPC ID
  worker_groups = {
    eks_nodes = {
      desired_capacity = 2
      max_capacity     = 3
      min_capacity     = 1
    }
  }
}

# Output variables
output "eks_cluster_endpoint" {
  value = module.eks_cluster.cluster_endpoint
}

output "eks_cluster_security_group_ids" {
  value = module.eks_cluster.cluster_security_group_ids
}
