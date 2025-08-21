Write-Host "Getting ALB DNS name..." -ForegroundColor Green

try {
    $ALB_DNS = aws cloudformation describe-stacks --stack-name taskmaster-dev-alb --query "Stacks[0].Outputs[?OutputKey=='ALBDNSName'].OutputValue" --output text
    
    if ([string]::IsNullOrEmpty($ALB_DNS)) {
        Write-Host "Error: Could not get ALB DNS name. Make sure ALB stack is deployed." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    Write-Host "ALB DNS: $ALB_DNS" -ForegroundColor Yellow
    Write-Host "Opening TaskMaster demo..." -ForegroundColor Green
    
    $currentDir = Get-Location
    $htmlFile = Join-Path $currentDir "demo-frontend.html"
    $demoUrl = "file:///$htmlFile?alb=$ALB_DNS"
    
    # Use default browser to open the file
    Start-Process $htmlFile
    
    Write-Host "Demo opened in browser!" -ForegroundColor Green
    Read-Host "Press Enter to exit"
}
catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}