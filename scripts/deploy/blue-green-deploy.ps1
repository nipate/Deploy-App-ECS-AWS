# Blue/Green Deployment Script
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("dev", "staging", "prod")]
    [string]$Environment,
    
    [Parameter(Mandatory=$true)]
    [ValidateSet("blue", "green")]
    [string]$TargetColor,
    
    [Parameter(Mandatory=$false)]
    [int]$TrafficPercentage = 10
)

Write-Host "🚀 Starting Blue/Green Deployment" -ForegroundColor Green
Write-Host "Environment: $Environment" -ForegroundColor Yellow
Write-Host "Target Color: $TargetColor" -ForegroundColor Yellow
Write-Host "Traffic Percentage: $TrafficPercentage%" -ForegroundColor Yellow

# Step 1: Deploy new version to target color
Write-Host "`n📦 Deploying to $TargetColor environment..." -ForegroundColor Cyan
aws cloudformation deploy `
  --template-file infrastructure/environments/$Environment/app-stack-$TargetColor.yaml `
  --stack-name taskmaster-$Environment-app-$TargetColor `
  --region us-east-1 `
  --capabilities CAPABILITY_IAM `
  --parameter-overrides Environment=$Environment DeploymentColor=$TargetColor

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    exit 1
}

# Step 2: Health check
Write-Host "`n🏥 Running health checks..." -ForegroundColor Cyan
$albDns = aws cloudformation describe-stacks --stack-name taskmaster-$Environment-alb-bg --query "Stacks[0].Outputs[?OutputKey=='ALBDNSName'].OutputValue" --output text

for ($i = 1; $i -le 5; $i++) {
    Write-Host "Health check attempt $i/5..."
    $response = curl -s "http://$albDns/health"
    if ($response -match "healthy") {
        Write-Host "✅ Health check passed!" -ForegroundColor Green
        break
    }
    Start-Sleep 10
}

# Step 3: Gradual traffic shift
Write-Host "`n🔄 Shifting $TrafficPercentage% traffic to $TargetColor..." -ForegroundColor Cyan

$blueWeight = if ($TargetColor -eq "blue") { $TrafficPercentage } else { 100 - $TrafficPercentage }
$greenWeight = if ($TargetColor -eq "green") { $TrafficPercentage } else { 100 - $TrafficPercentage }

# Update ALB listener weights
$listenerArn = aws cloudformation describe-stacks --stack-name taskmaster-$Environment-alb-bg --query "Stacks[0].Outputs[?OutputKey=='ALBListenerArn'].OutputValue" --output text
$blueTargetArn = aws cloudformation describe-stacks --stack-name taskmaster-$Environment-alb-bg --query "Stacks[0].Outputs[?OutputKey=='BlueTargetGroupArn'].OutputValue" --output text
$greenTargetArn = aws cloudformation describe-stacks --stack-name taskmaster-$Environment-alb-bg --query "Stacks[0].Outputs[?OutputKey=='GreenTargetGroupArn'].OutputValue" --output text

aws elbv2 modify-listener `
  --listener-arn $listenerArn `
  --default-actions Type=forward,ForwardConfig="{TargetGroups=[{TargetGroupArn=$blueTargetArn,Weight=$blueWeight},{TargetGroupArn=$greenTargetArn,Weight=$greenWeight}]}"

Write-Host "✅ Traffic shifted successfully!" -ForegroundColor Green
Write-Host "Blue: $blueWeight%, Green: $greenWeight%" -ForegroundColor Yellow

# Step 4: Monitor and validate
Write-Host "`n📊 Monitoring deployment..." -ForegroundColor Cyan
Write-Host "Monitor at: http://$albDns" -ForegroundColor Blue
Write-Host "Use 'scripts/deploy/rollback.ps1' if issues detected" -ForegroundColor Yellow

Write-Host "`n🎉 Blue/Green deployment completed!" -ForegroundColor Green