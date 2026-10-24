-----

## name: windows
description: >
Expert Windows administration, PowerShell scripting, and systems automation. Always use
this skill when the user needs to: write or debug PowerShell scripts, manage Active Directory
users/groups/OUs, configure Windows services, manage the registry, set up Group Policy,
automate tasks with Task Scheduler, manage IIS, troubleshoot Windows errors, configure
networking (DNS, DHCP, firewall), handle permissions and ACLs, work with Windows Event Logs,
manage Hyper-V, or administer Windows Server. Trigger for any mention of PowerShell, cmd,
winrm, GPO, AD, WSUS, IIS, NTFS permissions, or Windows-specific sysadmin tasks — even
if the user just says “how do I do X on Windows”.
license: MIT
compatibility: opencode
metadata:
audience: developers
category: systems-administration

# Windows Administration & PowerShell

Covers: **PowerShell scripting · Active Directory · Services & Processes · Networking · Security · IIS · Registry · Event Logs**

-----

## PowerShell Scripting Fundamentals

### Script Best Practices

```powershell
#Requires -Version 5.1
#Requires -RunAsAdministrator

[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)]
    [string]$ComputerName,

    [Parameter()]
    [ValidateSet("Start","Stop","Restart")]
    [string]$Action = "Restart",

    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Logging helper
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $entry = "[$ts] [$Level] $Message"
    Add-Content -Path "$PSScriptRoot\script.log" -Value $entry
    Write-Verbose $entry
}

# Error handling
try {
    Write-Log "Starting action '$Action' on $ComputerName"
    # ... work here ...
}
catch {
    Write-Log "FAILED: $_" -Level "ERROR"
    throw
}
```

### Common Patterns

```powershell
# Pipeline with filtering and projection
Get-Process | Where-Object { $_.CPU -gt 100 } |
    Select-Object Name, Id, CPU, WorkingSet |
    Sort-Object CPU -Descending |
    Format-Table -AutoSize

# ForEach-Object with progress
$servers = @("srv01","srv02","srv03")
$i = 0
$servers | ForEach-Object {
    $i++
    Write-Progress -Activity "Checking servers" -Status $_ -PercentComplete ($i/$servers.Count*100)
    Test-Connection $_ -Count 1 -Quiet
}

# Hash tables as lookup / config
$config = @{
    LogPath    = "C:\Logs\app.log"
    MaxRetries = 3
    Timeout    = 30
}

# String interpolation and here-strings
$name = "World"
Write-Output "Hello, $name!"          # variable expansion
Write-Output 'No $expansion here'     # literal
$body = @"
Dear $name,
This is a multiline message.
"@

# Splatting (clean way to pass many parameters)
$params = @{
    ComputerName = "srv01"
    Credential   = $cred
    ErrorAction  = "Stop"
}
Get-Service @params
```

-----

## Active Directory

```powershell
Import-Module ActiveDirectory

# --- Users ---
# Create user
New-ADUser -Name "Jane Smith" `
    -SamAccountName "jsmith" `
    -UserPrincipalName "jsmith@contoso.com" `
    -GivenName "Jane" -Surname "Smith" `
    -Path "OU=Sales,DC=contoso,DC=com" `
    -AccountPassword (Read-Host -AsSecureString "Password") `
    -Enabled $true `
    -PasswordNeverExpires $false `
    -ChangePasswordAtLogon $true

# Bulk-create from CSV
Import-Csv "new_users.csv" | ForEach-Object {
    New-ADUser -Name "$($_.First) $($_.Last)" `
        -SamAccountName $_.Username `
        -Department $_.Department `
        -Path "OU=$($_.Department),DC=contoso,DC=com" `
        -AccountPassword (ConvertTo-SecureString $_.TempPass -AsPlainText -Force) `
        -Enabled $true
}

# Find stale accounts (90+ days no login)
$cutoff = (Get-Date).AddDays(-90)
Get-ADUser -Filter { LastLogonDate -lt $cutoff -and Enabled -eq $true } `
    -Properties LastLogonDate, Department |
    Select-Object Name, SamAccountName, LastLogonDate, Department |
    Export-Csv "stale_accounts.csv" -NoTypeInformation

# --- Groups ---
New-ADGroup -Name "VPN-Users" -GroupScope Global -GroupCategory Security `
    -Path "OU=Groups,DC=contoso,DC=com"

