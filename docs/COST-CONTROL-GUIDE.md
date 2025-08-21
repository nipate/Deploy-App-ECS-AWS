# 💰 Cost Control Strategy

## 🆓 **Keep Always (FREE Resources)**

Deploy once and keep running:

```bash
# Foundation (Always FREE)
aws cloudformation deploy --template-file infrastructure/cloudformation/vpc.yaml --stack-name taskmaster-dev-vpc --region us-east-1
aws cloudformation deploy --template-file infrastructure/cloudformation/iam-roles.yaml --stack-name taskmaster-dev-iam --region us-east-1 --capabilities CAPABILITY_NAMED_IAM
aws cloudformation deploy --template-file infrastructure/cloudformation/ecr.yaml --stack-name taskmaster-dev-ecr --region us-east-1
aws cloudformation deploy --template-file infrastructure/cloudformation/ecs-cluster.yaml --stack-name taskmaster-dev-cluster-free --region us-east-1
aws cloudformation deploy --template-file infrastructure/cloudformation/cognito.yaml --stack-name taskmaster-cognito --region us-east-1 --capabilities CAPABILITY_NAMED_IAM
aws cloudformation deploy --template-file infrastructure/cloudformation/dynamodb-multi-env.yaml --stack-name taskmaster-dev-dynamodb --region us-east-1 --parameter-overrides Environment=dev
aws cloudformation deploy --template-file infrastructure/cloudformation/dynamodb-multi-env.yaml --stack-name taskmaster-staging-dynamodb --region us-east-1 --parameter-overrides Environment=staging
```

**Cost**: $0/month permanently

## 💸 **Deploy/Delete Daily (PAID Resources)**

### **Morning: Start Demo**
```bash
# Deploy ALB (~$16/month - charges immediately)
aws cloudformation deploy --template-file infrastructure/cloudformation/alb.yaml --stack-name taskmaster-dev-alb --region us-east-1

# Deploy Application (Fargate ~$5/month - only when running)
aws cloudformation deploy --template-file infrastructure/environments/dev/app-stack.yaml --stack-name taskmaster-dev-app --region us-east-1 --capabilities CAPABILITY_IAM
```

### **Evening: Stop Charges**
```bash
# Delete Application (stops Fargate charges)
aws cloudformation delete-stack --stack-name taskmaster-dev-app

# Delete ALB (stops ALB charges)
aws cloudformation delete-stack --stack-name taskmaster-dev-alb
```

## 📊 **Cost Breakdown**

| Resource | Deploy Once | Deploy/Delete Daily |
|----------|-------------|-------------------|
| VPC | ✅ FREE | |
| IAM Roles | ✅ FREE | |
| ECR | ✅ FREE | |
| ECS Cluster | ✅ FREE | |
| Cognito User Pools | ✅ FREE (50K users) | |
| DynamoDB Tables | ✅ FREE (25GB) | |
| Security Groups | ✅ FREE | |
| ALB | | 💸 ~$16/month |
| ECS Fargate | | 💸 ~$5/month |

## 🎯 **Daily Workflow**

### **Demo Day**
1. Deploy paid resources (2 commands per environment)
2. Run your demo with authentication and database
3. Delete paid resources (2 commands per environment)
4. **Daily cost**: ~$0.70 (dev only) or ~$1.40 (dev + staging)

### **Non-Demo Days**
- Keep free resources running
- **Daily cost**: $0

## ⚡ **Quick Commands**

### **Start Demo**
```bash
# Start paid resources
aws cloudformation deploy --template-file infrastructure/cloudformation/alb.yaml --stack-name taskmaster-dev-alb --region us-east-1
aws cloudformation deploy --template-file infrastructure/environments/dev/app-stack.yaml --stack-name taskmaster-dev-app --region us-east-1 --capabilities CAPABILITY_IAM
```

### **Stop Demo**
```bash
# Stop paid resources
aws cloudformation delete-stack --stack-name taskmaster-dev-app
aws cloudformation delete-stack --stack-name taskmaster-dev-alb
```

## 🎯 **Multi-Environment Workflow**

### **Start Both Environments**
```bash
# Dev Environment
aws cloudformation deploy --template-file infrastructure/cloudformation/alb.yaml --stack-name taskmaster-dev-alb --region us-east-1
aws cloudformation deploy --template-file infrastructure/environments/dev/app-stack.yaml --stack-name taskmaster-dev-app --region us-east-1 --capabilities CAPABILITY_IAM

# Staging Environment
aws cloudformation deploy --template-file infrastructure/cloudformation/alb-staging.yaml --stack-name taskmaster-staging-alb --region us-east-1
aws cloudformation deploy --template-file infrastructure/environments/staging/app-stack.yaml --stack-name taskmaster-staging-app --region us-east-1 --capabilities CAPABILITY_IAM
```

### **Stop Both Environments**
```bash
# Delete All PAID Resources
aws cloudformation delete-stack --stack-name taskmaster-dev-app
aws cloudformation delete-stack --stack-name taskmaster-staging-app
aws cloudformation delete-stack --stack-name taskmaster-dev-alb
aws cloudformation delete-stack --stack-name taskmaster-staging-alb
```

## 💡 **Pro Tips**

1. **ALB takes ~2-3 minutes** to provision
2. **Fargate tasks start in ~30 seconds** after ALB is ready
3. **Deletion is faster** than creation (~1-2 minutes)
4. **Free resources** can stay up indefinitely
5. **ECR images** persist even when stacks are deleted
6. **Cognito users** persist across deployments
7. **DynamoDB data** persists across deployments
8. **Authentication works** immediately after deployment

This strategy gives you **maximum cost control** while maintaining demo readiness with full authentication and database!