import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import { FiSend } from 'react-icons/fi'

const sessionId = crypto.randomUUID()

function App() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const [started, setStarted] = useState(false)

  const messagesEndRef = useRef(null)

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({
      behavior: 'smooth',
    })
  }

  const addMessage = (sender, text) => {
    setMessages((prev) => [
      ...prev,
      {
        sender,
        text,
        time: new Date().toLocaleTimeString(),
      },
    ])
  }

  const api = axios.create({
    baseURL: 'http://127.0.0.1:8000',
  })

  // START CONVERSATION
  const startConversation = async () => {
    if (!input.trim()) return

    const userMessage = input

    addMessage('User', userMessage)

    setInput('')
    setLoading(true)

    try {
      const response = await api.post('/start', {
        session_id: sessionId,
        task: userMessage,
      })

      addMessage(
        response.data.agent,
        response.data.message
      )

      if (response.data.type === 'workflow') {
        setStarted(true)
      } else {
        setStarted(false)
      }
    } catch (error) {
      addMessage(
        'System',
        'Something went wrong.'
      )
    }

    setLoading(false)
  }

  const sendReply = async () => {
    if (!input.trim()) return

    const userMessage = input

    addMessage('User', userMessage)

    setInput('')
    setLoading(true)

    try {
      const response = await api.post('/reply', {
        session_id: sessionId,
        answer: userMessage,
      })

      addMessage(
        response.data.agent,
        response.data.message
      )

      if (response.data.completed) {
        setStarted(false)
      }
    } catch (error) {
      addMessage(
        'System',
        'Session expired. Start a new task.'
      )

      setStarted(false)
    }

    setLoading(false)
  }

  const handleSubmit = () => {
    if (!started) {
      startConversation()
    } else {
      sendReply()
    }
  }

  return (
    <div className="app">
      <div className="chat-container">
        <div className="header">
          <h1>AI Agent Assistant</h1>
        </div>

        <div className="messages">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`message ${
                msg.sender === 'User'
                  ? 'user-message'
                  : 'bot-message'
              }`}
            >
              <div className="message-header">
                <span>{msg.sender}</span>

                <small>{msg.time}</small>
              </div>

              <ReactMarkdown>
                {msg.text}
              </ReactMarkdown>
            </div>
          ))}

          {loading && (
            <div className="typing">
              AI Agent is typing...
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="input-box">
          <input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(e) =>
              setInput(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                handleSubmit()
              }
            }}
          />

          <button onClick={handleSubmit}>
            <FiSend />
          </button>
        </div>
      </div>
    </div>
  )
}

export default App