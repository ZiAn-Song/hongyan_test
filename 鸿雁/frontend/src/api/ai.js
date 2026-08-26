import request from './request'

export function searchContent(query, topK = 5) {
  return request.get('/ai/search', { params: { q: query, top_k: topK } })
}

export function indexContent() {
  return request.post('/ai/index')
}

export function chat(message, onChunk, { useRag = false } = {}) {
  const token = localStorage.getItem('access_token')
  return fetch('/api/ai/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    },
    body: JSON.stringify({ message, use_rag: useRag })
  }).then(async (response) => {
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop()
      for (const line of lines) {
        if (line.startsWith('data:')) {
          const data = line.slice(5).trim()
          if (data && onChunk) {
            onChunk(data)
          }
        }
      }
    }
  })
}
