const { spawn } = require('child_process');
const { app } = require('electron');

console.log('🎬 Starting Video Summarizer App...');

// Start Python backend
console.log('🐍 Starting Python backend...');
const pythonProcess = spawn('python', ['main.py'], {
  cwd: __dirname,
  stdio: 'inherit'
});

pythonProcess.on('error', (err) => {
  console.error('❌ Failed to start Python backend:', err);
  process.exit(1);
});

// Wait for backend to start, then start Electron
setTimeout(() => {
  console.log('⚡ Starting Electron app...');
  const electronProcess = spawn('electron', ['.'], {
    cwd: __dirname,
    stdio: 'inherit'
  });

  electronProcess.on('close', () => {
    console.log('🛑 Stopping Python backend...');
    pythonProcess.kill();
    process.exit(0);
  });
}, 3000);

// Handle app termination
process.on('SIGINT', () => {
  console.log('🛑 Received interrupt signal, shutting down...');
  pythonProcess.kill();
  process.exit(0);
});