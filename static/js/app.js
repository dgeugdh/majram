// Instagram Bot Web Interface JavaScript

class InstagramBotUI {
    constructor() {
        this.isRunning = false;
        this.statusInterval = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateCurrentTime();
        this.startStatusPolling();
        this.addLogEntry('Bot interface initialized', 'info');
    }

    bindEvents() {
        // Start button
        document.getElementById('startBtn').addEventListener('click', () => {
            this.startBot();
        });

        // Stop button
        document.getElementById('stopBtn').addEventListener('click', () => {
            this.stopBot();
        });

        // Clear log button
        document.getElementById('clearLog').addEventListener('click', () => {
            this.clearLog();
        });

        // Update current time every second
        setInterval(() => {
            this.updateCurrentTime();
        }, 1000);
    }

    updateCurrentTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        document.getElementById('currentTime').textContent = timeString;
    }

    async startBot() {
        if (this.isRunning) {
            this.addLogEntry('Bot is already running', 'warning');
            return;
        }

        const numAccounts = parseInt(document.getElementById('numAccounts').value);
        const delayBetween = parseInt(document.getElementById('delayBetween').value);

        if (numAccounts < 1 || numAccounts > 10) {
            this.addLogEntry('Invalid number of accounts (1-10)', 'error');
            return;
        }

        if (delayBetween < 5 || delayBetween > 60) {
            this.addLogEntry('Invalid delay between accounts (5-60 seconds)', 'error');
            return;
        }

        this.addLogEntry(`Starting bot with ${numAccounts} accounts...`, 'info');
        this.showLoadingModal();

        try {
            const response = await fetch('/api/start_bot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    num_accounts: numAccounts,
                    delay_between: delayBetween
                })
            });

            const data = await response.json();

            if (data.success) {
                this.isRunning = true;
                this.updateButtonStates();
                this.addLogEntry('Bot started successfully', 'success');
                this.hideLoadingModal();
            } else {
                this.addLogEntry(`Failed to start bot: ${data.message}`, 'error');
                this.hideLoadingModal();
            }
        } catch (error) {
            this.addLogEntry(`Error starting bot: ${error.message}`, 'error');
            this.hideLoadingModal();
        }
    }

    async stopBot() {
        if (!this.isRunning) {
            this.addLogEntry('Bot is not running', 'warning');
            return;
        }

        this.addLogEntry('Stopping bot...', 'info');

        try {
            const response = await fetch('/api/stop_bot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (data.success) {
                this.isRunning = false;
                this.updateButtonStates();
                this.addLogEntry('Bot stopped successfully', 'success');
            } else {
                this.addLogEntry(`Failed to stop bot: ${data.message}`, 'error');
            }
        } catch (error) {
            this.addLogEntry(`Error stopping bot: ${error.message}`, 'error');
        }
    }

    updateButtonStates() {
        const startBtn = document.getElementById('startBtn');
        const stopBtn = document.getElementById('stopBtn');

        if (this.isRunning) {
            startBtn.disabled = true;
            stopBtn.disabled = false;
            startBtn.innerHTML = '<i class="fas fa-play"></i> Running...';
            stopBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Bot';
        } else {
            startBtn.disabled = false;
            stopBtn.disabled = true;
            startBtn.innerHTML = '<i class="fas fa-play"></i> Start Bot';
            stopBtn.innerHTML = '<i class="fas fa-stop"></i> Stopped';
        }
    }

    showLoadingModal() {
        const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
        modal.show();
    }

    hideLoadingModal() {
        const modal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
        if (modal) {
            modal.hide();
        }
    }

    addLogEntry(message, type = 'info') {
        const logDisplay = document.getElementById('logDisplay');
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${type}`;
        
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        
        logEntry.innerHTML = `
            <span class="log-time">[${timeString}]</span>
            <span class="log-message">${message}</span>
        `;
        
        logDisplay.appendChild(logEntry);
        logDisplay.scrollTop = logDisplay.scrollHeight;
        
        // Add fade-in animation
        logEntry.classList.add('fade-in');
    }

    clearLog() {
        const logDisplay = document.getElementById('logDisplay');
        logDisplay.innerHTML = '';
        this.addLogEntry('Log cleared', 'info');
    }

    startStatusPolling() {
        this.statusInterval = setInterval(() => {
            this.updateStatus();
        }, 2000); // Poll every 2 seconds
    }

    stopStatusPolling() {
        if (this.statusInterval) {
            clearInterval(this.statusInterval);
            this.statusInterval = null;
        }
    }

    async updateStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();

            // Update status display
            document.getElementById('botStatus').textContent = data.status || 'Unknown';
            document.getElementById('accountsCreated').textContent = data.accounts_created || 0;
            document.getElementById('botMessage').textContent = data.message || '';

            // Update running state based on status
            if (data.status === 'running' || data.status === 'starting') {
                this.isRunning = true;
            } else if (data.status === 'stopped' || data.status === 'completed' || data.status === 'error') {
                this.isRunning = false;
            }

            this.updateButtonStates();

            // Update status indicator
            this.updateStatusIndicator(data.status);

            // Update accounts list
            this.updateAccountsList();

        } catch (error) {
            console.error('Error updating status:', error);
        }
    }

    updateStatusIndicator(status) {
        const statusElement = document.getElementById('botStatus');
        const currentIndicator = statusElement.querySelector('.status-indicator');
        
        if (currentIndicator) {
            currentIndicator.remove();
        }

        const indicator = document.createElement('span');
        indicator.className = 'status-indicator';
        
        switch (status) {
            case 'running':
            case 'starting':
                indicator.classList.add('running');
                break;
            case 'stopped':
            case 'completed':
            case 'error':
                indicator.classList.add('stopped');
                break;
            default:
                indicator.classList.add('idle');
        }

        statusElement.insertBefore(indicator, statusElement.firstChild);
    }

    async updateAccountsList() {
        try {
            const response = await fetch('/api/accounts');
            const data = await response.json();

            const accountsList = document.getElementById('accountsList');
            
            if (data.accounts && data.accounts.length > 0) {
                accountsList.innerHTML = '';
                
                data.accounts.forEach((account, index) => {
                    const accountItem = document.createElement('div');
                    accountItem.className = 'account-item fade-in';
                    
                    accountItem.innerHTML = `
                        <div class="account-header">
                            <span class="account-username">@${account.username}</span>
                            <span class="account-status">Created</span>
                        </div>
                        <div class="account-details">
                            <div><strong>Email:</strong> ${account.email}</div>
                            <div><strong>Name:</strong> ${account.first_name} ${account.last_name}</div>
                            <div><strong>Password:</strong> ${'*'.repeat(account.password.length)}</div>
                        </div>
                    `;
                    
                    accountsList.appendChild(accountItem);
                });
            } else {
                accountsList.innerHTML = `
                    <div class="no-accounts">
                        <i class="fas fa-users"></i>
                        <p>No accounts created yet</p>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error updating accounts list:', error);
        }
    }

    // Utility functions
    showNotification(message, type = 'info') {
        // Create a simple notification
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
}

// Initialize the UI when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.instagramBotUI = new InstagramBotUI();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Page is hidden, reduce polling frequency
        if (window.instagramBotUI) {
            window.instagramBotUI.stopStatusPolling();
        }
    } else {
        // Page is visible, resume polling
        if (window.instagramBotUI) {
            window.instagramBotUI.startStatusPolling();
        }
    }
});

// Handle beforeunload event
window.addEventListener('beforeunload', () => {
    if (window.instagramBotUI) {
        window.instagramBotUI.stopStatusPolling();
    }
});