import chalk from 'chalk';
import boxen from 'boxen';
import { select, confirm } from '@inquirer/prompts';
import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs/promises';
import path from 'path';

const execAsync = promisify(exec);

const menuItems = [
  {
    name: '📁 File Operations',
    value: 'file',
    description: 'List, read, create files'
  },
  {
    name: '🔧 Git Helpers',
    value: 'git',
    description: 'Status, branches, commits'
  },
  {
    name: '📦 Project Scaffolder',
    value: 'scaffold',
    description: 'Create new projects'
  },
  {
    name: '🖥️ System Info',
    value: 'sysinfo',
    description: 'System information'
  },
  {
    name: '🚀 Quick Actions',
    value: 'quick',
    description: 'Common dev tasks'
  },
  {
    name: '⚙️ Settings',
    value: 'settings',
    description: 'Configure toolbox'
  }
];

export async function showMenu() {
  const banner = boxen(
    chalk.bold.cyan('🧰 Toolbox CLI') + '\n' +
    chalk.dim('Developer productivity toolkit'),
    { padding: 1, borderStyle: 'round', borderColor: 'cyan' }
  );
  
  console.log(banner);
  console.log();
  
  while (true) {
    const choice = await select({
      message: chalk.cyan('What would you like to do?'),
      choices: [
        ...menuItems,
        { name: chalk.red('❌ Exit'), value: 'exit' }
      ]
    });
    
    if (choice === 'exit') {
      console.log(chalk.dim('\n👋 Goodbye!\n'));
      break;
    }
    
    await handleChoice(choice);
  }
}

async function handleChoice(choice) {
  const spinner = { succeed: () => {}, fail: () => {}, start: () => {} };
  
  try {
    switch (choice) {
      case 'file':
        await interactiveFileOps();
        break;
      case 'git':
        await interactiveGitOps();
        break;
      case 'scaffold':
        await interactiveScaffold();
        break;
      case 'sysinfo':
        await showSysInfo();
        break;
      case 'quick':
        await showQuickActions();
        break;
      case 'settings':
        await showSettings();
        break;
    }
  } catch (err) {
    console.log(chalk.red(`\n✗ Error: ${err.message}\n`));
  }
}

async function interactiveFileOps() {
  console.log(chalk.bold.cyan('\n📁 File Operations\n'));
  
  const action = await select({
    message: 'Select operation:',
    choices: [
      { name: 'List current directory', value: 'ls' },
      { name: 'List with details', value: 'ls -la' },
      { name: 'Show file info', value: 'stat' },
      { name: 'Read file', value: 'cat' }
    ]
  });
  
  if (action === 'ls') {
    const { stdout } = await execAsync('ls -la');
    console.log(chalk.dim(stdout));
  } else if (action === 'stat') {
    const name = await input({ message: 'File path:' });
    try {
      const { stdout } = await execAsync(`stat "${name}"`);
      console.log(chalk.dim(stdout));
    } catch {
      console.log(chalk.red('File not found'));
    }
  }
}

async function interactiveGitOps() {
  console.log(chalk.bold.cyan('\n🔧 Git Helpers\n'));
  
  const action = await select({
    message: 'Select operation:',
    choices: [
      { name: 'Status', value: 'status' },
      { name: 'Branches', value: 'branch' },
      { name: 'Recent commits', value: 'log' },
      { name: 'Stash changes', value: 'stash' }
    ]
  });
  
  const spinner = { succeed: () => {}, fail: () => {} };
  
  try {
    switch (action) {
      case 'status':
        const { stdout: statusOut } = await execAsync('git status --porcelain');
        if (statusOut.trim()) {
          console.log(statusOut);
        } else {
          console.log(chalk.green('✓ Working tree clean'));
        }
        break;
      case 'branch':
        const { stdout: branchOut } = await execAsync('git branch -a');
        console.log(chalk.cyan(branchOut));
        break;
      case 'log':
        const { stdout: logOut } = await execAsync('git log --oneline -5');
        console.log(logOut);
        break;
      case 'stash':
        await execAsync('git stash push -m "Quick stash via toolbox"');
        console.log(chalk.green('✓ Changes stashed'));
        break;
    }
  } catch (err) {
    console.log(chalk.red('Not a git repository or command failed'));
  }
}

