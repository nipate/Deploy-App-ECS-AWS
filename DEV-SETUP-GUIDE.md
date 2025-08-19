# TaskMaster Dev Environment Setup Guide

## 🚀 Quick Start

### Prerequisites
- AWS CLI configured with dev account credentials
- Docker installed locally
- GitHub repository access

### 1. Deploy Infrastructure (One-time setup)

```bash
# Deploy VPC and base infrastructure
aws cloudformation deploy \
  --template-file vpc.yaml \
  --stack-name taskmaster-dev-vpc \
  --region us-east-1

# Deploy ECS cluster
aws cloudformation deploy \
  --template-file ecs-cluster.yaml \
  --stack-name taskmaster-dev-cluster \
  --region us-east-1 \
  --capabilities CAPABILITY_IAM

# Deploy application stack
aws cloudformation deploy \
  --template-file infrastructure/dev/dev-stack.yaml \
  --stack-name taskmaster-dev-app \
  --region us-east-1 \
  --capabilities CAPABILITY_IAM
```

### 2. Test Locally

```bash
# Build and run the backend locally
cd app/backend
docker build -t taskmaster-backend .
docker run -p 5000:5000 taskmaster-backend

# Test endpoints
curl http://localhost:5000/health
curl http://localhost:5000/api/projects
```

### 3. Deploy to AWS

```bash
# Get ECR login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Tag and push image
docker tag taskmaster-backend:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/taskmaster-backend:latest
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/taskmaster-backend:latest

# Update ECS service
aws ecs update-service \
  --cluster taskmaster-dev \
  --service taskmaster-backend-dev \
  --force-new-deployment
```

## 🔧 Development Workflow

### Daily Development
1. Make code changes in `app/backend/`
2. Test locally with Docker
3. Push to `dev` branch
4. GitHub Actions automatically deploys to dev environment
5. Test deployed application via ALB endpoint

### Key Endpoints
- **Health Check**: `https://dev-alb-url.com/health`
- **Projects API**: `https://dev-alb-url.com/api/projects`
- **Tasks API**: `https://dev-alb-url.com/api/tasks`

### Monitoring & Debugging
- **CloudWatch Logs**: `/ecs/taskmaster-backend-dev`
- **ECS Console**: Monitor service health and tasks
- **ALB Target Groups**: Check health check status

## 📊 Cost Optimization (Dev Environment)

### Current Configuration
- **ECS Fargate**: 0.25 vCPU, 0.5 GB RAM
- **ALB**: Shared across services
- **ECR**: 500MB free tier
- **CloudWatch**: 7-day log retention

### Estimated Monthly Cost: ~$8
- ECS Fargate: ~$5
- ALB: ~$2 (shared)
- Data transfer: ~$1

### Cost-Saving Tips
- Use spot instances for non-critical testing
- Set up auto-scaling to scale down during off-hours
- Clean up old ECR images automatically
- Use shorter log retention periods

## 🔍 Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check ECS service events
aws ecs describe-services --cluster taskmaster-dev --services taskmaster-backend-dev

# Check task logs
aws logs tail /ecs/taskmaster-backend-dev --follow
```

#### Image Push Fails
```bash
# Verify ECR repository exists
aws ecr describe-repositories --repository-names taskmaster-backend

# Check Docker login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

#### Health Check Failing
- Verify container port 5000 is exposed
- Check security group allows ALB traffic
- Ensure health check endpoint `/health` returns 200

## 🎯 Next Steps

### Phase 1: Basic Functionality ✅
- [x] Container deployment
- [x] Basic API endpoints
- [x] Health checks
- [x] CI/CD pipeline

### Phase 2: Database Integration
- [ ] DynamoDB tables for projects/tasks
- [ ] Parameter Store for configuration
- [ ] Real data persistence

### Phase 3: Advanced Features
- [ ] User authentication (Cognito)
- [ ] File uploads (S3)
- [ ] Real-time notifications (SNS/SQS)
- [ ] Analytics dashboard

### Phase 4: Production Readiness
- [ ] Multi-AZ deployment
- [ ] Auto-scaling policies
- [ ] Monitoring and alerting
- [ ] Security hardening

## 📚 Learning Resources

- [ECS Developer Guide](https://docs.aws.amazon.com/ecs/)
- [Fargate Pricing](https://aws.amazon.com/fargate/pricing/)
- [CloudFormation Templates](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
- [GitHub Actions for AWS](https://github.com/aws-actions)