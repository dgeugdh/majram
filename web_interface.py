from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import threading
import time
import json
import os
from instagram_bot import InstagramBot
from temp_email_service import MockEmailService
import logging
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
CORS(app)

# Global variables for bot management
bot_instances = {}
bot_status = {}

class BotManager:
    def __init__(self):
        self.bots = {}
        self.email_service = MockEmailService()
    
    def create_bot_instance(self, session_id):
        """Create a new bot instance for a session"""
        bot = InstagramBot()
        self.bots[session_id] = {
            'bot': bot,
            'email_service': self.email_service,
            'status': 'idle',
            'accounts_created': 0,
            'current_task': None
        }
        return bot
    
    def get_bot_instance(self, session_id):
        """Get bot instance for a session"""
        if session_id not in self.bots:
            return self.create_bot_instance(session_id)
        return self.bots[session_id]['bot']
    
    def update_status(self, session_id, status, message=""):
        """Update bot status"""
        if session_id in self.bots:
            self.bots[session_id]['status'] = status
            self.bots[session_id]['message'] = message
    
    def get_status(self, session_id):
        """Get current bot status"""
        if session_id in self.bots:
            return {
                'status': self.bots[session_id]['status'],
                'message': self.bots[session_id].get('message', ''),
                'accounts_created': self.bots[session_id]['accounts_created']
            }
        return {'status': 'not_found', 'message': 'Bot not found'}

bot_manager = BotManager()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/start_bot', methods=['POST'])
def start_bot():
    """Start the Instagram bot"""
    try:
        data = request.get_json()
        num_accounts = data.get('num_accounts', 1)
        
        if 'session_id' not in session:
            session['session_id'] = str(int(time.time()))
        
        session_id = session['session_id']
        
        # Create bot instance
        bot = bot_manager.create_bot_instance(session_id)
        
        # Start bot in background thread
        thread = threading.Thread(
            target=run_bot_task,
            args=(session_id, num_accounts)
        )
        thread.daemon = True
        thread.start()
        
        bot_manager.update_status(session_id, 'starting', 'Bot is starting...')
        
        return jsonify({
            'success': True,
            'message': 'Bot started successfully',
            'session_id': session_id
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error starting bot: {str(e)}'
        })

@app.route('/api/stop_bot', methods=['POST'])
def stop_bot():
    """Stop the Instagram bot"""
    try:
        session_id = session.get('session_id')
        if session_id and session_id in bot_manager.bots:
            bot_manager.update_status(session_id, 'stopping', 'Stopping bot...')
            
            # Close the bot driver
            bot = bot_manager.bots[session_id]['bot']
            bot.close_driver()
            
            bot_manager.update_status(session_id, 'stopped', 'Bot stopped')
            
            return jsonify({
                'success': True,
                'message': 'Bot stopped successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No active bot found'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error stopping bot: {str(e)}'
        })

@app.route('/api/status')
def get_status():
    """Get current bot status"""
    session_id = session.get('session_id')
    if session_id:
        status = bot_manager.get_status(session_id)
        return jsonify(status)
    else:
        return jsonify({'status': 'no_session', 'message': 'No active session'})

@app.route('/api/accounts')
def get_accounts():
    """Get created accounts list"""
    session_id = session.get('session_id')
    if session_id and session_id in bot_manager.bots:
        accounts = bot_manager.bots[session_id].get('accounts', [])
        return jsonify({'accounts': accounts})
    else:
        return jsonify({'accounts': []})

def run_bot_task(session_id, num_accounts):
    """Run the bot task in background"""
    try:
        bot_manager.update_status(session_id, 'running', 'Setting up browser...')
        
        bot = bot_manager.bots[session_id]['bot']
        email_service = bot_manager.bots[session_id]['email_service']
        
        # Setup driver
        if not bot.setup_driver():
            bot_manager.update_status(session_id, 'error', 'Failed to setup browser driver')
            return
        
        bot_manager.update_status(session_id, 'running', 'Browser ready, starting account creation...')
        
        accounts_created = []
        
        for i in range(num_accounts):
            if bot_manager.bots[session_id]['status'] == 'stopping':
                break
            
            bot_manager.update_status(session_id, 'running', f'Creating account {i+1}/{num_accounts}...')
            
            # Generate user data
            user_data = bot.generate_random_user_data()
            user_data['email'] = email_service.generate_email()
            
            # Create account
            if bot.create_instagram_account(user_data):
                accounts_created.append(user_data)
                bot_manager.bots[session_id]['accounts_created'] += 1
                bot_manager.update_status(session_id, 'running', f'Account {i+1} created successfully!')
            else:
                bot_manager.update_status(session_id, 'running', f'Failed to create account {i+1}')
            
            # Wait between accounts
            time.sleep(random.randint(5, 15))
        
        # Store created accounts
        bot_manager.bots[session_id]['accounts'] = accounts_created
        
        if len(accounts_created) > 0:
            bot_manager.update_status(session_id, 'completed', f'Successfully created {len(accounts_created)} accounts!')
        else:
            bot_manager.update_status(session_id, 'completed', 'No accounts were created successfully.')
    
    except Exception as e:
        bot_manager.update_status(session_id, 'error', f'Error during bot execution: {str(e)}')
        logging.error(f"Bot error: {e}")

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)