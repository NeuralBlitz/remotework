---

## name: powershell
description: >
  PowerShell expert for Windows automation, system administration, and scripting. Use this
  skill whenever the user needs: automating Windows tasks, managing Active Directory, working
  with Windows Management Instrumentation (WMI), scripting complex administrative tasks,
  or any task involving PowerShell scripting for Windows environments. This skill covers
  PowerShell fundamentals, cmdlets, scripting constructs, modules, and practical
  administration examples.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: scripting

# PowerShell — Windows Automation and Administration

Covers: **Cmdlets · Variables and Types · Control Flow · Functions · Modules · WMI/CIM · Active Directory · File Operations · Registry · Error Handling**

-----

## PowerShell Fundamentals

### Getting Started

```powershell
# Basic commands
Get-Command                    # List all commands
Get-Help Get-Process           # Get help for a command
Get-Member                     # Get object members
Get-Alias                      # List aliases

# Working with providers
Get-PSProvider                 # List providers
Get-PSDrive                    # List drives

# Environment
$PSVersionTable               # Check PowerShell version
$env:VARIABLE_NAME            # Access environment variables
```

### Variables and Data Types

```powershell
# Variables (prefixed with $)
$name = "John"
$age = 30
$isActive = $true
$prices = @(10.50, 20.25, 15.00)  # Array
$person = @{                      # Hashtable
    Name = "John"
    Age = 30
    City = "Seattle"
}

# Type annotations
[string]$name = "John"
[int]$count = 10
[datetime]$date = "2024-01-01"
[array]$items = @()

# Common types
$int = 42                    # System.Int32
$double = 3.14               # System.Double
$bool = $true                # System.Boolean
$array = @()                 # System.Object[]
$hash = @{}                  # System.Collections.Hashtable
```

### Operators

```powershell
# Arithmetic operators
+, -, *, /, %                # Addition, subtraction, multiplication, division, modulo

# Comparison operators
-eq, -ne                     # Equal, not equal
-gt, -lt, -ge, -le          # Greater than, less than, >=, <=
-like, -notlike              # Wildcard matching
-match, -notmatch            # Regex matching
-contains, -notcontains      # Collection containment

# Logical operators
-and, -or, -not, -xor       # Logical AND, OR, NOT, XOR

# Assignment operators
=, +=, -=, *=, /=, %=       # Assignment and compound

# Special operators
?.                          # Null-conditional
??                           # Null-coalescing
..                           # Range operator
```

-----

## Working with Objects

### Pipeline and Objects

```powershell
# Objects flow through the pipeline
Get-Process | Sort-Object CPU -Descending | Select-Object -First 5

# Common cmdlets for working with objects
Get-Process | 
    Where-Object { $_.CPU -gt 10 } | 
    Select-Object Name, CPU, WorkingSet |
    Sort-Object CPU -Descending |
    Format-Table

# Creating custom objects
$obj = [PSCustomObject]@{
    Name = "John"
    Age = 30
    City = "Seattle"
}

# Adding methods
$obj | Add-Member -MemberType ScriptMethod -Name GetInfo -Value {
    return "$($this.Name) is $($this.Age) years old"
}
```

### Formatting Output

```powershell
# Format cmdlets
Format-Table                    # Table format
Format-List                      # List format
Format-Wide                      # Wide format
Format-Custom                    # Custom format

# Output cmdlets
Out-Host                        # Send to console
Out-File                        # Save to file
Out-String                     # Convert to string
Out-Null                       # Discard output

# Export cmdlets
Export-Csv                      # Export to CSV
Export-Clixml                   # Export to XML
ConvertTo-Json                  # Convert to JSON
ConvertTo-Html                   # Convert to HTML
```

-----

## Control Flow

### Conditionals

```powershell
# If-ElseIf-Else
if ($age -lt 18) {
    Write-Host "Minor"
} elseif ($age -lt 65) {
    Write-Host "Adult"
} else {
    Write-Host "Senior"
}

# Switch statement
switch ($status) {
    "Active" { Write-Host "User is active" }
    "Inactive" { Write-Host "User is inactive" }
    "Pending" { Write-Host "Awaiting approval" }
    default { Write-Host "Unknown status" }
}

# Ternary operator (PowerShell 7+)
$result = $age -ge 18 ? "Adult" : "Minor"
```

