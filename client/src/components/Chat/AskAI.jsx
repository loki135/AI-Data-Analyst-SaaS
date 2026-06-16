import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';

const EXAMPLES = [
  'What is the average value in this dataset?',
  'Which category appears most frequently?',
  'Are there any outliers in the data?',
  'What trends can you spot?',
];

export default function AskAI({ datasetId }) {
  const { token } = useAuth();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (question) => {
    if (!question.trim() || loading) return;
    const userMsg = { role: 'user', text: question };
    setMessages((m) => [...m, userMsg]);
    setInput('');
    setLoading(true);
    try {
      const res = await axios.post(
        '/api/ai/ask',
        { datasetId, question },
        { headers: token ? { Authorization: `Bearer ${token}` } : {} }
      );
      setMessages((m) => [...m, { role: 'ai', text: res.data.answer }]);
    } catch (err) {
      setMessages((m) => [...m, { role: 'ai', text: 'Sorry, I could not answer that. Please try again.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(input);
  };

  return (
    <div className="card flex flex-col h-[500px]">
      <div className="flex-1 overflow-y-auto space-y-3 pb-2 min-h-0">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center">
            <p className="text-slate-500 text-sm mb-4">Ask anything about your data</p>
            <div className="flex flex-wrap gap-2 justify-center">
              {EXAMPLES.map((ex) => (
                <button
                  key={ex}
                  onClick={() => sendMessage(ex)}
                  className="text-xs bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 px-3 py-1.5 rounded-full transition-colors"
                >
                  {ex}
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`max-w-[80%] px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-brand-500 text-white rounded-br-sm'
                    : 'bg-slate-800 text-slate-200 rounded-bl-sm'
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-800 px-4 py-2.5 rounded-2xl rounded-bl-sm">
              <div className="flex gap-1">
                {[0, 1, 2].map((i) => (
                  <div
                    key={i}
                    className="w-2 h-2 bg-slate-500 rounded-full animate-bounce"
                    style={{ animationDelay: `${i * 0.15}s` }}
                  />
                ))}
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2 pt-3 border-t border-slate-800 mt-2">
        <input
          className="input flex-1"
          placeholder="Ask a question about your data..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
        />
        <button type="submit" className="btn-primary px-5" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}
