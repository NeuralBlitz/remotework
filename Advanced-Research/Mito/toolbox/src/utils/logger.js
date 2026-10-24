#!/usr/bin/env node

import chalk from 'chalk';
import boxen from 'boxen';

const branding = {
  title: chalk.bold.cyan('🧰 Toolbox CLI'),
  tagline: chalk.dim('Developer productivity toolkit'),
  version: 'v1.0.0'
};

export function printBanner() {
  const banner = boxen(
    `${chalk.bold.cyan(branding.title)}\n` +
    `${chalk.dim(branding.tagline)}\n` +
    `${chalk.gray('─'.repeat(40))}\n` +
    `${chalk.green('✓')} File operations\n` +
    `${chalk.green('✓')} Git helpers\n` +
    `${chalk.green('✓')} Project scaffold\n` +
    `${chalk.green('✓')} Interactive menu`,
    {
      padding: 1,
      margin: 1,
      borderStyle: 'round',
      borderColor: 'cyan'
    }
  );
  console.log(banner);
}

export function log(type, message) {
  const styles = {
    info:    { color: 'cyan',    icon: 'ℹ' },
    success: { color: 'green',   icon: '✓' },
    warning: { color: 'yellow',  icon: '⚠' },
    error:   { color: 'red',     icon: '✗' },
    title:   { color: 'magenta', icon: '▸' }
  };
  
  const { color, icon } = styles[type] || styles.info;
  console.log(`  ${chalk[color](icon)} ${chalk[color](message)}`);
}

export function section(title) {
  console.log(`\n${chalk.bold.underline.cyan(title)}`);
  console.log(chalk.dim('─'.repeat(40)));
}

export default { printBanner, log, section, chalk };