### Loops

```powershell
# For loop
for ($i = 0; $i -lt 10; $i++) {
    Write-Host $i
}

# ForEach loop
foreach ($item in $collection) {
    Write-Host $item
}

# ForEach-Object (pipeline)
1..10 | ForEach-Object { $_ * 2 }

# While loop
while ($condition) {
    # code
}

# Do-While
do {
    # code
} while ($condition)

# Do-Until
do {
    # code
} until ($condition)

# Parallel ForEach (PowerShell 7+)
1..10 -Parallel { $_ * 2 }
```

-----

## Functions

### Basic Functions

```powershell
function Get-Square {
    param (
        [Parameter(Mandatory=$true)]
        [int]$Number
    )
    
    return $Number * $Number
}

# Calling the function
$result = Get-Square -Number 5
```

### Advanced Functions

```powershell
function Invoke-MainOperation {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true, Position=0)]
        [string]$Name,
        
        [Parameter(Mandatory=$false)]
        [int]$Age = 18,
        
        [Parameter(Mandatory=$false)]
        [ValidateSet("Active", "Inactive", "Pending")]
        [string]$Status = "Active",
        
        [Parameter(ValueFromPipeline=$true)]
        [string]$InputObject
    )
    
    begin {
        # Runs once before processing
        $total = 0
    }
    
    process {
        # Runs for each input object
        $total++
        Write-Host "Processing: $Name (Age: $Age, Status: $Status)"
    }
    
    end {
        # Runs once after processing
        Write-Host "Processed $total items"
    }
}

# Advanced: Supports ShouldProcess (WhatIf, Confirm)
function Remove-ItemSafely {
    [CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
    param (
        [Parameter(Mandatory=$true)]
        [string]$Path
    )
    
    if ($PSCmdlet.ShouldProcess($Path, "Remove item")) {
        Remove-Item -Path $Path -Force
        Write-Host "Item removed"
    }
}
```

### Advanced Parameters

```powershell
# Parameter attributes
function Test-Parameters {
    param(
        # Mandatory parameter
        [Parameter(Mandatory=$true)]
        [string]$RequiredParam,
        
        # Default value
        [string]$DefaultParam = "Default",
        
        # Validate set
        [ValidateSet("Option1", "Option2", "Option3")]
        [string]$ValidateParam,
        
        # Validate range
        [ValidateRange(1, 100)]
        [int]$RangeParam,
        
        # Validate pattern (regex)
        [ValidatePattern("^[A-Z]{3}$")]
        [string]$PatternParam,
        
        # Allow null
        [AllowNull()]
        [string]$AllowNullParam,
        
        # Allow empty string
        [AllowEmptyString()]
        [string]$AllowEmptyParam,
        
        # Array of values
        [Parameter(ValueFromPipeline=$true)]
        [string[]]$ArrayParam
    )
}
```

-----

## File Operations

### Working with Files and Directories

```powershell
# File system navigation
Set-Location C:\Scripts
Get-ChildItem                    # List files
Get-ChildItem -Recurse           # Recursive listing
Get-ChildItem -Filter "*.txt"    # Filter by pattern

# File operations
Copy-Item -Path source -Destination dest
Move-Item -Path source -Destination dest
Remove-Item -Path file -Force
New-Item -Path newfile -ItemType File

# Reading and writing files
Get-Content -Path file.txt
Get-Content -Path file.txt -Tail 10    # Last 10 lines
Set-Content -Path file.txt -Value "Content"
Add-Content -Path file.txt -Value "Append"

# Working with CSV
Import-Csv -Path data.csv
Export-Csv -Path output.csv -NoTypeInformation

# Working with JSON
$object | ConvertTo-Json
Get-Content -Path data.json | ConvertFrom-Json
```

### Working with XML

```powershell
# Reading XML
[xml]$xml = Get-Content -Path data.xml
$xml.root.childelement

# Modifying XML
$xml.root.element = "New Value"
$xml.Save("output.xml")

# Creating XML
$xml = [xml]@"
<configuration>
    <setting name="Debug" value="true"/>
</configuration>
"@
```

