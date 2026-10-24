---
name: shell
description: Shell scripting, bash, zsh, process management, and terminal productivity
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: scripting
---

## What I do
- Use shell commands effectively
- Write robust shell scripts
- Manage processes and jobs
- Handle I/O redirection and pipes
- Automate tasks
- Debug shell scripts

## When to use me
When working in terminal, automating tasks, or writing shell scripts.

## Shell Types
- **bash**: Bourne Again Shell, most popular
- **zsh**: Z Shell, Oh My Zsh, advanced features
- **fish**: Friendly Interactive Shell, user-friendly
- **sh**: POSIX shell, portable

## Basic Commands

### File Operations
```bash
ls -la          # List with details
cp -r           # Copy recursive
rm -rf          # Force remove
mkdir -p        # Create nested dirs
chmod           # Change permissions
chown           # Change owner
```

### Text Processing
```bash
cat             # View file
grep            # Search pattern
sed             # Stream editor
awk             # Text processing
sort            # Sort lines
uniq            # Unique lines
head/tail       # First/last lines
wc              # Word count
```

### System
```bash
ps              # Process status
top/htop        # Process monitor
kill            # Kill process
df              # Disk free
du              # Disk usage
free            # Memory
```

## Scripting

### Shebang
```bash
#!/bin/bash
#!/usr/bin/env bash
```

### Variables
```bash
NAME="John"
echo $NAME
echo ${NAME}
# Arrays
arr=(one two three)
echo ${arr[0]}
```

### Conditionals
```bash
if [ $name = "admin" ]; then
    echo "Hello admin"
elif [ $name = "guest" ]; then
    echo "Hello guest"
else
    echo "Hello stranger"
fi
```

### Loops
```bash
# For loop
for f in *.txt; do
    echo "Processing $f"
done

# While loop
while read line; do
    echo "$line"
done < file.txt
```

### Functions
```bash
greet() {
    local name=$1
    echo "Hello, $name"
}
greet "World"
```

## Advanced Features

### I/O Redirection
```bash
>   # Redirect stdout
2>  # Redirect stderr
&>  # Redirect both
>>  # Append
<   # Redirect stdin
|   # Pipe
```

### Process Substitution
```bash
diff <(ls dir1) <(ls dir2)
```

### Parameter Expansion
```bash
${var:-default}  # Default if unset
${var:=default}  # Set default
${var:?error}   # Error if unset
${var#pattern}  # Remove prefix
${var%pattern}  # Remove suffix
${var/old/new} # Replace
```

### Globbing
```bash
*.txt       # All txt files
file?.txt   # file1.txt, file2.txt
[abc]*.txt  # Starting with a,b,c
```

## Best Practices
- Use `set -euo pipefail`
- Quote variables
- Use `[[ ]]` over `[ ]`
- Add comments
- Use functions
- Check exit codes
- Use shellcheck
- Make scripts portable
