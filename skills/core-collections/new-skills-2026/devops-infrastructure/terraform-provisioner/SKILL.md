---
name: terraform-provisioner
description: Provision and manage infrastructure as code with Terraform — cloud resources, modules, state management, and automated deployments. Use when creating cloud infrastructure, managing multi-cloud deployments, refactoring infrastructure code, planning infrastructure changes, or migrating to Infrastructure as Code.
---

# terraform-provisioner

Provision, manage, and version infrastructure using Terraform with best practices.

## When to Use

Invoke this skill when you need to:
- **Provision** cloud infrastructure across AWS, Azure, GCP, or multi-cloud
- **Create reusable** Terraform modules
- **Manage** Terraform state and backends
- **Plan and apply** infrastructure changes safely
- **Import** existing infrastructure into Terraform
- **Refactor** infrastructure code for maintainability
- **Set up** CI/CD for infrastructure deployment
- **Troubleshoot** Terraform errors and state issues

## Quick Start

### Basic AWS Infrastructure

```hcl
# main.tf
terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "production/infrastructure.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = var.project_name
    }
  }
}

# VPC Module
module "vpc" {
  source = "./modules/vpc"
  
  vpc_cidr            = var.vpc_cidr
  availability_zones  = var.availability_zones
  environment         = var.environment
  enable_nat_gateway  = true
  enable_vpn_gateway  = false
}

# EKS Cluster
module "eks" {
  source = "./modules/eks"
  
  cluster_name    = "${var.project_name}-${var.environment}"
  cluster_version = "1.28"
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnet_ids
  
  node_groups = {
    general = {
      desired_size = 3
      min_size     = 2
      max_size     = 10
      
      instance_types = ["t3.large"]
      capacity_type  = "ON_DEMAND"
      
      labels = {
        role = "general"
      }
    }
  }
}

# RDS Database
resource "aws_db_instance" "main" {
  identifier     = "${var.project_name}-${var.environment}-db"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = var.db_instance_class
  
  allocated_storage     = 100
  max_allocated_storage = 500
  storage_encrypted     = true
  
  db_name  = var.db_name
  username = var.db_username
  password = random_password.db_password.result
  
  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "mon:04:00-mon:05:00"
  
  skip_final_snapshot = false
  final_snapshot_identifier = "${var.project_name}-${var.environment}-db-final-snapshot"
  
  tags = {
    Name = "${var.project_name}-${var.environment}-db"
  }
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret" "db_password" {
  name = "${var.project_name}/${var.environment}/db/password"
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db_password.result
}
```

### Variables File

```hcl
# variables.tf
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.large"
}

variable "db_name" {
  description = "Database name"
  type        = string
}

variable "db_username" {
  description = "Database master username"
  type        = string
  default     = "dbadmin"
  sensitive   = true
}
```

### Outputs File

```hcl
# outputs.tf
output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
  sensitive   = true
}

output "eks_cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "rds_password_secret_arn" {
  description = "ARN of the secret containing RDS password"
  value       = aws_secretsmanager_secret.db_password.arn
}
```

## Common Scenarios

### Scenario 1: Reusable VPC Module

