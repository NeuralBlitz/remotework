-----
name: bash
description: >
  Expert in Bash shell scripting for automation, system administration, and command-line 
  productivity. Use this skill for writing robust shell scripts, text processing, file 
  management, system automation, and DevOps tooling. Covers variables, control structures, 
  functions, text processing (awk/sed), and common automation patterns.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: scripting
  tags: [bash, shell, scripting, automation, devops, linux]

# Bash Shell Scripting

Covers: **Variables · Control Flow · Functions · Text Processing · File Operations · Error Handling · Command-Line Arguments · Automation Patterns**

-----

## Fundamentals and Best Practices

### Shell Options for Robust Scripts

```bash
#!/bin/bash

# Enable strict mode
set -euo pipefail

# Explanation:
# -e: Exit immediately on command failure
# -u: Treat unset variables as errors
# -o pipefail: Pipeline fails if any command fails
# -n: Check syntax without executing (use: bash -n script.sh)
# -x: Debug mode - print commands before executing

# Additional useful options
set -E  # Inherit ERR trap in functions
set -T  # Inherit DEBUG and RETURN traps

# Example with error handling
#!/bin/bash
set -euo pipefail

# Define cleanup function
cleanup() {
    local exit_code=$?
    echo "Cleaning up... (exit code: $exit_code)"
    # Add cleanup tasks here
    exit $exit_code
}

# Register cleanup trap
trap cleanup EXIT

# Function that might fail
risky_operation() {
    echo "Starting risky operation..."
    false  # This would cause script to exit without proper handling
}

# Using || to handle potential failure
risky_operation || echo "Operation failed, continuing..."

echo "Script completed successfully"
```

### Variables and Data Types

```bash
#!/bin/bash

# Basic variables
name="World"
age=30
height=5.11
is_active=true

# Read-only variables
readonly CONSTANT_VALUE="immutable"
# CONSTANT_VALUE="changed"  # This would fail

# Integer arithmetic
a=5
b=3
sum=$((a + b))           # Addition: 8
product=$((a * b))       # Multiplication: 15
power=$((a ** b))        # Exponentiation: 125

# String operations
str="Hello World"
echo "${#str}"            # Length: 11
echo "${str:0:5}"         # Substring: Hello
echo "${str#*o}"          # Remove prefix: World (first 'o')
echo "${str##*o}"         # Remove prefix: rld (last 'o')
echo "${str%o*}"          # Remove suffix: Hello W
echo "${str%%o*}"         # Remove suffix: Hell

# Arrays
fruits=("apple" "banana" "cherry")
echo "${fruits[0]}"       # First element: apple
echo "${fruits[@]}"       # All elements
echo "${#fruits[@]}"      # Array length: 3

# Associative arrays (Bash 4+)
declare -A user_info
user_info[name]="John"
user_info[email]="john@example.com"
user_info[age]=30

echo "${user_info[name]}"
echo "${!user_info[@]}"  # All keys
echo "${user_info[@]}"    # All values

# Environment variables
export APP_ENV="production"
export LOG_LEVEL="debug"

# Access with defaults
HOME_DIR="${HOME:-/tmp}"
API_KEY="${API_KEY:-default_key}"
```

### Control Flow

```bash
#!/bin/bash

# IF-ELSE STATEMENTS
name="admin"

if [ "$name" = "admin" ]; then
    echo "Welcome admin"
elif [ "$age" -ge 18 ]; then
    echo "Adult"
else
    echo "Minor"
fi

# File tests
file="/path/to/file"
if [ -f "$file" ]; then
    echo "Regular file exists"
fi

if [ -d "$file" ]; then
    echo "Directory exists"
fi

if [ -z "$var" ]; then
    echo "Variable is empty"
fi

if [ -n "$var" ]; then
    echo "Variable is not empty"
fi

if [ -r "$file" ]; then
    echo "File is readable"
fi

if [ -w "$file" ]; then
    echo "File is writable"
fi

if [ -x "$file" ]; then
    echo "File is executable"
fi

# String comparisons
if [[ "$str" == *"pattern"* ]]; then
    echo "Contains pattern"
fi

if [[ "$str" =~ ^regex$ ]]; then
    echo "Matches regex"
fi

# CASE STATEMENTS
read -p "Enter choice: " choice

case $choice in
    1)
        echo "Option 1 selected"
        ;;
    2)
        echo "Option 2 selected"
        ;;
    3|4)
        echo "Option 3 or 4"
        ;;
    *)
        echo "Invalid option"
        ;;
esac

# Pattern matching in case
filename="document.txt"

case $filename in
    *.txt)
        echo "Text file"
        ;;
    *.pdf)
        echo "PDF file"
        ;;
    *.jpg|*.png|*.gif)
        echo "Image file"
        ;;
    *)
        echo "Unknown file type"
        ;;
esac
```