# Add members from list
$members = @("jsmith","bjones","kwilliams")
Add-ADGroupMember -Identity "VPN-Users" -Members $members

# Get all members recursively
Get-ADGroupMember -Identity "Domain Admins" -Recursive |
    Select-Object Name, SamAccountName, objectClass

# --- OUs ---
New-ADOrganizationalUnit -Name "Contractors" `
    -Path "DC=contoso,DC=com" `
    -ProtectedFromAccidentalDeletion $true

# --- Computers ---
# Find computers not seen in 60 days
Get-ADComputer -Filter { LastLogonDate -lt $((Get-Date).AddDays(-60)) } `
    -Properties LastLogonDate, OperatingSystem |
    Select-Object Name, LastLogonDate, OperatingSystem
```

-----

## Services, Processes & Scheduled Tasks

```powershell
# Services
Get-Service | Where-Object { $_.Status -eq "Stopped" -and $_.StartType -eq "Automatic" }
Set-Service -Name "wuauserv" -StartupType Disabled
Restart-Service -Name "spooler" -Force

# Remote service management
Invoke-Command -ComputerName srv01, srv02 -ScriptBlock {
    Get-Service -Name "MyAppService" | Select-Object Name, Status
}

# Processes
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10 Name, Id, CPU, @{
    Name="RAM(MB)"; Expression={ [math]::Round($_.WorkingSet/1MB,1) }
}
Stop-Process -Name "notepad" -Force

# Scheduled Tasks
$action  = New-ScheduledTaskAction -Execute "PowerShell.exe" `
               -Argument "-NonInteractive -File C:\Scripts\backup.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At "2:00AM"
$settings = New-ScheduledTaskSettingsSet -RunOnlyIfNetworkAvailable `
                -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 2)

Register-ScheduledTask -TaskName "NightlyBackup" `
    -Action $action -Trigger $trigger -Settings $settings `
    -RunLevel Highest -User "SYSTEM"
```

-----

## Networking

```powershell
# IP configuration
Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.PrefixOrigin -ne "WellKnown" }
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 192.168.1.50 `
    -PrefixLength 24 -DefaultGateway 192.168.1.1
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses 8.8.8.8, 1.1.1.1

# Firewall
New-NetFirewallRule -DisplayName "Allow App Port 8080" `
    -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow
Get-NetFirewallRule | Where-Object { $_.Enabled -eq $true -and $_.Direction -eq "Inbound" } |
    Select-Object DisplayName, Profile, Action | Format-Table

# Connectivity troubleshooting
Test-NetConnection -ComputerName "google.com" -Port 443
Resolve-DnsName "internal.contoso.com" -Type A
Get-NetTCPConnection -State Listen | Select-Object LocalPort, OwningProcess |
    Sort-Object LocalPort

# Remote management
Enable-PSRemoting -Force
Enter-PSSession -ComputerName srv01 -Credential (Get-Credential)
Invoke-Command -ComputerName (Get-Content servers.txt) -ScriptBlock { hostname }
```

-----

## Registry

```powershell
# Read
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion" |
    Select-Object ProductName, CurrentBuild, ReleaseId

# Write
Set-ItemProperty -Path "HKCU:\Software\MyApp" -Name "Theme" -Value "Dark"

# Create key if missing
$path = "HKLM:\SOFTWARE\MyCompany\Config"
if (-not (Test-Path $path)) { New-Item -Path $path -Force }
New-ItemProperty -Path $path -Name "MaxConnections" -Value 100 -PropertyType DWord -Force

# Remove
Remove-ItemProperty -Path $path -Name "OldSetting"

# Remote registry (requires RemoteRegistry service)
$reg = [Microsoft.Win32.RegistryKey]::OpenRemoteBaseKey("LocalMachine", "srv01")
$key = $reg.OpenSubKey("SOFTWARE\MyApp")
$val = $key.GetValue("Version")
```