```hcl
# modules/vpc/main.tf
variable "vpc_cidr" {
  type = string
}

variable "environment" {
  type = string
}

variable "availability_zones" {
  type = list(string)
}

variable "enable_nat_gateway" {
  type    = bool
  default = true
}

locals {
  public_subnets  = [for i, az in var.availability_zones : cidrsubnet(var.vpc_cidr, 8, i)]
  private_subnets = [for i, az in var.availability_zones : cidrsubnet(var.vpc_cidr, 8, i + 10)]
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.environment}-vpc"
  }
}

resource "aws_subnet" "public" {
  count = length(var.availability_zones)
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = local.public_subnets[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${var.environment}-public-${var.availability_zones[count.index]}"
    "kubernetes.io/role/elb" = "1"
  }
}

resource "aws_subnet" "private" {
  count = length(var.availability_zones)
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = local.private_subnets[count.index]
  availability_zone = var.availability_zones[count.index]
  
  tags = {
    Name = "${var.environment}-private-${var.availability_zones[count.index]}"
    "kubernetes.io/role/internal-elb" = "1"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${var.environment}-igw"
  }
}

resource "aws_eip" "nat" {
  count  = var.enable_nat_gateway ? length(var.availability_zones) : 0
  domain = "vpc"
  
  tags = {
    Name = "${var.environment}-nat-eip-${var.availability_zones[count.index]}"
  }
}

resource "aws_nat_gateway" "main" {
  count = var.enable_nat_gateway ? length(var.availability_zones) : 0
  
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
  
  tags = {
    Name = "${var.environment}-nat-${var.availability_zones[count.index]}"
  }
  
  depends_on = [aws_internet_gateway.main]
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "${var.environment}-public-rt"
  }
}

resource "aws_route_table" "private" {
  count  = length(var.availability_zones)
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = var.enable_nat_gateway ? aws_nat_gateway.main[count.index].id : null
  }
  
  tags = {
    Name = "${var.environment}-private-rt-${var.availability_zones[count.index]}"
  }
}

resource "aws_route_table_association" "public" {
  count          = length(var.availability_zones)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count          = length(var.availability_zones)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# outputs.tf
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}
```

### Scenario 2: Multi-Environment Setup

```hcl
# environments/dev/terraform.tfvars
environment         = "dev"
project_name        = "myapp"
aws_region          = "us-east-1"
vpc_cidr            = "10.0.0.0/16"
availability_zones  = ["us-east-1a", "us-east-1b"]
db_instance_class   = "db.t3.small"
db_name             = "myappdb"

# environments/production/terraform.tfvars
environment         = "production"
project_name        = "myapp"
aws_region          = "us-east-1"
vpc_cidr            = "10.1.0.0/16"
availability_zones  = ["us-east-1a", "us-east-1b", "us-east-1c"]
db_instance_class   = "db.r6g.xlarge"
db_name             = "myappdb"
```

### Scenario 3: Remote State Management

```hcl
# bootstrap/main.tf - Create S3 bucket and DynamoDB for state
terraform {
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "mycompany-terraform-state"
  
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  
  attribute {
    name = "LockID"
    type = "S"
  }
  
  lifecycle {
    prevent_destroy = true
  }
}
```

### Scenario 4: Data Sources and Lookups

```hcl
# Use existing resources
data "aws_caller_identity" "current" {}

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]
  
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
  
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

data "aws_secretsmanager_secret_version" "api_key" {
  secret_id = "third-party/api-key"
}

locals {
  api_key = jsondecode(data.aws_secretsmanager_secret_version.api_key.secret_string)
}
```

## Best Practices

### State Management
- **Always** use remote state (S3, Terraform Cloud, etc.)
- **Enable** state locking with DynamoDB
- **Never** commit state files to version control
- Use **workspaces** for multiple environments cautiously
- Implement **state file encryption**

### Code Organization
- Use **modules** for reusable components
- Keep **environments** in separate directories or workspaces
- Follow **naming conventions** consistently
- Group related resources in separate files
- Use **locals** for computed values and DRY principle

### Security
- **Never** hardcode secrets in code
- Use **AWS Secrets Manager** or **Parameter Store**
- Mark sensitive outputs with `sensitive = true`
- Implement **least privilege** IAM policies
- Enable **encryption** at rest and in transit
- Use **private subnets** for internal resources

### Version Control
- Pin **provider versions** to avoid breaking changes
- Use **semantic versioning** for modules
- Tag **releases** for production deployments
- Include **.gitignore** for Terraform files
- Document **breaking changes** in CHANGELOG

### Testing
- Use `terraform plan` before applying
- Implement **automated validation** in CI/CD
- Use **terraform validate** and **terraform fmt**
- Consider **Terratest** for integration testing
- Test modules independently

## Troubleshooting

### State Lock Issues

```bash
# View current locks
aws dynamodb scan --table-name terraform-locks

# Force unlock (use with caution)
terraform force-unlock <lock-id>
```

### Import Existing Resources

```bash
# Import EC2 instance
terraform import aws_instance.example i-1234567890abcdef

# Import S3 bucket
terraform import aws_s3_bucket.example my-bucket-name

# Generate import block (Terraform 1.5+)
terraform plan -generate-config-out=imported.tf
```

### Debugging

