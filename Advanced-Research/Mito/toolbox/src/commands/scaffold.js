import { Command } from 'commander';
import chalk from 'chalk';
import fs from 'fs/promises';
import path from 'path';
import { log, section } from '../utils/logger.js';
import { input, select, confirm } from '@inquirer/prompts';
import ora from 'ora';

const scaffoldCmd = new Command('scaffold')
  .description('Scaffold new projects');

function createNodeTemplate(name) {
  return {
    name: 'Node.js (ESM)',
    files: {
      'package.json': JSON.stringify({
        name: name.toLowerCase().replace(/\s+/g, '-'),
        version: '1.0.0',
        type: 'module',
        main: 'src/index.js',
        scripts: {
          start: 'node src/index.js',
          dev: 'node --watch src/index.js',
          test: 'echo "No tests"'
        },
        keywords: [],
        author: '',
        license: 'MIT'
      }, null, 2),
      'src/index.js': `#!/usr/bin/env node

import chalk from 'chalk';
import { Command } from 'commander';

const program = new Command();

program
  .name('${name.toLowerCase().replace(/\s+/g, '-')}')
  .description('${name}')
  .version('1.0.0');

program.parse();
`,
      'README.md': `# ${name}\n\nBuilt with Toolbox CLI`
    }
  };
}

function createTsTemplate(name) {
  return {
    name: 'TypeScript',
    files: {
      'package.json': JSON.stringify({
        name: name.toLowerCase().replace(/\s+/g, '-'),
        version: '1.0.0',
        type: 'module',
        main: 'dist/index.js',
        scripts: {
          build: 'tsc',
          start: 'node dist/index.js',
          dev: 'tsc --watch'
        },
        keywords: [],
        author: '',
        license: 'MIT'
      }, null, 2),
      'tsconfig.json': JSON.stringify({
        compilerOptions: {
          target: 'ES2022',
          module: 'NodeNext',
          moduleResolution: 'NodeNext',
          outDir: 'dist',
          rootDir: 'src',
          strict: true
        }
      }, null, 2),
      'src/index.ts': `#!/usr/bin/env node

console.log('Hello from TypeScript!');`,
      'README.md': `# ${name}\n\nBuilt with Toolbox CLI`
    }
  };
}

function createPythonTemplate(name) {
  return {
    name: 'Python',
    files: {
      'main.py': `#!/usr/bin/env python3

def main():
    print("Hello from ${name}!")

if __name__ == "__main__":
    main()
`,
      'requirements.txt': '# Add dependencies here\n',
      'README.md': `# ${name}\n\nBuilt with Toolbox CLI`
    }
  };
}

function createReactTemplate(name) {
  return {
    name: 'React App',
    files: {
      'package.json': JSON.stringify({
        name: name.toLowerCase().replace(/\s+/g, '-'),
        version: '1.0.0',
        private: true,
        scripts: {
          dev: 'vite',
          build: 'vite build'
        },
        dependencies: {
          react: '^18.2.0',
          'react-dom': '^18.2.0'
        },
        devDependencies: {
          '@vitejs/plugin-react': '^4.0.0',
          vite: '^5.0.0'
        }
      }, null, 2),
      'vite.config.js': `import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()]
});`,
      'index.html': `<!DOCTYPE html>
<html>
<head>
  <title>${name}</title>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.jsx"></script>
</body>
</html>`,
      'src/main.jsx': `import React from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  return <h1>Hello from ${name}!</h1>;
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);`,
      'README.md': `# ${name}\n\nBuilt with Toolbox CLI`
    }
  };
}

const templateBuilders = {
  node: createNodeTemplate,
  ts: createTsTemplate,
  python: createPythonTemplate,
  react: createReactTemplate
};

scaffoldCmd
  .command('new')
  .description('Create a new project')
  .action(async () => {
    console.log(chalk.bold.cyan('\n📦 Project Scaffolder\n'));
    
    const projectName = await input({
      message: 'Project name:',
      default: 'my-project'
    });
    
    const template = await select({
      message: 'Choose template:',
      choices: [
        { name: 'Node.js (ESM)', value: 'node' },
        { name: 'TypeScript', value: 'ts' },
        { name: 'Python', value: 'python' },
        { name: 'React App', value: 'react' }
      ]
    });
    
    const addGitignore = await confirm({ message: 'Add .gitignore?', default: true });
    const addEnv = await confirm({ message: 'Add .env.example?', default: true });
    
    const selectedTemplate = templateBuilders[template](projectName);
    const spinner = ora(chalk.cyan('Creating project...')).start();
    
    try {
      const projectDir = projectName;
      await fs.mkdir(projectDir, { recursive: true });
      
      for (const [filePath, content] of Object.entries(selectedTemplate.files)) {
        const fullPath = path.join(projectDir, filePath);
        const dir = path.dirname(fullPath);
        if (dir !== projectDir) {
          await fs.mkdir(dir, { recursive: true });
        }
        await fs.writeFile(fullPath, content);
      }
      
      if (addGitignore) {
        await fs.writeFile(
          path.join(projectDir, '.gitignore'),
          'node_modules/\ndist/\n.env\n*.log\n.DS_Store\n'
        );
      }
      
      if (addEnv) {
        await fs.writeFile(
          path.join(projectDir, '.env.example'),
          'NODE_ENV=development\nAPI_KEY=\n'
        );
      }
      
      spinner.succeed(chalk.green(`\n✓ Project created: ${projectName}\n`));
      
      console.log(`  ${chalk.cyan('Template:')} ${selectedTemplate.name}`);
      console.log(`  ${chalk.cyan('Location:')} ./${projectDir}`);
      console.log();
      console.log(chalk.dim('Next steps:'));
      console.log(`  ${chalk.white(`cd ${projectDir}`)}`);
      console.log(`  ${chalk.white('npm install')}`);
      console.log(`  ${chalk.white('npm start')}`);
      
    } catch (err) {
      spinner.fail(chalk.red('Failed to create project'));
      log('error', err.message);
    }
  });

scaffoldCmd
  .command('templates')
  .description('List available templates')
  .action(() => {
    section('Available Templates');
    const templates = [
      { key: 'node', name: 'Node.js (ESM)' },
      { key: 'ts', name: 'TypeScript' },
      { key: 'python', name: 'Python' },
      { key: 'react', name: 'React App' }
    ];
    for (const t of templates) {
      console.log(`  ${chalk.cyan(t.key.padEnd(10))} ${t.name}`);
    }
  });

export default scaffoldCmd;
