import { Command } from 'commander';
import chalk from 'chalk';
import fs from 'fs/promises';
import path from 'path';
import { log, section } from '../utils/logger.js';
import { input, confirm } from '@inquirer/prompts';
import ora from 'ora';

const fileCmd = new Command('file')
  .description('File operations');

fileCmd
  .command('list')
  .description('List files in a directory')
  .argument('[dir]', 'Directory path', '.')
  .option('-a, --all', 'Show hidden files')
  .option('-l, --long', 'Long format with details')
  .action(async (dir, options) => {
    const spinner = ora(chalk.cyan('Reading directory...')).start();
    
    try {
      const files = await fs.readdir(dir, { withFileTypes: true });
      spinner.succeed(chalk.green('Directory contents:'));
      
      for (const file of files) {
        if (!options.all && file.name.startsWith('.')) continue;
        
        const icon = file.isDirectory() ? '📁' : '📄';
        const name = file.isDirectory() ? chalk.blue(file.name) : chalk.white(file.name);
        
        if (options.long) {
          const stats = await fs.stat(path.join(dir, file.name));
          const size = formatSize(stats.size);
          console.log(`  ${icon} ${chalk.gray(size.padStart(8))} ${name}`);
        } else {
          console.log(`  ${icon} ${name}`);
        }
      }
    } catch (err) {
      spinner.fail(chalk.red('Failed to read directory'));
      log('error', err.message);
    }
  });

fileCmd
  .command('read')
  .description('Read file contents')
  .argument('<file>', 'File to read')
  .option('-l, --lines <n>', 'Number of lines', '50')
  .action(async (file, options) => {
    const spinner = ora(chalk.cyan('Reading file...')).start();
    
    try {
      const content = await fs.readFile(file, 'utf-8');
      const lines = content.split('\n').slice(0, parseInt(options.lines));
      
      spinner.succeed(chalk.green(`File: ${file}`));
      
      console.log(chalk.dim('─'.repeat(50)));
      lines.forEach((line, i) => {
        console.log(`${chalk.gray(String(i + 1).padStart(4))}  ${line}`);
      });
      console.log(chalk.dim('─'.repeat(50)));
    } catch (err) {
      spinner.fail(chalk.red('Failed to read file'));
      log('error', err.message);
    }
  });

fileCmd
  .command('create')
  .description('Create a new file')
  .argument('<file>', 'File path to create')
  .action(async (file) => {
    const content = await input({ 
      message: 'Enter file content (or press Enter for empty):',
      default: ''
    });
    
    try {
      await fs.writeFile(file, content);
      log('success', `Created: ${file}`);
    } catch (err) {
      log('error', err.message);
    }
  });

fileCmd
  .command('info')
  .description('Get file/directory information')
  .argument('<path>', 'Path to inspect')
  .action(async (p) => {
    section(`Info: ${p}`);
    
    try {
      const stats = await fs.stat(p);
      
      console.log(`  ${chalk.cyan('Type:')}    ${stats.isDirectory() ? 'Directory' : 'File'}`);
      console.log(`  ${chalk.cyan('Size:')}    ${formatSize(stats.size)}`);
      console.log(`  ${chalk.cyan('Created:')} ${stats.birthtime.toLocaleString()}`);
      console.log(`  ${chalk.cyan('Modified:')} ${stats.mtime.toLocaleString()}`);
      console.log(`  ${chalk.cyan('Accessed:')} ${stats.atime.toLocaleString()}`);
    } catch (err) {
      log('error', err.message);
    }
  });

function formatSize(bytes) {
  const units = ['B', 'KB', 'MB', 'GB'];
  let size = bytes;
  let unit = 0;
  while (size >= 1024 && unit < units.length - 1) {
    size /= 1024;
    unit++;
  }
  return `${size.toFixed(1)} ${units[unit]}`;
}

export default fileCmd;
