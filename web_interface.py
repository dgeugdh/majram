from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import threading
import queue
import time
import json
from instagram_bot import InstagramBot
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
CORS(app)

# Global variables for bot management
bot_queue = queue.Queue()
bot_results = {}
bot_status = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start_bot', methods=['POST'])
def start_bot():
    """Start the Instagram bot"""
    try:
        data = request.get_json()
        num_accounts = data.get('num_accounts', 1)
        
        # Generate unique session ID
        session_id = f"bot_{int(time.time())}"
        session['bot_id'] = session_id
        
        # Initialize bot status
        bot_status[session_id] = {
            'status': 'running',
            'progress': 0,
            'accounts_created': 0,
            'total_accounts': num_accounts,
            'logs': []
        }
        
        # Start bot in background thread
        thread = threading.Thread(
            target=run_bot_worker,
            args=(session_id, num_accounts)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Bot started successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bot_status/<session_id>')
def get_bot_status(session_id):
    """Get bot status and progress"""
    try:
        if session_id in bot_status:
            return jsonify(bot_status[session_id])
        else:
            return jsonify({'error': 'Session not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop_bot/<session_id>')
def stop_bot(session_id):
    """Stop the bot"""
    try:
        if session_id in bot_status:
            bot_status[session_id]['status'] = 'stopped'
            return jsonify({'success': True, 'message': 'Bot stopped'})
        else:
            return jsonify({'error': 'Session not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_results/<session_id>')
def get_results(session_id):
    """Get bot results"""
    try:
        if session_id in bot_results:
            return jsonify(bot_results[session_id])
        else:
            return jsonify({'error': 'Results not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_bot_worker(session_id, num_accounts):
    """Worker function to run the bot"""
    try:
        bot_status[session_id]['logs'].append('Starting Instagram bot...')
        
        created_accounts = []
        
        for i in range(num_accounts):
            if bot_status[session_id]['status'] == 'stopped':
                bot_status[session_id]['logs'].append('Bot stopped by user')
                break
            
            bot_status[session_id]['logs'].append(f'Creating account {i+1}/{num_accounts}...')
            
            # Create bot instance
            bot = InstagramBot()
            
            # Run account creation
            result = bot.run_account_creation()
            
            if result:
                created_accounts.append(result)
                bot_status[session_id]['accounts_created'] += 1
                bot_status[session_id]['logs'].append(f'Account {i+1} created successfully: {result["username"]}')
            else:
                bot_status[session_id]['logs'].append(f'Failed to create account {i+1}')
            
            # Update progress
            progress = ((i + 1) / num_accounts) * 100
            bot_status[session_id]['progress'] = progress
            
            # Small delay between accounts
            time.sleep(2)
        
        # Store results
        bot_results[session_id] = {
            'accounts_created': created_accounts,
            'total_attempted': num_accounts,
            'success_rate': len(created_accounts) / num_accounts if num_accounts > 0 else 0
        }
        
        bot_status[session_id]['status'] = 'completed'
        bot_status[session_id]['logs'].append('Bot completed successfully')
        
    except Exception as e:
        bot_status[session_id]['status'] = 'error'
        bot_status[session_id]['logs'].append(f'Error: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)