-----

## Windows Management Instrumentation (WMI/CIM)

### WMI and CIM Cmdlets

```powershell
# Get system information
Get-CimInstance -ClassName Win32_ComputerSystem
Get-CimInstance -ClassName Win32_OperatingSystem
Get-CimInstance -ClassName Win32_Processor
Get-CimInstance -ClassName Win32_LogicalDisk

# Get services
Get-CimInstance -ClassName Win32_Service | 
    Where-Object { $_.State -eq 'Running' }

# Get processes
Get-CimInstance -ClassName Win32_Process | 
    Select-Object Name, ProcessId, WorkingSetSize

# Remote WMI
Get-CimInstance -ClassName Win32_OperatingSystem -ComputerName Server01

# WMI filtering
Get-CimInstance -ClassName Win32_Service -Filter "Name='Spooler'"
```

### Registry Operations

```powershell
# Registry provider
Get-ItemProperty -Path HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion

# Registry cmdlets
Get-Item -Path HKCU:\Environment
Set-ItemProperty -Path HKCU:\Environment -Name MyVar -Value "Value"
New-Item -Path HKCU:\MyKey
Remove-Item -Path HKCU:\MyKey
```

-----

## Active Directory

### AD Module Cmdlets

```powershell
# Import AD module
Import-Module ActiveDirectory

# User operations
Get-ADUser -Identity username
New-ADUser -Name "John Doe" -SamAccountName jdoe -UserPrincipalName jdoe@domain.com
Set-ADUser -Identity jdoe -Department "IT"
Remove-ADUser -Identity jdoe -Confirm:$false

# Group operations
Get-ADGroup -Identity "Domain Admins"
New-ADGroup -Name "IT-Admins" -GroupScope Global
Add-ADGroupMember -Identity "IT-Admins" -Members jdoe
Remove-ADGroupMember -Identity "IT-Admins" -Members jdoe

# Computer operations
Get-ADComputer -Filter *
Get-ADComputer -Identity "Computer01"
New-ADComputer -Name "Computer02" -SamAccountName Computer02

# Organizational Units
Get-ADOrganizationalUnit -Filter *
New-ADOrganizationalUnit -Name "Sales" -Path "dc=domain,dc=com"

# Searching AD
Get-ADUser -Filter {Department -eq "IT"} -Properties Department, Title
Get-ADUser -SearchBase "ou=IT,dc=domain,dc=com" -Filter *
```

### Advanced AD Operations

```powershell
# Password operations
Set-ADAccountPassword -Identity jdoe -NewPassword (ConvertTo-SecureString "Pass@word1" -AsPlainText -Force)
Set-ADUser -Identity jdoe -ChangePasswordAtLogon $true

# Account control
Set-ADUser -Identity jdoe -Enabled $true -PasswordNeverExpires $false

# Group membership
Get-ADGroupMember -Identity "Domain Users" | Select-Object Name, SamAccountName

# Nested group membership
Get-ADGroupMember -Identity "Domain Admins" -Recursive

# User with properties
Get-ADUser -Identity jdoe -Properties * | 
    Select-Object Name, EmailAddress, Department, Manager, MemberOf
```

-----

## Modules and Packaging

### Working with Modules

```powershell
# List modules
Get-Module -ListAvailable

# Import module
Import-Module Pester

# Find module
Find-Module -Name *Azure*

# Install module
Install-Module -Name Az -Scope CurrentUser

# Create module
New-Module -Name MyModule -ScriptBlock {
    function Get-Square {
        param([int]$Number)
        $Number * $Number
    }
    
    Export-ModuleMember -Function Get-Square
}

# Module manifest
New-ModuleManifest -Path .\MyModule.psd1 -Author "Author" -Description "Description"
```

### Creating Scripts and Modules

```powershell
# Script structure
#Requires -Version 5.1
<#
.SYNOPSIS
    Script description

.DESCRIPTION
    Detailed description

.PARAMETER Name
    Parameter description

.EXAMPLE
    Example usage

.NOTES
    Author: Name
    Version: 1.0
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Name
)

# Script body
Write-Host "Hello, $Name"
```

-----

## Error Handling

### Try-Catch-Finally

