class InstagramBotApp {
    constructor() {
        this.currentSessionId = null;
        this.statusInterval = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateStatus('idle', 'جاهز');
    }

    bindEvents() {
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

        // Form validation
        document.getElementById('numAccounts').addEventListener('input', (e) => {
            const value = parseInt(e.target.value);
            if (value > 10) {
                e.target.value = 10;
                this.showAlert('الحد الأقصى لعدد الحسابات هو 10', 'warning');
            }
        });
    }

    async startBot() {
        try {
            const numAccounts = parseInt(document.getElementById('numAccounts').value);
            const delayBetween = parseInt(document.getElementById('delayBetween').value);

            if (numAccounts < 1 || numAccounts > 10) {
                this.showAlert('يرجى إدخال عدد صحيح من الحسابات (1-10)', 'error');
                return;
            }

            // Show loading modal
            this.showLoadingModal();

            // Disable start button
            document.getElementById('startBot').disabled = true;
            document.getElementById('startBot').style.display = 'none';
            document.getElementById('stopBot').style.display = 'block';

            // Update status
            this.updateStatus('running', 'قيد التشغيل');

            // Start bot
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
                this.currentSessionId = data.session_id;
                this.showAlert('تم بدء البوت بنجاح', 'success');
                this.startStatusPolling();
            } else {
                throw new Error(data.error || 'فشل في بدء البوت');
            }

        } catch (error) {
            console.error('Error starting bot:', error);
            this.showAlert(`خطأ في بدء البوت: ${error.message}`, 'error');
            this.resetUI();
        } finally {
            this.hideLoadingModal();
        }
    }

    async stopBot() {
        try {
            if (!this.currentSessionId) {
                this.showAlert('لا يوجد بوت قيد التشغيل', 'warning');
                return;
            }

            const response = await fetch(`/api/stop_bot/${this.currentSessionId}`);
            const data = await response.json();

            if (data.success) {
                this.showAlert('تم إيقاف البوت بنجاح', 'success');
                this.updateStatus('idle', 'جاهز');
                this.resetUI();
            } else {
                throw new Error(data.error || 'فشل في إيقاف البوت');
            }

        } catch (error) {
            console.error('Error stopping bot:', error);
            this.showAlert(`خطأ في إيقاف البوت: ${error.message}`, 'error');
        }
    }

    startStatusPolling() {
        if (this.statusInterval) {
            clearInterval(this.statusInterval);
        }

        this.statusInterval = setInterval(async () => {
            if (!this.currentSessionId) {
                this.stopStatusPolling();
                return;
            }

            try {
                const response = await fetch(`/api/bot_status/${this.currentSessionId}`);
                const data = await response.json();

                if (response.ok) {
                    this.updateProgress(data.progress);
                    this.updateStatistics(data);
                    this.updateLogs(data.logs);
                    this.updateStatus(data.status, this.getStatusText(data.status));

                    if (data.status === 'completed' || data.status === 'error' || data.status === 'stopped') {
                        this.stopStatusPolling();
                        this.loadResults();
                        
                        if (data.status === 'completed') {
                            this.showAlert('تم إنشاء الحسابات بنجاح!', 'success');
                        } else if (data.status === 'error') {
                            this.showAlert('حدث خطأ أثناء إنشاء الحسابات', 'error');
                        }
                        
                        this.resetUI();
                    }
                } else {
                    console.error('Failed to get bot status:', data.error);
                }
            } catch (error) {
                console.error('Error polling status:', error);
            }
        }, 2000); // Poll every 2 seconds
    }

    stopStatusPolling() {
        if (this.statusInterval) {
            clearInterval(this.statusInterval);
            this.statusInterval = null;
        }
    }

    async loadResults() {
        try {
            if (!this.currentSessionId) return;

            const response = await fetch(`/api/get_results/${this.currentSessionId}`);
            const data = await response.json();

            if (response.ok) {
                this.displayResults(data);
            }
        } catch (error) {
            console.error('Error loading results:', error);
        }
    }

    displayResults(data) {
        const container = document.getElementById('resultsContainer');
        
        if (!data.accounts_created || data.accounts_created.length === 0) {
            container.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-info-circle"></i>
                    <p>لم يتم إنشاء أي حسابات</p>
                </div>
            `;
            return;
        }

        let html = '';
        data.accounts_created.forEach((account, index) => {
            html += `
                <div class="account-item fade-in">
                    <div class="account-header">
                        <span class="account-username">${account.username}</span>
                        <span class="account-status success">تم الإنشاء</span>
                    </div>
                    <div class="account-details">
                        <div class="account-detail">
                            <span class="detail-label">البريد الإلكتروني:</span>
                            <span class="detail-value">${account.email}</span>
                        </div>
                        <div class="account-detail">
                            <span class="detail-label">الاسم:</span>
                            <span class="detail-value">${account.first_name} ${account.last_name}</span>
                        </div>
                        <div class="account-detail">
                            <span class="detail-label">كلمة المرور:</span>
                            <span class="detail-value">${account.password}</span>
                        </div>
                    </div>
                </div>
            `;
        });

        container.innerHTML = html;
    }

    updateProgress(progress) {
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        
        progressBar.style.width = `${progress}%`;
        progressText.textContent = `${Math.round(progress)}%`;
    }

    updateStatistics(data) {
        document.getElementById('totalAccounts').textContent = data.total_accounts || 0;
        document.getElementById('successfulAccounts').textContent = data.accounts_created || 0;
        
        const successRate = data.total_accounts > 0 ? 
            Math.round((data.accounts_created / data.total_accounts) * 100) : 0;
        document.getElementById('successRate').textContent = `${successRate}%`;
        
        document.getElementById('accountsCreated').textContent = 
            `${data.accounts_created || 0} / ${data.total_accounts || 0}`;
    }

    updateLogs(logs) {
        const container = document.getElementById('logsContainer');
        
        if (!logs || logs.length === 0) return;

        // Keep only the last 50 log entries
        const recentLogs = logs.slice(-50);
        
        let html = '';
        recentLogs.forEach(log => {
            const timestamp = new Date().toLocaleTimeString('ar-SA');
            html += `
                <div class="log-entry">
                    <span class="log-time">[${timestamp}]</span>
                    <span class="log-message">${this.escapeHtml(log)}</span>
                </div>
            `;
        });

        container.innerHTML = html;
        container.scrollTop = container.scrollHeight;
    }

    updateStatus(status, text) {
        const statusDot = document.querySelector('#botStatus .status-dot');
        const statusText = document.querySelector('#botStatus .status-text');
        
        // Remove all status classes
        statusDot.classList.remove('idle', 'running', 'completed', 'error');
        
        // Add current status class
        statusDot.classList.add(status);
        statusText.textContent = text;
    }

    getStatusText(status) {
        const statusMap = {
            'idle': 'جاهز',
            'running': 'قيد التشغيل',
            'completed': 'مكتمل',
            'error': 'خطأ',
            'stopped': 'متوقف'
        };
        return statusMap[status] || 'غير معروف';
    }

    resetUI() {
        document.getElementById('startBot').disabled = false;
        document.getElementById('startBot').style.display = 'block';
        document.getElementById('stopBot').style.display = 'none';
        this.currentSessionId = null;
    }

    clearLogs() {
        document.getElementById('logsContainer').innerHTML = `
            <div class="log-entry">
                <span class="log-time">[${new Date().toLocaleTimeString('ar-SA')}]</span>
                <span class="log-message">تم مسح السجل</span>
            </div>
        `;
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

    showAlert(message, type = 'info') {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());

        // Create new alert
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert at the top of main content
        const mainContent = document.querySelector('.main-content');
        mainContent.insertBefore(alertDiv, mainContent.firstChild);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new InstagramBotApp();
});

// Add some utility functions
window.InstagramBotApp = {
    // Export for potential external use
    formatTime: (seconds) => {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },

    // Format file size
    formatFileSize: (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    // Generate random ID
    generateId: () => {
        return Math.random().toString(36).substr(2, 9);
    }
};