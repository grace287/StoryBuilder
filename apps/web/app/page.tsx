'use client'

import { useState, useEffect } from 'react'
import Sidebar from '@/components/Sidebar'
import Editor from '@/components/Editor'
import { useStoryStore } from '@/store/storyStore'
import { manuscriptsAPI, scenesAPI } from '@/lib/api'
import { useWebSocketAutosave } from '@/hooks/useWebSocketAutosave'

export default function Home() {
  const [content, setContent] = useState('<p>씬을 작성하세요...</p>')
  const [saving, setSaving] = useState(false)
  const [lastSaved, setLastSaved] = useState<Date | null>(null)
  
  const { 
    currentSceneId, 
    currentManuscript,
    setCurrentManuscript,
    scenes,
    currentChapterId 
  } = useStoryStore()

  // WebSocket 자동저장
  useWebSocketAutosave({
    sceneId: currentSceneId,
    content,
    onSaved: (data) => {
      setLastSaved(new Date())
    },
    onError: (error) => {
      console.error('Autosave error:', error)
    },
  })

  // 현재 씬 정보
  const currentScene = currentChapterId && scenes[currentChapterId]
    ? scenes[currentChapterId].find(s => s.id === currentSceneId)
    : null

  // 씬 변경 시 원고 로드
  useEffect(() => {
    if (currentSceneId) {
      loadManuscript(currentSceneId)
    }
  }, [currentSceneId])

  const loadManuscript = async (sceneId: string) => {
    try {
      const response = await manuscriptsAPI.getLatest(sceneId)
      setCurrentManuscript(response.data)
      setContent(response.data.content)
    } catch (error: any) {
      if (error.response?.status === 404) {
        // 원고가 없으면 빈 내용으로 시작
        setContent('<p>씬을 작성하세요...</p>')
        setCurrentManuscript(null)
      }
    }
  }

  const handleSave = async () => {
    if (!currentSceneId) return

    try {
      setSaving(true)
      await manuscriptsAPI.autosave(currentSceneId, content)
      setLastSaved(new Date())
    } catch (error) {
      console.error('Save failed:', error)
    } finally {
      setSaving(false)
    }
  }

  const wordCount = content.replace(/<[^>]*>/g, '').split(/\s+/).filter(Boolean).length

  return (
    <div className="flex h-screen">
      <Sidebar />
      
      <div className="flex-1 flex flex-col">
        <header className="bg-white border-b border-gray-200 p-4">
          <h1 className="text-lg font-semibold">
            {currentScene?.title || '씬을 선택하세요'}
          </h1>
          {currentScene && (
            <p className="text-sm text-gray-600">
              위치: {currentScene.location || '미지정'} • 
              시간: {currentScene.scene_time ? new Date(currentScene.scene_time).toLocaleDateString() : '미지정'}
            </p>
          )}
        </header>

        <main className="flex-1 overflow-auto bg-gray-50 p-8">
          {currentSceneId ? (
            <div className="max-w-4xl mx-auto">
              <Editor
                content={content}
                onChange={setContent}
                placeholder="씬을 작성하세요..."
              />
            </div>
          ) : (
            <div className="flex items-center justify-center h-full">
              <div className="text-center text-gray-500">
                <p className="text-lg">왼쪽에서 씬을 선택하거나 새로 만드세요</p>
              </div>
            </div>
          )}
        </main>

        <footer className="bg-white border-t border-gray-200 p-4 flex justify-between items-center">
          <div className="text-sm text-gray-600">
            {saving ? (
              '저장 중...'
            ) : lastSaved ? (
              `자동 저장됨 • ${lastSaved.toLocaleTimeString()}`
            ) : (
              '변경사항 없음'
            )}
            {' • '}단어 수: {wordCount}
          </div>
          <div className="flex gap-2">
            <button 
              className="px-4 py-2 text-sm bg-gray-200 rounded hover:bg-gray-300"
              disabled={!currentSceneId}
            >
              버전 기록
            </button>
            <button 
              onClick={handleSave}
              disabled={saving || !currentSceneId}
              className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {saving ? '저장 중...' : '저장'}
            </button>
          </div>
        </footer>
      </div>
    </div>
  )
}
        <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
          <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
            To get started, edit the page.tsx file.
          </h1>
          <p className="max-w-md text-lg leading-8 text-zinc-600 dark:text-zinc-400">
            Looking for a starting point or more instructions? Head over to{" "}
            <a
              href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
              className="font-medium text-zinc-950 dark:text-zinc-50"
            >
              Templates
            </a>{" "}
            or the{" "}
            <a
              href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
              className="font-medium text-zinc-950 dark:text-zinc-50"
            >
              Learning
            </a>{" "}
            center.
          </p>
        </div>
        <div className="flex flex-col gap-4 text-base font-medium sm:flex-row">
          <a
            className="flex h-12 w-full items-center justify-center gap-2 rounded-full bg-foreground px-5 text-background transition-colors hover:bg-[#383838] dark:hover:bg-[#ccc] md:w-[158px]"
            href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Image
              className="dark:invert"
              src="/vercel.svg"
              alt="Vercel logomark"
              width={16}
              height={16}
            />
            Deploy Now
          </a>
          <a
            className="flex h-12 w-full items-center justify-center rounded-full border border-solid border-black/[.08] px-5 transition-colors hover:border-transparent hover:bg-black/[.04] dark:border-white/[.145] dark:hover:bg-[#1a1a1a] md:w-[158px]"
            href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            Documentation
          </a>
        </div>
      </main>
    </div>
  );
}