```powershell
try {
    # Risky operation
    Get-Content -Path "nonexistent.txt" -ErrorAction Stop
}
catch [System.IO.FileNotFoundException] {
    Write-Host "File not found: $_"
}
catch {
    Write-Host "An error occurred: $_"
}
finally {
    # Always runs
    Write-Host "Cleanup code here"
}
```

### Advanced Error Handling

```powershell
# Error action preferences
$ErrorActionPreference = "Stop"  # Stop, Continue, SilentlyContinue, Inquire

# Try-Catch with multiple errors
try {
    # Multiple operations
    $result = $null
    $result.Method()
}
catch [System.NullReferenceException] {
    Write-Host "Null reference: $($_.Exception.Message)"
}
catch [System.InvalidOperationException] {
    Write-Host "Invalid operation: $($_.Exception.Message)"
}
finally {
    # Cleanup
}

# Throwing custom errors
function Test-Input {
    param([string]$Input)
    
    if ($Input -eq "") {
        throw [System.ArgumentException]::new("Input cannot be empty", "Input")
    }
}
```

### Logging

```powershell
# Write to event log
Write-EventLog -LogName Application -Source "MyScript" -EventId 1000 -Message "Message"

# Start-Transcript / Stop-Transcript
Start-Transcript -Path C:\Logs\script.log
# ... script code ...
Stop-Transcript

# Using a logging function
function Write-Log {
    param(
        [string]$Message,
        [ValidateSet("Info", "Warning", "Error")]
        [string]$Level = "Info"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    Add-Content -Path C:\Logs\script.log -Value $logMessage
    
    if ($Level -eq "Error") {
        Write-Error $logMessage
    }
}
```

-----

## Practical Examples

### System Administration Scripts

```powershell
# Get disk space
Get-CimInstance Win32_LogicalDisk | 
    Select-Object DeviceID, 
        @{N='Size(GB)';E={[math]::Round($_.Size/1GB,2)}}, 
        @{N='Free(GB)';E={[math]::Round($_.FreeSpace/1GB,2)}}

# Find large files
Get-ChildItem C:\ -Recurse -File -ErrorAction SilentlyContinue | 
    Sort-Object Length -Descending | 
    Select-Object -First 20 FullName, @{N='Size(MB)';E={[math]::Round($_.Length/1MB,2)}}

# Process monitoring
Get-Process | 
    Where-Object { $_.WorkingSet -gt 100MB } | 
    Sort-Object WorkingSet -Descending | 
    Select-Object Name, @{N='Memory(MB)';E={[math]::Round($_.WorkingSet/1MB,2)}} -First 10

# Service management
Get-Service | 
    Where-Object { $_.Status -eq 'Running' } | 
    Select-Object Name, DisplayName, Status | 
    Sort-Object Name
```

### User Management Script

```powershell
# Create user from CSV
$users = Import-Csv C:\Scripts\users.csv

foreach ($user in $users) {
    try {
        $password = ConvertTo-SecureString $user.Password -AsPlainText -Force
        
        New-ADUser `
            -Name $user.Name `
            -SamAccountName $user.SamAccountName `
            -UserPrincipalName "$($user.SamAccountName)@domain.com" `
            -EmailAddress $user.Email `
            -Department $user.Department `
            -Title $user.Title `
            -AccountPassword $password `
            -Enabled $true
        
        Write-Host "Created user: $($user.SamAccountName)"
    }
    catch {
        Write-Warning "Failed to create $($user.SamAccountName): $_"
    }
}
```

-----

## Common Errors to Avoid

- **Forgetting to use -ErrorAction**: Always handle errors explicitly
- **Not using pipeline properly**: Leverage pipeline for efficiency
- **Ignoring object types**: PowerShell is object-oriented; use methods
- **Not checking null values**: Use ?. or -and conditionals
- **Using Write-Host instead of Write-Output**: Write-Host bypasses pipeline
- **Ignoring scope**: Understand $local, $script, $global scope
- **Not using ShouldProcess**: For destructive operations, support -WhatIf
- **Forgetting to dispose**: Close files, dispose objects
- **Ignoring strict mode**: Use Set-StrictMode -Version Latest
- **Not handling encoding**: Be careful with non-ASCII characters in files
