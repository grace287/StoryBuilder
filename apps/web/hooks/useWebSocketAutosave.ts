import { useEffect, useRef, useCallback } from 'react'

const WS_URL = process.env.NEXT_PUBLIC_API_URL?.replace('http', 'ws') || 'ws://localhost:8000'

interface UseWebSocketAutosaveProps {
  sceneId: string | null
  content: string
  onSaved?: (data: { word_count: number; saved_at: string }) => void
  onError?: (error: string) => void
  interval?: number // milliseconds
}

export function useWebSocketAutosave({
  sceneId,
  content,
  onSaved,
  onError,
  interval = 2000, // 2초
}: UseWebSocketAutosaveProps) {
  const wsRef = useRef<WebSocket | null>(null)
  const intervalRef = useRef<NodeJS.Timeout | null>(null)
  const lastContentRef = useRef<string>(content)

  const sendSave = useCallback(() => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return
    if (!sceneId) return
    if (content === lastContentRef.current) return // 변경사항 없으면 저장 안 함

    wsRef.current.send(JSON.stringify({
      action: 'save',
      content,
    }))

    lastContentRef.current = content
  }, [sceneId, content])

  useEffect(() => {
    if (!sceneId) {
      // 씬 선택 안 됨 - WebSocket 끊기
      if (wsRef.current) {
        wsRef.current.close()
        wsRef.current = null
      }
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
        intervalRef.current = null
      }
      return
    }

    // WebSocket 연결
    const ws = new WebSocket(`${WS_URL}/api/ws/scene/${sceneId}`)

    ws.onopen = () => {
      console.log('WebSocket connected for scene:', sceneId)
      
      // 자동저장 interval 시작
      intervalRef.current = setInterval(() => {
        sendSave()
      }, interval)
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      
      if (data.status === 'saved') {
        onSaved?.(data)
      } else if (data.status === 'error') {
        onError?.(data.message)
      }
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
      onError?.('WebSocket connection error')
    }

    ws.onclose = () => {
      console.log('WebSocket disconnected')
    }

    wsRef.current = ws

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [sceneId, interval])

  // content 변경 시 ref 업데이트
  useEffect(() => {
    if (content !== lastContentRef.current) {
      lastContentRef.current = content
    }
  }, [content])

  return {
    sendSave, // 수동 저장용
  }
}
