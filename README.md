# Deploy-App-ECS-AWS - ECS Container POC

## 🎯 TaskMaster SaaS Platform
A complete multi-tenant task management application demonstrating modern AWS architecture patterns, cost optimization strategies, and real-world SaaS development workflows.

### **Business Context**
TaskMaster helps companies manage projects, assign tasks, and track team productivity through a web-based dashboard with real-time updates and analytics.

### **Technical Achievement**
Fully functional SaaS application with backend API, web frontend, automated CI/CD, and cost-optimized infrastructure that can be deployed/deleted daily for maximum cost control.

## Cost-Optimized Architecture
```
Internet → CloudFront (Free Tier) → ALB (Free Tier) → ECS on EC2 t3.micro
                                                        ↓
GitHub Actions (Free) → ECR (500MB Free) → ECS Deployment
                                                        ↓
Route53 (1 Zone Free) ← Certificate Manager (Free) ← Load Balancer
                                                        ↓
VPC (Single AZ) → Parameter Store (10K Free) + DynamoDB (25GB Free)
```

## 💰 Cost Breakdown by Service

| Service | Monthly Cost | Free Tier | Notes |
|---------|-------------|-----------|-------|
| **VPC** | $0 | ✅ Always Free | VPC, subnets, route tables, IGW |
| **IAM Roles** | $0 | ✅ Always Free | No charges for IAM roles/policies |
| **ECR** | $0 - $0.50 | ✅ 500MB Free | $0.10/GB after free tier |
| **ECS Fargate** | ~$5 | ❌ No Free Tier | 0.25 vCPU, 0.5GB RAM |
| **ALB** | ~$16 | ✅ 750hrs Free | $16.20/month + $0.008/LCU-hour |
| **CloudWatch Logs** | $0 - $1 | ✅ 5GB Free | $0.50/GB ingested after free tier |
| **Data Transfer** | $0 - $2 | ✅ 1GB Free | $0.09/GB after free tier |

**Total Estimated Cost: ~$8-13/month** (depending on usage)

## 🏗️ Infrastructure Components

### 1. VPC Network Architecture (vpc.yaml)
**Purpose**: Secure, isolated network for TaskMaster application

**Network Layout**:
```
TaskMaster VPC: 10.1.0.0/16
├── Public Subnets (ALB + ECS)
│   ├── 10.1.1.0/24 (AZ-1) - Load Balancer & ECS tasks
│   └── 10.1.2.0/24 (AZ-2) - Load Balancer & ECS tasks
└── Private Subnets (ECS with public routing)
    ├── 10.1.11.0/24 (AZ-1) - ECS tasks
    └── 10.1.12.0/24 (AZ-2) - ECS tasks
```

**Cost Optimization**: No NAT Gateway (~$32/month saved) - ECS tasks use public subnets with security group restrictions

### 2. IAM Security Roles (iam-roles.yaml)
**Purpose**: Secure access control for different components

#### 🔐 ECS Task Execution Role (`dev-ecs-task-execution-role`)
- **Used by**: ECS service during container startup
- **Permissions**: Pull Docker images, write logs, fetch secrets
- **When**: Container deployment and runtime management

#### 🔐 ECS Task Role (`dev-ecs-task-role`)
- **Used by**: Your running application code
- **Permissions**: Access Parameter Store, Secrets Manager
- **When**: App makes AWS API calls (database config, etc.)

#### 🔐 CodeBuild Service Role (`dev-codebuild-service-role`)
- **Used by**: CI/CD pipeline (GitHub Actions + CodeBuild)
- **Permissions**: Build Docker images, push to ECR, write logs
- **When**: Code deployment and image building

**Security Flow**:
```
1. Developer pushes code → GitHub Actions
2. CodeBuild (CodeBuildServiceRole) → Builds & pushes Docker image
3. ECS (TaskExecutionRole) → Pulls image & starts container
4. Running app (TaskRole) → Accesses AWS services
```

### 3. Core Services (Cost-Optimized)
- **ECS Fargate**: Container orchestration (0.25 vCPU, 0.5GB RAM) - ~$5/month
- **ECR**: Container registry (500MB free tier) - $0/month
- **ALB**: Load balancing (shared across services) - ~$16/month
- **CloudWatch**: Logging and monitoring (7-day retention) - ~$1/month
- **Parameter Store**: Configuration management (10K parameters free) - $0/month

### 4. CI/CD Pipeline
- **GitHub**: Repository hosting (free)
- **GitHub Actions**: Automated deployment (free for public repos)
- **CloudFormation**: Infrastructure as Code (free)
- **AWS CLI**: Service deployments (free)

