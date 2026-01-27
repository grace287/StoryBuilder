'use client'

import { useState } from 'react'

interface Project {
  id: string
  title: string
  chapters: Chapter[]
}

interface Chapter {
  id: string
  title: string
  scenes: Scene[]
}

interface Scene {
  id: string
  title: string
}

export default function Sidebar() {
  const [projects, setProjects] = useState<Project[]>([
    {
      id: '1',
      title: '어둠 속의 빛',
      chapters: [
        {
          id: 'c1',
          title: '1장. 깨어남',
          scenes: [
            { id: 's1', title: '씬 1: 냉동실' },
            { id: 's2', title: '씬 2: 함장실' },
          ],
        },
      ],
    },
  ])

  const [expandedChapters, setExpandedChapters] = useState<Set<string>>(new Set())

  const toggleChapter = (chapterId: string) => {
    setExpandedChapters(prev => {
      const next = new Set(prev)
      if (next.has(chapterId)) {
        next.delete(chapterId)
      } else {
        next.add(chapterId)
      }
      return next
    })
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
        {projects.map(project => (
          <div key={project.id} className="mb-4">
            <div className="font-semibold text-gray-900 mb-2">{project.title}</div>
            
            {project.chapters.map(chapter => (
              <div key={chapter.id} className="ml-2 mb-2">
                <button
                  onClick={() => toggleChapter(chapter.id)}
                  className="w-full text-left flex items-center gap-2 py-1 hover:bg-gray-200 rounded px-2"
                >
                  <span>{expandedChapters.has(chapter.id) ? '▼' : '▶'}</span>
                  <span className="text-sm">{chapter.title}</span>
                </button>

                {expandedChapters.has(chapter.id) && (
                  <div className="ml-6 mt-1">
                    {chapter.scenes.map(scene => (
                      <button
                        key={scene.id}
                        className="w-full text-left py-1 px-2 text-sm text-gray-600 hover:bg-gray-200 rounded"
                      >
                        {scene.title}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            ))}

            <button className="ml-4 text-sm text-blue-600 hover:underline">
              + 장 추가
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
