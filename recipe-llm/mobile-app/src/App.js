/**
 * Recipe LLM Mobile App
 * AI-powered recipe and cooking assistant
 */

import React, {useState} from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
  ActivityIndicator,
} from 'react-native';

// Import API client
import {askRecipeLLM} from './api/recipeLLM';

const App = () => {
  const [messages, setMessages] = useState([
    {
      type: 'system',
      content:
        'Welcome! Ask me about any recipe or cooking question. I can help with recipes from any cuisine, cooking techniques, ingredient substitutions, and more!',
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);

  const quickActions = [
    {emoji: '🍪', text: 'Chocolate Chip Cookies'},
    {emoji: '🍝', text: 'Pasta Carbonara'},
    {emoji: '🥗', text: 'Vegan Dinner'},
    {emoji: '🥩', text: 'Perfect Steak'},
  ];

  const sendMessage = async text => {
    if (!text.trim() || loading) return;

    const userMessage = {type: 'user', content: text};
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setLoading(true);

    try {
      const response = await askRecipeLLM(text);
      const assistantMessage = {type: 'assistant', content: response};
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        type: 'system',
        content: `Error: ${error.message}`,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickAction = text => {
    sendMessage(`Give me a recipe for ${text}`);
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#667eea" />

      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>🍳 Recipe LLM</Text>
        <Text style={styles.headerSubtitle}>AI Cooking Assistant</Text>
      </View>

      {/* Quick Actions */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        style={styles.quickActionsContainer}>
        {quickActions.map((action, index) => (
          <TouchableOpacity
            key={index}
            style={styles.quickAction}
            onPress={() => handleQuickAction(action.text)}>
            <Text style={styles.quickActionEmoji}>{action.emoji}</Text>
            <Text style={styles.quickActionText}>{action.text}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* Messages */}
      <ScrollView style={styles.messagesContainer}>
        {messages.map((message, index) => (
          <View
            key={index}
            style={[
              styles.message,
              message.type === 'user' && styles.userMessage,
              message.type === 'assistant' && styles.assistantMessage,
              message.type === 'system' && styles.systemMessage,
            ]}>
            <Text
              style={[
                styles.messageText,
                message.type === 'user' && styles.userMessageText,
              ]}>
              {message.content}
            </Text>
          </View>
        ))}
        {loading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="small" color="#667eea" />
            <Text style={styles.loadingText}>Cooking up an answer...</Text>
          </View>
        )}
      </ScrollView>

      {/* Input */}
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="Ask about any recipe or cooking question..."
          value={inputText}
          onChangeText={setInputText}
          onSubmitEditing={() => sendMessage(inputText)}
          editable={!loading}
        />
        <TouchableOpacity
          style={[styles.sendButton, loading && styles.sendButtonDisabled]}
          onPress={() => sendMessage(inputText)}
          disabled={loading}>
          <Text style={styles.sendButtonText}>Send</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#667eea',
    padding: 20,
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
  },
  headerSubtitle: {
    fontSize: 16,
    color: 'white',
    opacity: 0.9,
  },
  quickActionsContainer: {
    backgroundColor: 'white',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  quickAction: {
    backgroundColor: '#f0f0f0',
    borderRadius: 20,
    paddingVertical: 8,
    paddingHorizontal: 15,
    marginHorizontal: 5,
    flexDirection: 'row',
    alignItems: 'center',
  },
  quickActionEmoji: {
    fontSize: 20,
    marginRight: 5,
  },
  quickActionText: {
    fontSize: 14,
    color: '#333',
  },
  messagesContainer: {
    flex: 1,
    padding: 10,
  },
  message: {
    marginVertical: 5,
    padding: 12,
    borderRadius: 10,
    maxWidth: '80%',
  },
  userMessage: {
    backgroundColor: '#667eea',
    alignSelf: 'flex-end',
  },
  assistantMessage: {
    backgroundColor: 'white',
    alignSelf: 'flex-start',
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  systemMessage: {
    backgroundColor: '#fff3cd',
    alignSelf: 'center',
    borderWidth: 1,
    borderColor: '#ffc107',
  },
  messageText: {
    fontSize: 15,
    color: '#333',
  },
  userMessageText: {
    color: 'white',
  },
  loadingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 15,
  },
  loadingText: {
    marginLeft: 10,
    color: '#666',
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 10,
    backgroundColor: 'white',
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  input: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    borderRadius: 20,
    paddingHorizontal: 15,
    paddingVertical: 10,
    marginRight: 10,
    fontSize: 15,
  },
  sendButton: {
    backgroundColor: '#667eea',
    borderRadius: 20,
    paddingHorizontal: 20,
    paddingVertical: 10,
    justifyContent: 'center',
  },
  sendButtonDisabled: {
    backgroundColor: '#ccc',
  },
  sendButtonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 15,
  },
});

export default App;
