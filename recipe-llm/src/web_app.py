"""
Flask-based web interface for Recipe LLM
"""

from flask import Flask, render_template_string, request, jsonify, session, send_from_directory
from recipe_llm import RecipeLLM
import os
import secrets

app = Flask(__name__, static_folder='../static')
app.secret_key = secrets.token_hex(16)

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <meta name="theme-color" content="#667eea">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Recipe LLM">
    <meta name="description" content="AI-powered recipe and cooking assistant for any dish ever made">

    <title>Recipe LLM - AI Cooking Assistant</title>

    <!-- PWA Manifest -->
    <link rel="manifest" href="/static/manifest.json">

    <!-- iOS Icons -->
    <link rel="apple-touch-icon" href="/static/icons/icon-152x152.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/static/icons/icon-72x72.png">
    <link rel="apple-touch-icon" sizes="96x96" href="/static/icons/icon-96x96.png">
    <link rel="apple-touch-icon" sizes="128x128" href="/static/icons/icon-128x128.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/static/icons/icon-144x144.png">
    <link rel="apple-touch-icon" sizes="152x152" href="/static/icons/icon-152x152.png">
    <link rel="apple-touch-icon" sizes="192x192" href="/static/icons/icon-192x192.png">
    <link rel="apple-touch-icon" sizes="384x384" href="/static/icons/icon-384x384.png">
    <link rel="apple-touch-icon" sizes="512x512" href="/static/icons/icon-512x512.png">

    <!-- Standard favicon -->
    <link rel="icon" type="image/png" sizes="32x32" href="/static/icons/icon-72x72.png">

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .main-content {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        .provider-select {
            margin-bottom: 20px;
            padding: 10px;
            display: flex;
            gap: 10px;
            align-items: center;
            background: #f5f5f5;
            border-radius: 10px;
        }

        .provider-select label {
            font-weight: bold;
        }

        .provider-select select {
            flex: 1;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
        }

        .chat-container {
            height: 500px;
            overflow-y: auto;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            background: #fafafa;
        }

        .message {
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 10px;
            max-width: 80%;
        }

        .message.user {
            background: #667eea;
            color: white;
            margin-left: auto;
            text-align: right;
        }

        .message.assistant {
            background: white;
            border: 2px solid #e0e0e0;
        }

        .message.system {
            background: #fff3cd;
            border: 2px solid #ffc107;
            text-align: center;
            max-width: 100%;
        }

        .message pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            margin: 10px 0;
            padding: 10px;
            background: #f5f5f5;
            border-radius: 5px;
            overflow-x: auto;
        }

        .input-container {
            display: flex;
            gap: 10px;
        }

        .input-container input {
            flex: 1;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 1em;
        }

        .input-container button {
            padding: 15px 30px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1em;
            cursor: pointer;
            transition: background 0.3s;
        }

        .input-container button:hover {
            background: #5568d3;
        }

        .input-container button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }

        .quick-actions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-bottom: 20px;
        }

        .quick-action {
            padding: 10px;
            background: #f0f0f0;
            border: 2px solid #ddd;
            border-radius: 8px;
            cursor: pointer;
            text-align: center;
            transition: all 0.3s;
        }

        .quick-action:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }

        .loading.active {
            display: block;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .clear-btn {
            padding: 10px 20px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-bottom: 20px;
        }

        .clear-btn:hover {
            background: #c82333;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🍳 Recipe LLM</h1>
            <p>AI-Powered Cooking Assistant - Ask me about any recipe or cooking technique!</p>
        </div>

        <div class="main-content">
            <div class="provider-select">
                <label for="provider">LLM Provider:</label>
                <select id="provider">
                    <option value="openai">OpenAI (GPT-4)</option>
                    <option value="anthropic">Anthropic Claude</option>
                    <option value="ollama">Ollama (Local)</option>
                </select>
            </div>

            <button class="clear-btn" onclick="clearChat()">Clear Chat</button>

            <div class="quick-actions">
                <div class="quick-action" onclick="quickAsk('Give me a recipe for chocolate chip cookies')">
                    🍪 Chocolate Chip Cookies
                </div>
                <div class="quick-action" onclick="quickAsk('How do I make perfect pasta carbonara?')">
                    🍝 Pasta Carbonara
                </div>
                <div class="quick-action" onclick="quickAsk('Give me a vegan dinner recipe')">
                    🥗 Vegan Dinner
                </div>
                <div class="quick-action" onclick="quickAsk('How do I cook the perfect steak?')">
                    🥩 Perfect Steak
                </div>
                <div class="quick-action" onclick="quickAsk('What can I substitute for eggs in baking?')">
                    🥚 Egg Substitutes
                </div>
                <div class="quick-action" onclick="quickAsk('Give me a quick 30-minute dinner recipe')">
                    ⏱️ Quick Dinner
                </div>
            </div>

            <div class="chat-container" id="chatContainer">
                <div class="message system">
                    Welcome! Ask me about any recipe or cooking question. I can help with recipes from any cuisine,
                    cooking techniques, ingredient substitutions, dietary adaptations, and more!
                </div>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Cooking up an answer...</p>
            </div>

            <div class="input-container">
                <input
                    type="text"
                    id="userInput"
                    placeholder="Ask about any recipe or cooking question..."
                    onkeypress="handleKeyPress(event)"
                >
                <button onclick="sendMessage()" id="sendBtn">Send</button>
            </div>
        </div>
    </div>

    <script>
        function addMessage(content, type) {
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;

            if (content.includes('\\n')) {
                const pre = document.createElement('pre');
                pre.textContent = content;
                messageDiv.appendChild(pre);
            } else {
                messageDiv.textContent = content;
            }

            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function quickAsk(question) {
            document.getElementById('userInput').value = question;
            sendMessage();
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        async function sendMessage() {
            const input = document.getElementById('userInput');
            const sendBtn = document.getElementById('sendBtn');
            const loading = document.getElementById('loading');
            const provider = document.getElementById('provider').value;

            const message = input.value.trim();
            if (!message) return;

            addMessage(message, 'user');
            input.value = '';
            sendBtn.disabled = true;
            loading.classList.add('active');

            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        question: message,
                        provider: provider
                    }),
                });

                const data = await response.json();

                if (data.error) {
                    addMessage(`Error: ${data.error}`, 'system');
                } else {
                    addMessage(data.response, 'assistant');
                }
            } catch (error) {
                addMessage(`Error: ${error.message}`, 'system');
            } finally {
                sendBtn.disabled = false;
                loading.classList.remove('active');
                input.focus();
            }
        }

        async function clearChat() {
            const chatContainer = document.getElementById('chatContainer');
            chatContainer.innerHTML = `
                <div class="message system">
                    Chat cleared! Ask me anything about recipes or cooking.
                </div>
            `;

            try {
                await fetch('/clear', { method: 'POST' });
            } catch (error) {
                console.error('Error clearing chat:', error);
            }
        }

        // Register Service Worker for PWA
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/service-worker.js')
                    .then((registration) => {
                        console.log('Service Worker registered successfully:', registration.scope);
                    })
                    .catch((error) => {
                        console.log('Service Worker registration failed:', error);
                    });
            });
        }

        // Install prompt for PWA
        let deferredPrompt;
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            console.log('PWA install prompt available');
        });
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template_string(HTML_TEMPLATE)


