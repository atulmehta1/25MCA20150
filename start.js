import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Ensure Windows System32 is in PATH to prevent spawn ENOENT issues
if (process.platform === 'win32') {
  const system32 = 'C:\\Windows\\System32';
  const windowsDir = 'C:\\Windows';
  const currentPath = process.env.PATH || '';
  if (!currentPath.toLowerCase().includes('system32')) {
    process.env.PATH = `${system32};${windowsDir};${currentPath}`;
  }
  if (!process.env.ComSpec) {
    process.env.ComSpec = `${system32}\\cmd.exe`;
  }
}

console.log('====================================================');
console.log('🚀 Starting FocusForge — Smart Study & Productivity Hub');
console.log('====================================================');
console.log('📡 Backend API Server:  http://localhost:5000');
console.log('💻 Frontend Web App:     http://localhost:5173');
console.log('👤 Demo Login Email:     alex@focusforge.com');
console.log('🔑 Demo Login Password:  password123');
console.log('----------------------------------------------------');

const nodeExec = process.execPath;

// Start Express Backend
const serverProcess = spawn(nodeExec, [path.join(__dirname, 'server', 'server.js')], {
  cwd: path.join(__dirname, 'server'),
  env: process.env,
  stdio: 'inherit',
});

// Start Vite Frontend Client (direct node invocation on vite binary avoids cmd.exe spawn dependency)
const viteBin = path.join(__dirname, 'client', 'node_modules', 'vite', 'bin', 'vite.js');
const clientProcess = spawn(nodeExec, [viteBin, '--port', '5173', '--host'], {
  cwd: path.join(__dirname, 'client'),
  env: process.env,
  stdio: 'inherit',
});

serverProcess.on('error', (err) => {
  console.error('❌ Server process failed to start:', err.message);
});

clientProcess.on('error', (err) => {
  console.error('❌ Client process failed to start:', err.message);
});

const cleanup = () => {
  console.log('\n🛑 Shutting down FocusForge...');
  try {
    serverProcess.kill();
  } catch (e) {}
  try {
    clientProcess.kill();
  } catch (e) {}
  process.exit(0);
};

process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);
process.on('exit', cleanup);