## 📁 Project Structure
```
Deploy-App-ECS-AWS/
├── app/backend/                    # Flask API application
│   ├── app.py                      # Main API with CORS support
│   ├── Dockerfile                  # Container configuration
│   └── requirements.txt            # Python dependencies
├── infrastructure/dev/             # CloudFormation templates
│   └── dev-stack.yaml             # Application deployment
├── ecs-cluster-free.yaml          # FREE ECS resources
├── alb-paid.yaml                   # PAID ALB resources
├── codebuild-project.yaml          # CI/CD build project
├── start-build-cors.json           # Build script with CORS
├── demo-frontend.html              # Web dashboard
├── COST-CONTROL-GUIDE.md           # Daily workflow guide
├── USE-CASE-SCENARIO.md            # Business context
└── DEV-SETUP-GUIDE.md              # Setup instructions
```

## 🎓 **Learning Outcomes**

By completing this POC, you'll understand:

### **AWS Services Integration**
- **ECS Fargate**: Serverless container orchestration
- **Application Load Balancer**: Traffic distribution and health checks
- **ECR**: Container image registry and lifecycle management
- **CodeBuild**: Automated Docker image building
- **CloudFormation**: Infrastructure as Code
- **IAM**: Security roles and permissions
- **VPC**: Network isolation and security groups

### **DevOps Best Practices**
- **Cost Optimization**: Deploy/delete workflow saves 70% costs
- **Security**: Least privilege IAM roles, CORS configuration
- **Monitoring**: CloudWatch logs and health checks
- **CI/CD**: Automated builds and deployments
- **Infrastructure as Code**: Reproducible deployments

### **Real-World SaaS Architecture**
- **Multi-tenant design**: Company isolation patterns
- **API-first approach**: Backend services with frontend flexibility
- **Scalable infrastructure**: Auto-scaling and load balancing
- **Cost-effective development**: Optimize for demo and development workflows

## 🏆 **Success Metrics**

- ✅ **Full Stack Deployment**: Backend API + Frontend Dashboard
- ✅ **Cost Control**: Daily workflow saves ~$15/day when not in use
- ✅ **Real User Experience**: Web dashboard with live data
- ✅ **Production Patterns**: Proper security, monitoring, and CI/CD
- ✅ **AWS Integration**: 8+ services working together seamlessly

**Total Setup Time**: ~2 hours | **Daily Demo Time**: ~5 minutes | **Monthly Cost**: ~$8-13 (if running 24/7) or ~$0.70/day (demo mode)**

## 🚀 One-Time Setup (Deploy Once)

### Phase 1: Foundation Infrastructure (FREE - Keep Running)
```bash
# 1. Deploy VPC (Network foundation) - Cost: $0/month
aws cloudformation deploy --template-file vpc.yaml --stack-name taskmaster-dev-vpc --region us-east-1

# 2. Deploy IAM Roles (Security foundation) - Cost: $0/month
aws cloudformation deploy --template-file iam-roles.yaml --stack-name taskmaster-dev-iam --region us-east-1 --capabilities CAPABILITY_NAMED_IAM

# 3. Deploy ECR Repository (Container registry) - Cost: $0/month (500MB free)
aws cloudformation deploy --template-file ecr.yaml --stack-name taskmaster-dev-ecr --region us-east-1

# 4. Deploy FREE ECS Resources - Cost: $0/month
aws cloudformation deploy --template-file ecs-cluster-free.yaml --stack-name taskmaster-dev-cluster-free --region us-east-1

# 5. Deploy CodeBuild Project - Cost: $0/month (pay per build)
aws cloudformation deploy --template-file codebuild-project.yaml --stack-name taskmaster-dev-codebuild --region us-east-1

# 6. Build Docker Image with CORS Support
aws codebuild start-build --cli-input-json file://start-build-cors.json
```

## 💰 Daily Demo Workflow (Cost Control)

### 🌅 **Start Demo Day** (~$0.70/day)
```bash
# Deploy ALB (Load Balancer) - Cost: ~$16/month
aws cloudformation deploy --template-file alb-paid.yaml --stack-name taskmaster-dev-alb --region us-east-1

# Deploy Application (ECS Fargate) - Cost: ~$5/month
aws cloudformation deploy --template-file infrastructure/dev/dev-stack.yaml --stack-name taskmaster-dev-app --region us-east-1 --capabilities CAPABILITY_IAM

# Wait 3-5 minutes for deployment, then test
curl http://ALB_DNS_NAME/health
```

### 🌐 **Access TaskMaster Dashboard**
```bash
# Start local web server
python -m http.server 8000

# Open browser to: http://localhost:8000/demo-frontend.html
# Enter ALB DNS when prompted (without http://)
```

