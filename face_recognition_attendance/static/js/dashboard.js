// Reusable UI JavaScript utilities for FaceMark AI Dashboard

// Toast Notification manager
class ToastManager {
    constructor(containerId = 'toast-container') {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            // Create container if not exists
            this.container = document.createElement('div');
            this.container.id = containerId;
            document.body.appendChild(this.container);
        }
    }

    show(title, message, type = 'info', duration = 5000) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        toast.innerHTML = `
            <div class="toast-content">
                <div class="toast-title">${title}</div>
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close">&times;</button>
        `;

        this.container.appendChild(toast);
        this.playNotificationSound(type);

        // Close event
        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.addEventListener('click', () => {
            this.dismiss(toast);
        });

        // Auto dismiss
        setTimeout(() => {
            this.dismiss(toast);
        }, duration);
    }

    dismiss(toast) {
        toast.style.opacity = '0';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }

    playNotificationSound(type) {
        try {
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            
            if (type === 'success') {
                // High double-ping
                oscillator.frequency.setValueAtTime(880, audioCtx.currentTime); // A5
                gainNode.gain.setValueAtTime(0.04, audioCtx.currentTime);
                oscillator.start();
                oscillator.stop(audioCtx.currentTime + 0.08);
                
                setTimeout(() => {
                    const osc2 = audioCtx.createOscillator();
                    const gain2 = audioCtx.createGain();
                    osc2.connect(gain2);
                    gain2.connect(audioCtx.destination);
                    osc2.frequency.setValueAtTime(1046.5, audioCtx.currentTime); // C6
                    gain2.gain.setValueAtTime(0.04, audioCtx.currentTime);
                    osc2.start();
                    osc2.stop(audioCtx.currentTime + 0.12);
                }, 80);
            } else if (type === 'error') {
                // Low error buzz
                oscillator.type = 'sawtooth';
                oscillator.frequency.setValueAtTime(130, audioCtx.currentTime);
                gainNode.gain.setValueAtTime(0.06, audioCtx.currentTime);
                oscillator.start();
                oscillator.stop(audioCtx.currentTime + 0.2);
            } else if (type === 'warning') {
                // Mid warning ping
                oscillator.frequency.setValueAtTime(440, audioCtx.currentTime); // A4
                gainNode.gain.setValueAtTime(0.04, audioCtx.currentTime);
                oscillator.start();
                oscillator.stop(audioCtx.currentTime + 0.15);
            }
        } catch (e) {
            // Audio context blocked by browser autoplay policy
        }
    }
}

// Global logger helper
function logDebug(message) {
    console.log(`[FaceMark AI] ${new Date().toISOString()}: ${message}`);
}