-----

## NTFS Permissions & ACLs

```powershell
# View permissions
Get-Acl "C:\Data\Shared" | Format-List

# Add permission
$acl  = Get-Acl "C:\Data\Shared"
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    "CONTOSO\Sales", "ReadAndExecute", "ContainerInherit,ObjectInherit", "None", "Allow"
)
$acl.AddAccessRule($rule)
Set-Acl "C:\Data\Shared" $acl

# Remove a specific user's access
$acl = Get-Acl "C:\Data\Sensitive"
$acl.Access | Where-Object { $_.IdentityReference -match "TempUser" } |
    ForEach-Object { $acl.RemoveAccessRule($_) }
Set-Acl "C:\Data\Sensitive" $acl

# Audit all permissions on a folder tree
Get-ChildItem "C:\Data" -Recurse -Directory | ForEach-Object {
    $acl = Get-Acl $_.FullName
    $acl.Access | Select-Object @{N="Path";E={$_.FullName}},
        IdentityReference, FileSystemRights, AccessControlType
} | Export-Csv "permissions_audit.csv" -NoTypeInformation
```

-----

## Event Logs

```powershell
# Query system and security logs
Get-WinEvent -LogName System -MaxEvents 50 |
    Where-Object { $_.LevelDisplayName -eq "Error" } |
    Select-Object TimeCreated, Id, Message | Format-List

# Filter by event ID (e.g., failed logons = 4625)
Get-WinEvent -FilterHashtable @{
    LogName   = "Security"
    Id        = 4625
    StartTime = (Get-Date).AddHours(-24)
} | Select-Object TimeCreated, Message

# Application crashes (event 1000)
Get-WinEvent -FilterHashtable @{ LogName="Application"; Id=1000 } -MaxEvents 20 |
    Select-Object TimeCreated, @{N="App";E={$_.Properties[0].Value}}, Message

# Export logs for analysis
Get-WinEvent -LogName "Microsoft-Windows-PowerShell/Operational" |
    Export-Csv "ps_audit.csv" -NoTypeInformation
```

-----

## IIS Administration

```powershell
Import-Module WebAdministration

# List sites and app pools
Get-Website | Select-Object Name, State, PhysicalPath, @{N="Port";E={$_.Bindings.Collection.bindingInformation}}
Get-WebConfiguration "system.applicationHost/applicationPools/add" |
    Select-Object name, state, managedRuntimeVersion

# Create site
New-Website -Name "MyApp" -PhysicalPath "C:\inetpub\myapp" `
    -ApplicationPool "MyAppPool" -Port 443 -Ssl

# App pool management
New-WebAppPool -Name "MyAppPool"
Set-ItemProperty "IIS:\AppPools\MyAppPool" -Name "managedRuntimeVersion" -Value "v4.0"
Set-ItemProperty "IIS:\AppPools\MyAppPool" -Name "recycling.periodicRestart.time" `
    -Value ([TimeSpan]::FromHours(24))

# Check for failed requests
Get-WebConfiguration "system.webServer/httpErrors" -PSPath "IIS:\Sites\MyApp"
```

-----

## Quick Reference

|Task              |Command                                                                                                 |
|------------------|--------------------------------------------------------------------------------------------------------|
|Check disk space  |`Get-PSDrive -PSProvider FileSystem`                                                                    |
|Find large files  |`Get-ChildItem C:\ -Recurse -ErrorAction SilentlyContinue | Sort-Object Length -Desc | Select -First 20`|
|Who is logged in  |`query user /server:srv01`                                                                              |
|Open ports        |`netstat -ano | findstr LISTENING`                                                                      |
|Check OS/uptime   |`Get-ComputerInfo | Select OsName,OsLastBootUpTime`                                                     |
|Installed software|`Get-Package | Select Name,Version`                                                                     |
|Pending reboots   |`Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending"`   |
|Disk health       |`Get-PhysicalDisk | Select FriendlyName,HealthStatus,OperationalStatus`                                 |
|Force GP update   |`gpupdate /force`                                                                                       |
|Check GP results  |`gpresult /r`                                                                                           |