### Loops

```bash
#!/bin/bash

# FOR LOOPS
# Range-based
for i in {1..5}; do
    echo "Number: $i"
done

# Array iteration
colors=("red" "green" "blue")
for color in "${colors[@]}"; do
    echo "Color: $color"
done

# Command substitution
for file in *.txt; do
    echo "Processing: $file"
done

# C-style for loop
for ((i=0; i<10; i++)); do
    echo "Count: $i"
done

# WHILE LOOPS
# Read file line by line
while IFS= read -r line; do
    echo "Line: $line"
done < file.txt

# Read with delimiter
while IFS= read -r -d '' file; do
    echo "File: $file"
done < <(find . -type f -print0)

# Infinite loop with break
count=0
while true; do
    count=$((count + 1))
    if [ $count -ge 10 ]; then
        break
    fi
    echo "Count: $count"
done

# UNTIL LOOP
until [ $count -eq 0 ]; do
    count=$((count - 1))
    echo "Counting down: $count"
done

# Parallel processing with xargs
cat hosts | xargs -P 10 -I {} ssh {} 'uptime'

# Loop control
for i in {1..10}; do
    if [ $i -eq 3 ]; then
        continue  # Skip iteration
    fi
    if [ $i -eq 8 ]; then
        break     # Exit loop
    fi
    echo "Number: $i"
done
```

### Functions

```bash
#!/bin/bash

# Function definitions
function greet() {
    local name="$1"  # local variable
    echo "Hello, $name!"
}

greet "World"

# Return value via echo
function get_sum() {
    local a=$1
    local b=$2
    echo $((a + b))
}

result=$(get_sum 5 10)
echo "Sum: $result"

# Return value via global
function divide() {
    if [ $2 -eq 0 ]; then
        echo "Error: Division by zero" >&2
        return 1
    fi
    echo $(( $1 / $2 ))
}

if divide 10 2; then
    echo "Division successful"
fi

# Returning arrays
function get_dates() {
    local dates=("2024-01-01" "2024-01-02" "2024-01-03")
    echo "${dates[@]}"
}

readarray -t date_array < <(get_dates)
echo "${date_array[@]}"

# Function with flags
function process() {
    local verbose=false
    local force=false
    local output_file=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -v|--verbose)
                verbose=true
                shift
                ;;
            -f|--force)
                force=true
                shift
                ;;
            -o|--output)
                output_file="$2"
                shift 2
                ;;
            *)
                echo "Unknown option: $1"
                return 1
                ;;
        esac
    done
    
    # Function body
    $verbose && echo "Processing..."
}

process -v -f -o output.txt
```

### Command-Line Arguments

```bash
#!/bin/bash

# Special variables
# $@ = all arguments
# $# = argument count
# $0 = script name
# $1, $2, ... = positional arguments
# $$ = script PID
# $? = exit status of last command

# Argument parsing with flags
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            help=true
            shift
            ;;
        -n|--name)
            name="$2"
            shift 2
            ;;
        -v|--verbose)
            verbose=true
            shift
            ;;
        -f|--force)
            force=true
            shift
            ;;
        -*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            echo "Positional argument: $1"
            shift
            ;;
    esac
done

# Default values
name="${name:-World}"
verbose="${verbose:-false}"

# Usage function
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help           Show this help message"
    echo "  -n, --name NAME      Set name"
    echo "  -v, --verbose        Enable verbose output"
    echo "  -f, --force          Force operation"
    exit 1
}

# Check required arguments
if [ -z "${name:-}" ]; then
    echo "Error: --name is required"
    usage
fi
```

-----

## Text Processing

### AWK