@app.route('/ask', methods=['POST'])
def ask():
    """Handle recipe/cooking questions."""
    try:
        data = request.json
        question = data.get('question')
        provider = data.get('provider', 'openai')

        if not question:
            return jsonify({'error': 'No question provided'}), 400

        # Get or create LLM instance for this session
        if 'llm_provider' not in session or session.get('llm_provider') != provider:
            try:
                llm = RecipeLLM(provider=provider)
                session['llm_provider'] = provider
                # Store LLM in app context (in production, use Redis or similar)
                if not hasattr(app, 'llm_instances'):
                    app.llm_instances = {}
                app.llm_instances[session.get('_id', 'default')] = llm
            except Exception as e:
                return jsonify({'error': f'Failed to initialize LLM: {str(e)}'}), 500

        # Get LLM instance
        llm = app.llm_instances.get(session.get('_id', 'default'))
        if not llm:
            llm = RecipeLLM(provider=provider)
            app.llm_instances[session.get('_id', 'default')] = llm

        # Get response
        response = llm.ask(question)

        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/clear', methods=['POST'])
def clear():
    """Clear conversation history."""
    try:
        if hasattr(app, 'llm_instances'):
            llm = app.llm_instances.get(session.get('_id', 'default'))
            if llm:
                llm.clear_history()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/service-worker.js')
def service_worker():
    """Serve the service worker file."""
    return send_from_directory('../static/js', 'service-worker.js', mimetype='application/javascript')


@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files."""
    return send_from_directory('../static', path)


def main():
    """Run the web application."""
    print("\n" + "="*60)
    print("Recipe LLM Web Interface")
    print("="*60)
    print("\nStarting server...")
    print("Open your browser to: http://localhost:5000")
    print("\nMake sure you have set your API key:")
    print("  export OPENAI_API_KEY='your-key'")
    print("  export ANTHROPIC_API_KEY='your-key'")
    print("\nOr use Ollama for local models (no API key needed)")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
