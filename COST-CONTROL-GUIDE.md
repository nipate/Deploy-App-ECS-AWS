# 💰 Cost Control Strategy

## 🆓 **Keep Always (FREE Resources)**

Deploy once and keep running:

```bash
# Foundation (Always FREE)
aws cloudformation deploy --template-file vpc.yaml --stack-name taskmaster-dev-vpc --region us-east-1
aws cloudformation deploy --template-file iam-roles.yaml --stack-name taskmaster-dev-iam --region us-east-1 --capabilities CAPABILITY_NAMED_IAM
aws cloudformation deploy --template-file ecr.yaml --stack-name taskmaster-dev-ecr --region us-east-1
aws cloudformation deploy --template-file ecs-cluster-free.yaml --stack-name taskmaster-dev-cluster-free --region us-east-1
```

**Cost**: $0/month permanently

## 💸 **Deploy/Delete Daily (PAID Resources)**

### **Morning: Start Demo**
```bash
# Deploy ALB (~$16/month - charges immediately)
aws cloudformation deploy --template-file alb-paid.yaml --stack-name taskmaster-dev-alb --region us-east-1

# Deploy Application (Fargate ~$5/month - only when running)
aws cloudformation deploy --template-file infrastructure/dev/dev-stack.yaml --stack-name taskmaster-dev-app --region us-east-1 --capabilities CAPABILITY_IAM
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
| Security Groups | ✅ FREE | |
| ALB | | 💸 ~$16/month |
| ECS Fargate | | 💸 ~$5/month |

## 🎯 **Daily Workflow**

### **Demo Day**
1. Deploy paid resources (2 commands)
2. Run your demo
3. Delete paid resources (2 commands)
4. **Daily cost**: ~$0.70 (if running 8 hours)

### **Non-Demo Days**
- Keep free resources running
- **Daily cost**: $0

## ⚡ **Quick Commands**

### **Start Demo**
```bash
# Start paid resources
aws cloudformation deploy --template-file alb-paid.yaml --stack-name taskmaster-dev-alb --region us-east-1
aws cloudformation deploy --template-file infrastructure/dev/dev-stack.yaml --stack-name taskmaster-dev-app --region us-east-1 --capabilities CAPABILITY_IAM
```

### **Stop Demo**
```bash
# Stop paid resources
aws cloudformation delete-stack --stack-name taskmaster-dev-app
aws cloudformation delete-stack --stack-name taskmaster-dev-alb
```

## 💡 **Pro Tips**

1. **ALB takes ~2-3 minutes** to provision
2. **Fargate tasks start in ~30 seconds** after ALB is ready
3. **Deletion is faster** than creation (~1-2 minutes)
4. **Free resources** can stay up indefinitely
5. **ECR images** persist even when stacks are deleted

This strategy gives you **maximum cost control** while maintaining demo readiness!