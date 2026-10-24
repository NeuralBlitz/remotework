import { Command } from 'commander';
import chalk from 'chalk';
import { exec } from 'child_process';
import { promisify } from 'util';
import { log, section } from '../utils/logger.js';
import { select, confirm } from '@inquirer/prompts';
import ora from 'ora';

const execAsync = promisify(exec);
const gitCmd = new Command('git')
  .description('Git helper commands');

async function runGit(cmd) {
  try {
    const { stdout } = await execAsync(cmd, { encoding: 'utf-8' });
    return { success: true, output: stdout.trim() };
  } catch (err) {
    return { success: false, output: err.message };
  }
}

gitCmd
  .command('status')
  .description('Show git status')
  .option('-s, --short', 'Short format')
  .action(async (options) => {
    const spinner = ora(chalk.cyan('Checking git status...')).start();
    const result = await runGit('git status --porcelain');
    
    if (!result.success) {
      spinner.fail(chalk.red('Not a git repository'));
      return;
    }
    
    spinner.stop();
    
    const lines = result.output.split('\n').filter(Boolean);
    
    if (lines.length === 0) {
      log('success', 'Working tree clean ✓');
      return;
    }
    
    console.log(chalk.dim('─'.repeat(50)));
    for (const line of lines) {
      const status = line.slice(0, 2);
      const file = line.slice(3);
      
      let statusColor = chalk.white;
      if (status.includes('M')) statusColor = chalk.yellow;
      if (status.includes('?')) statusColor = chalk.gray;
      if (status.includes('D')) statusColor = chalk.red;
      if (status.includes('A')) statusColor = chalk.green;
      
      console.log(`  ${chalk[statusColor](status)} ${file}`);
    }
    console.log(chalk.dim('─'.repeat(50)));
    
    log('info', `${lines.length} file(s) changed`);
  });

gitCmd
  .command('branch')
  .description('List git branches')
  .action(async () => {
    const spinner = ora(chalk.cyan('Fetching branches...')).start();
    
    const [current, all] = await Promise.all([
      runGit('git branch --show-current'),
      runGit('git branch -a --format="%(refname:short)"')
    ]);
    
    spinner.stop();
    
    if (!current.success) {
      spinner.fail(chalk.red('Not a git repository'));
      return;
    }
    
    section('Git Branches');
    
    const branches = all.output.split('\n').filter(Boolean);
    const currentBranch = current.output;
    
    for (const branch of branches) {
      const isCurrent = branch === currentBranch;
      const marker = isCurrent ? chalk.green('●') : ' ';
      const style = isCurrent ? chalk.bold.green : chalk.white;
      const remote = branch.includes('remotes/') ? chalk.gray(' (remote)') : '';
      
      console.log(`  ${marker} ${style(branch.replace('remotes/origin/', ''))}${remote}`);
    }
  });

gitCmd
  .command('log')
  .description('Show recent commits')
  .option('-n, --count <n>', 'Number of commits', '5')
  .action(async (options) => {
    const spinner = ora(chalk.cyan('Fetching commits...')).start();
    const cmd = `git log --oneline -${options.count}`;
    const result = await runGit(cmd);
    
    spinner.stop();
    
    if (!result.success) {
      log('error', 'Failed to fetch commits');
      return;
    }
    
    section('Recent Commits');
    
    const commits = result.output.split('\n').filter(Boolean);
    for (const commit of commits) {
      const [hash, ...msg] = commit.split(' ');
      console.log(`  ${chalk.gray(hash.slice(0, 7))} ${msg.join(' ')}`);
    }
  });

gitCmd
  .command('stash')
  .description('Stash or pop changes')
  .action(async () => {
    const action = await select({
      message: 'Stash action:',
      choices: [
        { name: 'Save changes', value: 'save' },
        { name: 'List stashes', value: 'list' },
        { name: 'Pop last stash', value: 'pop' },
        { name: 'Apply last stash', value: 'apply' }
      ]
    });
    
    const spinner = ora(chalk.cyan('Working...')).start();
    
    switch (action) {
      case 'save':
        const msg = await runGit('git stash push -m "Quick stash"');
        spinner.succeed(chalk.green('Changes stashed ✓'));
        break;
      case 'list':
        spinner.stop();
        const list = await runGit('git stash list');
        console.log(list.output || 'No stashes');
        break;
      case 'pop':
        await runGit('git stash pop');
        spinner.succeed(chalk.green('Stash applied ✓'));
        break;
      case 'apply':
        await runGit('git stash apply');
        spinner.succeed(chalk.green('Stash applied ✓'));
        break;
    }
  });

gitCmd
  .command('clean')
  .description('Clean untracked files')
  .action(async () => {
    const confirmClean = await confirm({
      message: 'Remove all untracked files?',
      default: false
    });
    
    if (!confirmClean) {
      log('info', 'Cancelled');
      return;
    }
    
    const spinner = ora(chalk.cyan('Cleaning...')).start();
    await runGit('git clean -fd');
    spinner.succeed(chalk.green('Cleaned ✓'));
  });

export default gitCmd;
