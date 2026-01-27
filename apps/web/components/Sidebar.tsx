'use client'

import { useEffect, useState } from 'react'
import { useStoryStore } from '@/store/storyStore'
import { projectsAPI, chaptersAPI, scenesAPI } from '@/lib/api'

export default function Sidebar() {
  const {
    projects,
    chapters,
    scenes,
    currentProjectId,
    currentChapterId,
    currentSceneId,
    setProjects,
    setChapters,
    setScenes,
    setCurrentProject,
    setCurrentChapter,
    setCurrentScene,
    setLoading,
    setError,
  } = useStoryStore()

  const [expandedProjects, setExpandedProjects] = useState<Set<string>>(new Set())
  const [expandedChapters, setExpandedChapters] = useState<Set<string>>(new Set())

  // 초기 데이터 로드
  useEffect(() => {
    loadProjects()
  }, [])

  // 작품 선택 시 장 로드
  useEffect(() => {
    if (currentProjectId) {
      loadChapters(currentProjectId)
      setExpandedProjects(prev => new Set(prev).add(currentProjectId))
    }
  }, [currentProjectId])

  // 장 선택 시 씬 로드
  useEffect(() => {
    if (currentChapterId) {
      loadScenes(currentChapterId)
      setExpandedChapters(prev => new Set(prev).add(currentChapterId))
    }
  }, [currentChapterId])

  const loadProjects = async () => {
    try {
      setLoading(true)
      const response = await projectsAPI.list()
      setProjects(response.data)
      setError(null)
    } catch (error: any) {
      setError(error.message)
    } finally {
      setLoading(false)
    }
  }

  const loadChapters = async (projectId: string) => {
    try {
      const response = await chaptersAPI.listByProject(projectId)
      setChapters(projectId, response.data)
    } catch (error: any) {
      console.error('Failed to load chapters:', error)
    }
  }

  const loadScenes = async (chapterId: string) => {
    try {
      const response = await scenesAPI.listByChapter(chapterId)
      setScenes(chapterId, response.data)
    } catch (error: any) {
      console.error('Failed to load scenes:', error)
    }
  }

  const toggleProject = (projectId: string) => {
    setExpandedProjects(prev => {
      const next = new Set(prev)
      if (next.has(projectId)) {
        next.delete(projectId)
      } else {
        next.add(projectId)
        setCurrentProject(projectId)
      }
      return next
    })
  }

  const toggleChapter = (chapterId: string) => {
    setExpandedChapters(prev => {
      const next = new Set(prev)
      if (next.has(chapterId)) {
        next.delete(chapterId)
      } else {
        next.add(chapterId)
        setCurrentChapter(chapterId)
      }
      return next
    })
  }

  const handleSceneClick = (sceneId: string) => {
    setCurrentScene(sceneId)
  }

  return (
    <div className="w-64 bg-gray-50 border-r border-gray-200 h-screen overflow-y-auto">
      <div className="p-4">
        <h2 className="text-xl font-bold mb-4">StoryBuilder</h2>
        <button className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700">
          + 새 작품
        </button>
      </div>

      <div className="px-4">
        {projects.map(project => {
          const projectChapters = chapters[project.id] || []
          
          return (
            <div key={project.id} className="mb-4">
              <button
                onClick={() => toggleProject(project.id)}
                className={`w-full text-left flex items-center gap-2 py-2 px-2 rounded hover:bg-gray-200 ${
                  currentProjectId === project.id ? 'bg-gray-200 font-semibold' : ''
                }`}
              >
                <span>{expandedProjects.has(project.id) ? '▼' : '▶'}</span>
                <span>{project.title}</span>
              </button>

              {expandedProjects.has(project.id) && (
                <div className="ml-4 mt-1">
                  {projectChapters.map(chapter => {
                    const chapterScenes = scenes[chapter.id] || []
                    
                    return (
                      <div key={chapter.id} className="mb-2">
                        <button
                          onClick={() => toggleChapter(chapter.id)}
                          className={`w-full text-left flex items-center gap-2 py-1 px-2 rounded hover:bg-gray-200 ${
                            currentChapterId === chapter.id ? 'bg-gray-200' : ''
                          }`}
                        >
                          <span className="text-xs">{expandedChapters.has(chapter.id) ? '▼' : '▶'}</span>
                          <span className="text-sm">{chapter.title}</span>
                        </button>

                        {expandedChapters.has(chapter.id) && (
                          <div className="ml-6 mt-1">
                            {chapterScenes.map(scene => (
                              <button
                                key={scene.id}
                                onClick={() => handleSceneClick(scene.id)}
                                className={`w-full text-left py-1 px-2 text-sm rounded hover:bg-gray-200 ${
                                  currentSceneId === scene.id ? 'bg-blue-100 text-blue-700' : 'text-gray-600'
                                }`}
                              >
                                {scene.title || `씬 ${scene.order_index}`}
                              </button>
                            ))}
                          </div>
                        )}
                      </div>
                    )
                  })}

                  <button className="ml-4 text-sm text-blue-600 hover:underline">
                    + 장 추가
                  </button>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
