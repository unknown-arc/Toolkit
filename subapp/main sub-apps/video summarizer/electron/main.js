const { app, BrowserWindow, Menu, dialog, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 700,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    title: 'Video Summarizer',
    show: false,
    icon: path.join(__dirname, 'icon.png') // Optional: add an icon
  });

  // Always load from localhost
  mainWindow.loadURL('http://localhost:8000');

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Open DevTools in development
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function startBackend() {
  console.log('🔧 Starting Python backend...');
  
  pythonProcess = spawn('python', ['main.py'], {
    cwd: process.cwd(),
    stdio: 'pipe'
  });

  pythonProcess.stdout.on('data', (data) => {
    console.log(`🐍 Python: ${data.toString().trim()}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`🐍 Python Error: ${data.toString().trim()}`);
  });

  pythonProcess.on('error', (err) => {
    console.error('❌ Failed to start Python backend:', err);
    dialog.showErrorBox(
      'Backend Error', 
      'Failed to start Python backend. Make sure:\n\n' +
      '1. Python is installed\n' +
      '2. All dependencies are installed (pip install -r requirements.txt)\n' +
      '3. No other app is using port 8000'
    );
  });

  pythonProcess.on('close', (code) => {
    console.log(`🐍 Python backend exited with code ${code}`);
  });
}

function stopBackend() {
  if (pythonProcess) {
    console.log('🛑 Stopping Python backend...');
    pythonProcess.kill();
    pythonProcess = null;
  }
}

function createMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Open Video...',
          accelerator: 'Ctrl+O',
          click: () => {
            mainWindow.webContents.send('open-file-dialog');
          }
        },
        { type: 'separator' },
        {
          label: 'Exit',
          accelerator: 'Ctrl+Q',
          click: () => {
            app.quit();
          }
        }
      ]
    },
    {
      label: 'Edit',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' }
      ]
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' }
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'About Video Summarizer',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'About',
              message: 'Video Summarizer',
              detail: 'A desktop application for summarizing video content.\n\nVersion 1.0.0\nBuilt with Electron + FastAPI'
            });
          }
        }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// App event handlers
app.whenReady().then(() => {
  console.log('🚀 App is ready, starting backend...');
  
  // Start Python backend first
  startBackend();
  
  // Wait a bit for backend to start, then create window
  setTimeout(() => {
    createWindow();
    createMenu();
    console.log('✅ App window created');
  }, 3000);
});

app.on('window-all-closed', () => {
  stopBackend();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

app.on('before-quit', () => {
  stopBackend();
});

// Handle file dialogs from renderer
ipcMain.handle('open-file-dialog', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile'],
    filters: [
      {
        name: 'Video Files',
        extensions: ['mp4', 'avi', 'mov', 'mkv', 'webm']
      },
      {
        name: 'All Files',
        extensions: ['*']
      }
    ]
  });
  
  return result;
});