### 🌙 **End Demo Day** (Stop All Charges)
```bash
# Delete Application Stack (stops Fargate charges)
aws cloudformation delete-stack --stack-name taskmaster-dev-app

# Delete ALB Stack (stops ALB charges)
aws cloudformation delete-stack --stack-name taskmaster-dev-alb

# Verify deletion (should show DELETE_COMPLETE)
aws cloudformation describe-stacks --stack-name taskmaster-dev-app --query "Stacks[0].StackStatus"
aws cloudformation describe-stacks --stack-name taskmaster-dev-alb --query "Stacks[0].StackStatus"
```

## 🎯 **TaskMaster Features Demo**

### **API Endpoints**
- **Health Check**: `http://ALB_DNS_NAME/health`
- **Projects**: `http://ALB_DNS_NAME/api/projects`
- **Tasks**: `http://ALB_DNS_NAME/api/tasks`
- **Filtered Tasks**: `http://ALB_DNS_NAME/api/tasks?project_id=1`

### **Dashboard Features**
- ✅ **System Health**: Real-time status monitoring
- ✅ **Project Management**: Website Redesign, Mobile App Development
- ✅ **Task Tracking**: Design mockups, Implementation progress
- ✅ **Team Assignments**: Lisa, Mike with status updates
- ✅ **Responsive Design**: Works on desktop, tablet, mobile

## 🔧 **Troubleshooting**

### **Get ALB DNS Name**
```bash
aws cloudformation describe-stacks --stack-name taskmaster-dev-alb --query "Stacks[0].Outputs[?OutputKey=='ALBDNSName'].OutputValue" --output text
```

### **Check Service Status**
```bash
aws ecs describe-services --cluster dev-cluster --services taskmaster-backend-dev --query "services[0].{running:runningCount,desired:desiredCount}"
```

### **View Application Logs**
```bash
aws logs tail /ecs/taskmaster-backend-dev --follow
```

### **Rebuild Application (if needed)**
```bash
aws codebuild start-build --cli-input-json file://start-build-cors.json
# Wait for build completion, then force ECS deployment
aws ecs update-service --cluster dev-cluster --service taskmaster-backend-dev --force-new-deployment
```


TaskMaster POC - Step-by-Step Execution Plan
Phase 1: Infrastructure Setup (30 minutes)
Step 1: Deploy VPC Foundation
aws cloudformation deploy \
  --template-file vpc.yaml \
  --stack-name taskmaster-dev-vpc \
  --region us-east-1

Copy
bash
Step 2: Deploy IAM Roles
aws cloudformation deploy \
  --template-file iam-roles.yaml \
  --stack-name taskmaster-dev-iam \
  --region us-east-1 \
  --capabilities CAPABILITY_IAM

Copy
bash
Step 3: Deploy ECR Repository
aws cloudformation deploy \
  --template-file ecr.yaml \
  --stack-name taskmaster-dev-ecr \
  --region us-east-1

Copy
bash
Step 4: Deploy ECS Cluster
aws cloudformation deploy \
  --template-file ecs-cluster.yaml \
  --stack-name taskmaster-dev-cluster \
  --region us-east-1 \
  --capabilities CAPABILITY_IAM

Copy
bash
Phase 2: Application Deployment (20 minutes)
Step 5: Build and Push Docker Image
cd app/backend
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
docker build -t taskmaster-backend .
docker tag taskmaster-backend:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/taskmaster-backend:latest
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/taskmaster-backend:latest

Copy
bash
Step 6: Deploy Application Stack
aws cloudformation deploy \
  --template-file infrastructure/dev/dev-stack.yaml \
  --stack-name taskmaster-dev-app \
  --region us-east-1 \
  --capabilities CAPABILITY_IAM

Copy
bash
Phase 3: Testing & Validation (10 minutes)
Step 7: Test Application Endpoints
# Get ALB DNS name
aws elbv2 describe-load-balancers --query 'LoadBalancers[0].DNSName' --output text

# Test endpoints
curl http://ALB_DNS_NAME/health
curl http://ALB_DNS_NAME/api/projects
curl http://ALB_DNS_NAME/api/tasks

Copy
bash
Step 8: Verify ECS Service
aws ecs describe-services --cluster taskmaster-dev --services taskmaster-backend-dev
aws logs tail /ecs/taskmaster-backend-dev --follow

Copy
bash
Phase 4: CI/CD Setup (15 minutes)
Step 9: Configure GitHub Secrets
AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

Step 10: Test Automated Deployment
git checkout -b dev
git push origin dev
# GitHub Actions will automatically deploy

Copy
bash
Total Execution Time: ~75 minutes
Prerequisites Checklist:
 AWS CLI configured
 Docker installed
 GitHub repository access
 Replace ACCOUNT_ID in commands with actual AWS account ID
Success Criteria:
 All CloudFormation stacks deployed successfully
 ECS service running with 1 healthy task
 API endpoints responding with 200 status
 GitHub Actions pipeline working
 Application accessible via ALB