async function interactiveScaffold() {
  console.log(chalk.bold.cyan('\n📦 Project Scaffolder\n'));
  
  const action = await select({
    message: 'Select template:',
    choices: [
      { name: 'Node.js (ESM)', value: 'node' },
      { name: 'TypeScript', value: 'ts' },
      { name: 'Python', value: 'python' },
      { name: 'React', value: 'react' }
    ]
  });
  
  const name = await input({ message: 'Project name:', default: 'my-project' });
  const dir = `./${name.replace(/\s+/g, '-')}`;
  
  console.log(chalk.yellow(`\nCreating ${name}...`));
  
  try {
    await fs.mkdir(dir, { recursive: true });
    await fs.writeFile(
      path.join(dir, 'package.json'),
      JSON.stringify({ name: name.toLowerCase().replace(/\s+/g, '-'), version: '1.0.0' }, null, 2)
    );
    console.log(chalk.green(`\n✓ Created: ${dir}`));
  } catch (err) {
    console.log(chalk.red(`Failed: ${err.message}`));
  }
}

async function showSysInfo() {
  console.log(chalk.bold.cyan('\n🖥️ System Info\n'));
  
  try {
    const [hostname, platform, arch] = await Promise.all([
      execAsync('hostname').then(r => r.stdout.trim()),
      execAsync('uname -s').then(r => r.stdout.trim()),
      execAsync('uname -m').then(r => r.stdout.trim())
    ]);
    
    const uptime = await execAsync('uptime -p').then(r => r.stdout.trim()).catch(() => 'unknown');
    
    console.log(`  ${chalk.cyan('Hostname:')} ${hostname}`);
    console.log(`  ${chalk.cyan('Platform:')} ${platform}`);
    console.log(`  ${chalk.cyan('Arch:')} ${arch}`);
    console.log(`  ${chalk.cyan('Uptime:')} ${uptime}`);
    
    const cpuUsage = await execAsync("top -l 1 -n 1 | grep 'CPU usage'").then(r => r.stdout.trim()).catch(() => 'N/A');
    console.log(`  ${chalk.cyan('CPU:')} ${cpuUsage}`);
  } catch (err) {
    console.log(chalk.red('Failed to get system info'));
  }
}

async function showQuickActions() {
  console.log(chalk.bold.cyan('\n🚀 Quick Actions\n'));
  
  const action = await select({
    message: 'Select action:',
    choices: [
      { name: '🔄 npm install', value: 'npm i' },
      { name: '📦 npm update', value: 'npm u' },
      { name: '🧹 Clean node_modules', value: 'clean' },
      { name: '🔍 Search node_modules', value: 'find' },
      { name: '📋 List npm scripts', value: 'scripts' }
    ]
  });
  
  try {
    switch (action) {
      case 'npm i':
        console.log(chalk.yellow('Running npm install...'));
        await execAsync('npm install');
        console.log(chalk.green('✓ Done'));
        break;
      case 'npm u':
        console.log(chalk.yellow('Running npm update...'));
        await execAsync('npm update');
        console.log(chalk.green('✓ Done'));
        break;
      case 'clean':
        await execAsync('rm -rf node_modules package-lock.json');
        console.log(chalk.green('✓ Cleaned'));
        break;
      case 'find':
        const pkg = await input({ message: 'Package name:' });
        await execAsync(`find node_modules -name "${pkg}" -type d | head -5`);
        break;
      case 'scripts':
        const { stdout } = await execAsync('cat package.json | grep -A 20 "scripts"');
        console.log(chalk.dim(stdout));
        break;
    }
  } catch (err) {
    console.log(chalk.red('Command failed or not in npm project'));
  }
}

async function showSettings() {
  console.log(chalk.bold.cyan('\n⚙️ Settings\n'));
  
  const setting = await select({
    message: 'Select setting:',
    choices: [
      { name: '🔔 Notifications', value: 'notif' },
      { name: '🎨 Theme', value: 'theme' },
      { name: '📝 Aliases', value: 'alias' },
      { name: 'ℹ️ About', value: 'about' }
    ]
  });
  
  switch (setting) {
    case 'about':
      console.log(boxen(
        chalk.bold.cyan('🧰 Toolbox CLI') + '\n\n' +
        chalk.dim('Version 1.0.0\n') +
        'A developer productivity toolkit',
        { padding: 1, borderStyle: 'round' }
      ));
      break;
    default:
      console.log(chalk.dim('Coming soon...'));
  }
}

export default { showMenu };
