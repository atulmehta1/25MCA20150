const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

console.log('========================================================');
console.log(' FaceMark AI - Smart Face Recognition Attendance System');
console.log('========================================================');
console.log('[*] Note: This project backend is powered by Python Flask & OpenCV.');
console.log('[*] Forwarding execution to Python application...\n');

const projectDir = __dirname;
const appPyPath = path.join(projectDir, 'app.py');

if (!fs.existsSync(appPyPath)) {
    console.error(`[-] Error: Could not find app.py at ${appPyPath}`);
    process.exit(1);
}

function launchPython(pythonCmd) {
    const proc = spawn(pythonCmd, ['app.py'], {
        cwd: projectDir,
        stdio: 'inherit',
        shell: true
    });

    proc.on('error', (err) => {
        if (pythonCmd === 'python') {
            launchPython('py');
        } else {
            console.error('\n[-] Failed to start Python process:');
            console.error(err.message);
            console.error('\nPlease ensure Python is installed and added to your system PATH.');
            console.error('You can also run the project directly by double-clicking: run.bat');
        }
    });

    proc.on('close', (code) => {
        if (code !== 0 && code !== null) {
            console.log(`\nProcess exited with code ${code}`);
        }
    });
}

launchPython('python');