```bash
# Enable detailed logging
export TF_LOG=DEBUG
export TF_LOG_PATH=terraform.log

# Trace provider issues
export TF_LOG_PROVIDER=TRACE

# Validate configuration
terraform validate

# Format code
terraform fmt -recursive

# Check for security issues
tfsec .
checkov -d .
```

### Common Errors

**Error: Cycle in dependencies**
- Break circular references
- Use `depends_on` explicitly
- Reorganize resource dependencies

**Error: Provider configuration not present**
- Ensure provider is configured in modules
- Pass provider explicitly to modules if needed

**Error: Resource already exists**
- Import existing resource
- Or rename Terraform resource

## Advanced Patterns

### Conditional Resources

```hcl
resource "aws_instance" "optional" {
  count = var.enable_instance ? 1 : 0
  
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.micro"
}

# Access with:
# aws_instance.optional[0]
```

### Dynamic Blocks

```hcl
resource "aws_security_group" "main" {
  name        = "main-sg"
  description = "Main security group"
  vpc_id      = aws_vpc.main.id
  
  dynamic "ingress" {
    for_each = var.ingress_rules
    
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
      description = ingress.value.description
    }
  }
}
```

### Workspaces

```bash
# Create workspace
terraform workspace new production
terraform workspace new staging

# List workspaces
terraform workspace list

# Switch workspace
terraform workspace select production

# Use in code
resource "aws_instance" "example" {
  tags = {
    Environment = terraform.workspace
  }
}
```

### Terraform Cloud Integration

```hcl
terraform {
  cloud {
    organization = "mycompany"
    
    workspaces {
      name = "production-infrastructure"
    }
  }
}
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
name: Terraform

on:
  pull_request:
    paths:
      - 'terraform/**'
  push:
    branches:
      - main
    paths:
      - 'terraform/**'

env:
  TF_VERSION: '1.5.0'

jobs:
  terraform:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: terraform
    
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: ${{ env.TF_VERSION }}
      
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1
      
      - name: Terraform Format
        run: terraform fmt -check -recursive
      
      - name: Terraform Init
        run: terraform init
      
      - name: Terraform Validate
        run: terraform validate
      
      - name: Terraform Plan
        run: terraform plan -no-color
        continue-on-error: true
      
      - name: Security Scan
        uses: aquasecurity/tfsec-action@v1.0.0
      
      - name: Terraform Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply -auto-approve
```

## Useful Commands

```bash
# Initialize working directory
terraform init
terraform init -upgrade  # Upgrade providers

# Plan changes
terraform plan
terraform plan -out=tfplan
terraform plan -target=aws_instance.example

# Apply changes
terraform apply
terraform apply tfplan
terraform apply -auto-approve

# Destroy infrastructure
terraform destroy
terraform destroy -target=aws_instance.example

# Show current state
terraform show
terraform state list
terraform state show aws_instance.example

# Move resources
terraform state mv aws_instance.old aws_instance.new

# Remove from state
terraform state rm aws_instance.example

# Refresh state
terraform refresh

# Output values
terraform output
terraform output -json

# Validate configuration
terraform validate

# Format code
terraform fmt
terraform fmt -recursive

# Create workspace
terraform workspace new dev

# Import resource
terraform import aws_instance.example i-1234567890abcdef

# Taint resource (mark for recreation)
terraform taint aws_instance.example
terraform untaint aws_instance.example

# Graph dependencies
terraform graph | dot -Tsvg > graph.svg

# Console (test expressions)
terraform console
```

## Related Skills

- **ansible-automator**: Configuration management on provisioned infrastructure
- **kubernetes-orchestrator**: Deploy K8s clusters provisioned by Terraform
- **cloud-migration-planner**: Plan infrastructure migration strategies
- **infrastructure-cost-optimizer**: Optimize cloud costs
- **secrets-manager**: Manage secrets for Terraform
- **gitops-deployer**: Automate Terraform with GitOps
- **disaster-recovery-planner**: Plan DR for Terraform-managed infrastructure

## References

- [Terraform Documentation](https://www.terraform.io/docs)
- [Terraform Registry](https://registry.terraform.io/)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Azure Provider Docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [GCP Provider Docs](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
