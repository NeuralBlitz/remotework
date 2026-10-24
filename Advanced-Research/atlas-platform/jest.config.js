module.exports = {
preset: ‘ts-jest’,
testEnvironment: ‘node’,
roots: [’<rootDir>’],
testMatch: [’**/**tests**/**/*.ts’, ’**/?(*.)+(spec|test).ts’],
transform: {
‘^.+\.ts$’: ‘ts-jest’,
},
collectCoverageFrom: [
‘**/*.ts’,
’!**/*.d.ts’,
‘!**/node_modules/**’,
‘!**/dist/**’,
‘!**/coverage/**’,
‘!**/**tests**/**’,
],
coverageDirectory: ‘coverage’,
coverageReporters: [‘text’, ‘lcov’, ‘json’],
moduleFileExtensions: [‘ts’, ‘js’, ‘json’],
verbose: true,
};