```bash
#!/bin/bash

# AWK basics
# Print specific columns
awk -F',' '{print $1, $3}' file.csv

# Calculate sum
awk -F',' '{sum+=$2} END {print sum}' file.txt

# Print with conditions
awk -F',' 'NR>1 && $2>100 {print $1, $2}' file.csv

# Field separator as regex
awk -F'[;,]' '{print $1}' mixed.csv

# Built-in variables
# NR = current record number
# NF = number of fields
# OFS = output field separator
# ORS = output record separator
# FS = field separator
# RS = record separator

# Calculate statistics
awk '
    BEGIN { sum=0; count=0 }
    { sum+=$2; count++ }
    END { 
        if (count > 0) {
            print "Sum:", sum
            print "Average:", sum/count
        }
    }
' data.txt

# Multiple actions
awk '
    BEGIN { FS="," }
    $3 > 1000 { high++ }
    $3 <= 1000 { low++ }
    END { 
        print "High values:", high
        print "Low values:", low
    }
' data.csv

# String functions
awk '{
    print toupper($1)
    print tolower($2)
    print length($1)
    print substr($1, 1, 5)
}' data.txt
```

### SED

```bash
#!/bin/bash

# Basic substitutions
sed 's/old/new/' file.txt           # Replace first occurrence
sed 's/old/new/g' file.txt          # Replace all occurrences
sed 's/old/new/2' file.txt          # Replace second occurrence

# In-place editing
sed -i 's/old/new/g' file.txt

# Regex substitution
sed 's/[0-9]*/NUM/g' file.txt

# Delete lines
sed '/pattern/d' file.txt           # Delete lines with pattern
sed '1,5d' file.txt                 # Delete lines 1-5
sed '/^$/d' file.txt               # Delete empty lines
sed '/^#/d' file.txt               # Delete comments

# Insert and append
sed '1i\Header line' file.txt      # Insert before line 1
sed '$a\Footer line' file.txt       # Append after last line

# Multi-line operations
sed 'N;s/\n/ /' file.txt           # Join lines

# Address-based operations
sed -n '10,20p' file.txt           # Print lines 10-20
sed -n '/start/,/end/p' file.txt  # Print between patterns

# Hold space for multi-line processing
sed ':a;N;$!ba;s/\n/,/g' file.txt  # Join all lines with comma

# Using & for matched string
sed 's/[a-z]/(&)/g' file.txt       # Wrap letters in parentheses
```

### FIND

```bash
#!/bin/bash

# Find files by name
find . -name "*.txt"
find . -iname "*.txt"               # Case insensitive
find . -name "*.txt" -o -name "*.md"

# Find by type
find . -type f                     # Regular files
find . -type d                     # Directories
find . -type l                     # Symbolic links
find . -type b                     # Block devices
find . -type c                     # Character devices

# Find by time
find . -mtime -7                   # Modified in last 7 days
find . -mtime +30                  # Modified more than 30 days ago
find . -atime -1                   # Accessed in last 24 hours
find . -ctime -1                   # Changed in last 24 hours

# Find by size
find . -size +1M                   # Larger than 1MB
find . -size -1k                   # Smaller than 1KB
find . -size 0                     # Empty files
find . -size +100M -size -1G      # Between 100MB and 1GB

# Find by permissions
find . -perm 644                  # Exact permissions
find . -perm -644                  # At least 644
find . -executable                 # Executable files

# Execute commands on found files
find . -name "*.log" -exec rm {} \;     # Delete log files
find . -name "*.txt" -exec wc {} \;    # Count lines

# Using xargs for better performance
find . -name "*.txt" | xargs wc -l
find . -name "*.txt" -print0 | xargs -0 -I {} mv {} ./backup/

# Find and move
find . -name "*.jpg" -exec mv {} ./images/ \;

# Combined conditions
find . -type f -name "*.txt" -size +1k -mtime -7

# Using -newer
find . -newer file.txt             # Modified after file.txt
```

-----

## Error Handling

