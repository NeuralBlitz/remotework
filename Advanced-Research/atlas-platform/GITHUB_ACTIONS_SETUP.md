# GitHub Actions Setup Guide

## Problem: “Dependencies lock file is not found”

This error occurs when GitHub Actions tries to cache npm dependencies but can’t find `package-lock.json`.

## Solution

### Step 1: Ensure Lock File Exists

The repository now includes `package-lock.json`. If you need to regenerate it:

```bash
npm install --package-lock-only
```

Or do a full install:

```bash
npm install
```

### Step 2: Commit the Lock File

```bash
git add package-lock.json
git commit -m "Add package-lock.json for GitHub Actions caching"
git push
```

### Step 3: Verify GitHub Actions Configuration

The `.github/workflows/ci.yml` file is configured correctly:

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: 20.x
    cache: 'npm'  # This enables caching
```

## Alternative: Disable Cache (Not Recommended)

If you want to disable caching temporarily:

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: 20.x
    # Remove the cache line
```

Then change the install command from:

```yaml
- name: Install dependencies
  run: npm ci
```

To:

```yaml
- name: Install dependencies
  run: npm install
```

## Best Practices

1. **Always commit lock files** (`package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`)
1. **Use `npm ci` instead of `npm install`** in CI/CD for faster, more reliable installs
1. **Enable caching** to speed up workflows
1. **Use matrix strategy** to test against multiple Node.js versions

## Complete CI/CD Workflow

The project includes a complete CI/CD pipeline that:

1. ✅ Runs on push to `main` or `develop` branches
1. ✅ Tests against Node.js 18.x and 20.x
1. ✅ Caches npm dependencies for faster builds
1. ✅ Runs linting with ESLint
1. ✅ Runs tests with Jest
1. ✅ Generates coverage reports
1. ✅ Builds the TypeScript project
1. ✅ Uploads build artifacts

## Verifying the Fix

After committing `package-lock.json`, your GitHub Actions should show:

```
Run actions/setup-node@v4
  with:
    node-version: 20.x
    cache: npm
Found in cache @ /opt/hostedtoolcache/node/20.19.6/x64
Cache restored from key: setup-node-Linux-npm-abc123...
```

## File Checklist

Ensure these files are in your repository:

- ✅ `package.json` - Project configuration
- ✅ `package-lock.json` - Dependency lock file
- ✅ `.github/workflows/ci.yml` - GitHub Actions workflow
- ✅ `tsconfig.json` - TypeScript configuration
- ✅ `.eslintrc.js` - ESLint configuration
- ✅ `.prettierrc.json` - Prettier configuration
- ✅ `jest.config.js` - Jest configuration
- ✅ `.gitignore` - Git ignore patterns

## Troubleshooting

### Issue: Cache not being used

**Symptoms:**

```
Cache not found for input keys: setup-node-Linux-npm-...
```

**Solution:**

- Ensure `package-lock.json` is committed
- Check that file hasn’t been added to `.gitignore`
- Verify the cache key hasn’t changed

### Issue: npm ci fails

**Error:**

```
npm ERR! The `npm ci` command can only install with an existing package-lock.json
```

**Solution:**

1. Generate lock file: `npm install`
1. Commit it: `git add package-lock.json && git commit -m "Add lock file"`

### Issue: Build fails after cache restore

**Solution:**

1. Clear GitHub Actions cache in repository settings
1. Re-run the workflow
1. If still failing, try `npm install` instead of `npm ci`

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [setup-node Action](https://github.com/actions/setup-node)
- [npm ci Documentation](https://docs.npmjs.com/cli/v8/commands/npm-ci)
- [Package Lock Documentation](https://docs.npmjs.com/cli/v8/configuring-npm/package-lock-json)
