@echo off
echo Getting ALB DNS name...

REM Get ALB DNS from CloudFormation
for /f "tokens=*" %%i in ('aws cloudformation describe-stacks --stack-name taskmaster-dev-alb --query "Stacks[0].Outputs[?OutputKey==`ALBDNSName`].OutputValue" --output text') do set ALB_DNS=%%i

if "%ALB_DNS%"=="" (
    echo Error: Could not get ALB DNS name. Make sure ALB stack is deployed.
    pause
    exit /b 1
)

echo ALB DNS: %ALB_DNS%
echo Opening TaskMaster demo...

REM Open browser with ALB DNS as parameter
start "" "demo-frontend.html?alb=%ALB_DNS%"

echo Demo opened in browser!
pause