```bash
#!/bin/bash
set -euo pipefail

# Check if command exists
if ! command -v git &> /dev/null; then
    echo "Error: Git is required but not installed"
    exit 1
fi

# Check if file exists
if [ ! -f "$file" ]; then
    echo "Error: File not found: $file"
    exit 1
fi

# Check if directory exists
if [ ! -d "$dir" ]; then
    mkdir -p "$dir" || { echo "Failed to create directory"; exit 1; }
fi

# Using && and ||
command1 && command2              # Run command2 if command1 succeeds
command1 || command2              # Run command2 if command1 fails

# Exit codes
if ! some_command; then
    echo "Command failed"
    exit 1
fi

# Trap for error handling
trap 'echo "Error on line $LINENO"' ERR

# Custom error function
error() {
    echo "ERROR: $*" >&2
    exit 1
}

# Usage
[ -z "$var" ] && error "Variable is required"

# Validate function input
validate_input() {
    local input=$1
    
    [ -z "$input" ] && return 1
    [[ "$input" =~ ^[a-z]+$ ]] || return 1
    
    return 0
}

validate_input "$var" || { echo "Invalid input"; exit 1; }
```

-----

## Useful Patterns

```bash
#!/bin/bash

# Progress bar
for i in {1..100}; do
    echo -ne "Progress: $i%\r"
    sleep 0.05
done
echo ""

# Download with progress
curl -# -O file.tar.gz

# Parallel processing
parallel --jobs 4 ./process.sh ::: file1 file2 file3

# Menu selection
PS3="Select option: "
select option in "Option 1" "Option 2" "Exit"; do
    case $option in
        "Option 1") echo "Selected 1"; break ;;
        "Option 2") echo "Selected 2"; break ;;
        "Exit") exit ;;
    esac
done

# Temporary file handling
tmpfile=$(mktemp)
trap "rm -f $tmpfile" EXIT

# Confirmation prompt
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Success!${NC}"
echo -e "${RED}Error!${NC}"

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

log "Starting process"
log "Completed successfully"

# Retry logic
max_retries=3
retry_count=0
until some_command; do
    retry_count=$((retry_count + 1))
    if [ $retry_count -ge $max_retries ]; then
        echo "Failed after $max_retries attempts"
        exit 1
    fi
    echo "Retrying... ($retry_count/$max_retries)"
    sleep 5
done
```

-----

## Common Automation Scripts

### Backup Script

```bash
#!/bin/bash
set -euo pipefail

SOURCE_DIRS=("/home" "/etc")
BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="backup_${DATE}.tar.gz"

# Create backup
tar -czf "${BACKUP_DIR}/${BACKUP_NAME}" "${SOURCE_DIRS[@]}"

# Verify backup
if [ $? -eq 0 ]; then
    echo "Backup created: ${BACKUP_NAME}"
else
    echo "Backup failed"
    exit 1
fi

# Clean old backups (keep last 7 days)
find "${BACKUP_DIR}" -name "backup_*.tar.gz" -mtime +7 -delete
```

### Monitoring Script

```bash
#!/bin/bash
set -euo pipefail

# Check disk usage
disk_usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')

if [ "$disk_usage" -gt 90 ]; then
    echo "WARNING: Disk usage at ${disk_usage}%"
    # Send alert
fi

# Check memory
free -m | awk 'NR==2 {printf "Memory Usage: %.2f%%\n", $3*100/$2 }'

# Check services
for service in nginx postgresql; do
    if systemctl is-active --quiet "$service"; then
        echo "$service: running"
    else
        echo "$service: NOT running"
    fi
done

# Check logs for errors
if journalctl -p err -n 5 --since "1 hour ago" | grep -q .; then
    echo "WARNING: Recent errors found in logs"
fi
```

### Deployment Script

```bash
#!/bin/bash
set -euo pipefail

APP_DIR="/opt/myapp"
BACKUP_DIR="/opt/myapp/backups"

echo "Starting deployment..."

# Backup current version
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp -r "$APP_DIR" "${BACKUP_DIR}/backup_${TIMESTAMP}"

# Pull latest changes
cd "$APP_DIR"
git pull origin main

# Install dependencies
npm ci --production

# Run migrations
npm run migrate

# Restart service
sudo systemctl restart myapp

# Health check
sleep 5
if curl -sf http://localhost:3000/health > /dev/null; then
    echo "Deployment successful!"
else
    echo "Deployment failed - rolling back"
    rm -rf "$APP_DIR"
    cp -r "${BACKUP_DIR}/backup_${TIMESTAMP}" "$APP_DIR"
    sudo systemctl restart myapp
    exit 1
fi
```
