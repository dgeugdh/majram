// Instagram Bot Web Interface JavaScript

class InstagramBotUI {
    constructor() {
        this.currentSessionId = null;
        this.statusInterval = null;
        this.startTime = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Start bot button
        document.getElementById('startBot').addEventListener('click', () => {
            this.startBot();
        });

        // Stop bot button
        document.getElementById('stopBot').addEventListener('click', () => {
            this.stopBot();
        });

        // Clear logs button
        document.getElementById('clearLogs').addEventListener('click', () => {
            this.clearLogs();
        });

        // Export results button
        document.getElementById('exportResults').addEventListener('click', () => {
            this.exportResults();
        });

        // Number of accounts input validation
        document.getElementById('numAccounts').addEventListener('input', (e) => {
            const value = parseInt(e.target.value);
            if (value > 10) {
                e.target.value = 10;
            } else if (value < 1) {
                e.target.value = 1;
            }
        });
    }

    async startBot() {
        const numAccounts = parseInt(document.getElementById('numAccounts').value);
        
        if (numAccounts < 1 || numAccounts > 10) {
            this.showNotification('يرجى إدخال عدد صحيح بين 1 و 10', 'error');
            return;
        }

        try {
            // Show loading modal
            const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
            loadingModal.show();

            // Disable start button
            document.getElementById('startBot').disabled = true;

            const response = await fetch('/api/start_bot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    num_accounts: numAccounts
                })
            });

            const data = await response.json();

            if (data.success) {
                this.currentSessionId = data.session_id;
                this.startTime = new Date();
                this.startStatusPolling();
                this.showNotification('تم بدء البوت بنجاح', 'success');
                this.updateUIForRunningState();
            } else {
                this.showNotification('فشل في بدء البوت: ' + data.error, 'error');
            }

        } catch (error) {
            this.showNotification('خطأ في الاتصال: ' + error.message, 'error');
        } finally {
            // Hide loading modal
            const loadingModal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
            if (loadingModal) {
                loadingModal.hide();
            }
        }
    }

    async stopBot() {
        if (!this.currentSessionId) return;

        try {
            const response = await fetch(`/api/stop_bot/${this.currentSessionId}`);
            const data = await response.json();

            if (data.success) {
                this.showNotification('تم إيقاف البوت', 'warning');
                this.updateUIForStoppedState();
            } else {
                this.showNotification('فشل في إيقاف البوت: ' + data.error, 'error');
            }

        } catch (error) {
            this.showNotification('خطأ في الاتصال: ' + error.message, 'error');
        }
    }

    startStatusPolling() {
        if (this.statusInterval) {
            clearInterval(this.statusInterval);
        }

        this.statusInterval = setInterval(async () => {
            await this.updateStatus();
        }, 2000);
    }

    async updateStatus() {
        if (!this.currentSessionId) return;

        try {
            const response = await fetch(`/api/bot_status/${this.currentSessionId}`);
            const status = await response.json();

            if (status.error) {
                console.error('Status error:', status.error);
                return;
            }

            this.updateStatusUI(status);
            this.updateLogs(status.logs);
            this.updateStatistics(status);

            // Check if bot is completed or stopped
            if (status.status === 'completed' || status.status === 'stopped' || status.status === 'error') {
                this.stopStatusPolling();
                this.updateUIForCompletedState(status.status);
                
                // Get final results
                await this.loadResults();
            }

        } catch (error) {
            console.error('Failed to update status:', error);
        }
    }

    updateStatusUI(status) {
        const statusElement = document.getElementById('botStatus');
        const progressBar = document.getElementById('progressBar');
        const progressBarInner = progressBar.querySelector('.progress-bar');

        // Update status text
        let statusText = 'جاهز';
        let statusColor = 'var(--success-color)';

        switch (status.status) {
            case 'running':
                statusText = 'جاري العمل...';
                statusColor = 'var(--warning-color)';
                break;
            case 'completed':
                statusText = 'مكتمل';
                statusColor = 'var(--success-color)';
                break;
            case 'stopped':
                statusText = 'متوقف';
                statusColor = 'var(--danger-color)';
                break;
            case 'error':
                statusText = 'خطأ';
                statusColor = 'var(--danger-color)';
                break;
        }

        statusElement.textContent = statusText;
        statusElement.style.color = statusColor;

        // Update progress bar
        if (status.progress > 0) {
            progressBar.style.display = 'block';
            progressBarInner.style.width = status.progress + '%';
            progressBarInner.setAttribute('aria-valuenow', status.progress);
        } else {
            progressBar.style.display = 'none';
        }
    }

    updateLogs(logs) {
        const logsContainer = document.getElementById('logsContainer');
        
        // Clear existing logs
        logsContainer.innerHTML = '';

        // Add new logs
        logs.forEach(log => {
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry fade-in';
            
            const time = new Date().toLocaleTimeString('ar-SA');
            logEntry.innerHTML = `
                <span class="log-time">[${time}]</span>
                <span class="log-message">${log}</span>
            `;
            
            logsContainer.appendChild(logEntry);
        });

        // Scroll to bottom
        logsContainer.scrollTop = logsContainer.scrollHeight;
    }

    updateStatistics(status) {
        // Update accounts created
        document.getElementById('accountsCreated').textContent = status.accounts_created || 0;

        // Update success rate
        const successRate = status.total_accounts > 0 ? 
            Math.round((status.accounts_created / status.total_accounts) * 100) : 0;
        document.getElementById('successRate').textContent = successRate + '%';

        // Update total time
        if (this.startTime) {
            const elapsed = Math.floor((new Date() - this.startTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            document.getElementById('totalTime').textContent = 
                `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
    }

    async loadResults() {
        if (!this.currentSessionId) return;

        try {
            const response = await fetch(`/api/get_results/${this.currentSessionId}`);
            const results = await response.json();

            if (results.error) {
                console.error('Results error:', results.error);
                return;
            }

            this.displayResults(results);

        } catch (error) {
            console.error('Failed to load results:', error);
        }
    }

    displayResults(results) {
        const resultsContainer = document.getElementById('resultsContainer');
        
        if (!results.accounts_created || results.accounts_created.length === 0) {
            resultsContainer.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-inbox"></i>
                    <p>لا توجد حسابات منشأة</p>
                </div>
            `;
            return;
        }

        let resultsHTML = '';
        
        results.accounts_created.forEach((account, index) => {
            resultsHTML += `
                <div class="account-item fade-in">
                    <div class="account-header">
                        <span class="account-username">@${account.username}</span>
                        <span class="account-status status-success">نجح</span>
                    </div>
                    <div class="account-details">
                        <div>البريد الإلكتروني: ${account.email}</div>
                        <div>الاسم: ${account.first_name} ${account.last_name}</div>
                        <div>كلمة المرور: ${account.password}</div>
                    </div>
                </div>
            `;
        });

        resultsContainer.innerHTML = resultsHTML;
    }

    updateUIForRunningState() {
        document.getElementById('startBot').style.display = 'none';
        document.getElementById('stopBot').style.display = 'block';
        document.getElementById('numAccounts').disabled = true;
    }

    updateUIForStoppedState() {
        document.getElementById('startBot').style.display = 'block';
        document.getElementById('stopBot').style.display = 'none';
        document.getElementById('startBot').disabled = false;
        document.getElementById('numAccounts').disabled = false;
    }

    updateUIForCompletedState(status) {
        this.updateUIForStoppedState();
        
        if (status === 'completed') {
            this.showNotification('تم إنشاء الحسابات بنجاح!', 'success');
        } else if (status === 'error') {
            this.showNotification('حدث خطأ أثناء إنشاء الحسابات', 'error');
        }
    }

    stopStatusPolling() {
        if (this.statusInterval) {
            clearInterval(this.statusInterval);
            this.statusInterval = null;
        }
    }

    clearLogs() {
        const logsContainer = document.getElementById('logsContainer');
        logsContainer.innerHTML = `
            <div class="log-entry">
                <span class="log-time">[${new Date().toLocaleTimeString('ar-SA')}]</span>
                <span class="log-message">تم مسح السجل</span>
            </div>
        `;
    }

    exportResults() {
        if (!this.currentSessionId) {
            this.showNotification('لا توجد نتائج للتصدير', 'warning');
            return;
        }

        // Create CSV content
        const resultsContainer = document.getElementById('resultsContainer');
        const accountItems = resultsContainer.querySelectorAll('.account-item');
        
        if (accountItems.length === 0) {
            this.showNotification('لا توجد نتائج للتصدير', 'warning');
            return;
        }

        let csvContent = 'Username,Email,First Name,Last Name,Password,Status\n';
        
        accountItems.forEach(item => {
            const username = item.querySelector('.account-username').textContent.replace('@', '');
            const details = item.querySelectorAll('.account-details div');
            const email = details[0].textContent.replace('البريد الإلكتروني: ', '');
            const name = details[1].textContent.replace('الاسم: ', '');
            const password = details[2].textContent.replace('كلمة المرور: ', '');
            const status = item.querySelector('.account-status').textContent;
            
            csvContent += `"${username}","${email}","${name.split(' ')[0]}","${name.split(' ')[1] || ''}","${password}","${status}"\n`;
        });

        // Create and download file
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', `instagram_accounts_${new Date().toISOString().split('T')[0]}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        this.showNotification('تم تصدير النتائج بنجاح', 'success');
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            direction: rtl;
        `;
        
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new InstagramBotUI();
});

// Add some utility functions
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}