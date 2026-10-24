#!/usr/bin/env node

import chalk from 'chalk';
import { Command } from 'commander';
import boxen from 'boxen';
import { showMenu } from './commands/menu.js';
import fileCmd from './commands/file.js';
import gitCmd from './commands/git.js';
import scaffoldCmd from './commands/scaffold.js';

const program = new Command();

program
  .name('toolbox')
  .description(chalk.cyan('🧰 Developer productivity toolkit'))
  .version('1.0.0');

program
  .command('menu')
  .alias('m')
  .description('Open interactive menu')
  .action(() => showMenu());

program.addCommand(fileCmd);
program.addCommand(gitCmd);
program.addCommand(scaffoldCmd);

program
  .command('info')
  .description('Show toolbox info')
  .action(() => {
    console.log(boxen(
      `${chalk.bold.cyan('🧰 Toolbox CLI')}\n\n` +
      `${chalk.green('Version:')} 1.0.0\n` +
      `${chalk.green('Commands:')}\n` +
      `  ${chalk.cyan('toolbox menu')}     Interactive menu\n` +
      `  ${chalk.cyan('toolbox file')}     File operations\n` +
      `  ${chalk.cyan('toolbox git')}      Git helpers\n` +
      `  ${chalk.cyan('toolbox scaffold')} Project scaffolding\n\n` +
      `${chalk.dim('Run any command with --help for details')}`,
      { padding: 1, borderStyle: 'round', borderColor: 'cyan' }
    ));
  });

if (process.argv.length === 2) {
  showMenu();
} else {
  program.parse();
}
