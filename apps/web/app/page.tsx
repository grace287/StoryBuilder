'use client'

import { useState } from 'react'
import { Binder } from '@/components/Binder'
import type { TreeNodeData } from '@/components/Binder/TreeNode'
import Editor from '@/components/Editor'

// Mock data for testing
const mockProjectData: TreeNodeData = {
  id: 'project-1',
  title: '어둠 속의 진실',
  type: 'project',
  wordCount: 45230,
  children: [
    {
      id: 'chapter-1',
      title: '제1장: 시작',
      type: 'chapter',
      wordCount: 12500,
      children: [
        {
          id: 'scene-1-1',
          title: '사건 발생',
          type: 'scene',
          status: 'completed',
          wordCount: 3200,
        },
        {
          id: 'scene-1-2',
          title: '현장 도착',
          type: 'scene',
          status: 'in-progress',
          wordCount: 2800,
        },
      ],
    },
    {
      id: 'chapter-2',
      title: '제2장: 조사',
      type: 'chapter',
      wordCount: 18500,
      children: [
        {
          id: 'scene-2-1',
          title: '증거 분석',
          type: 'scene',
          status: 'draft',
          wordCount: 0,
        },
      ],
    },
  ],
}

export default function Home() {
  const [content, setContent] = useState('<p>씬을 선택하세요...</p>')
  const [selectedNode, setSelectedNode] = useState<TreeNodeData | null>(null)

  const handleSelectNode = (node: TreeNodeData) => {
    setSelectedNode(node)
    if (node.type === 'scene') {
      setContent(`<h1>${node.title}</h1><p>여기에 내용을 작성하세요...</p>`)
    }
  }

  const wordCount = content.replace(/<[^>]*>/g, '').split(/\s+/).filter(Boolean).length

  return (
    <div className="flex h-screen">
      <div className="w-80">
        <Binder
          projectData={mockProjectData}
          onSelectNode={handleSelectNode}
          selectedNodeId={selectedNode?.id}
        />
      </div>

      <div className="flex-1 flex flex-col">
        <header className="bg-white border-b border-gray-200 p-4">
          <h1 className="text-lg font-semibold">
            {selectedNode?.title || '씬을 선택하세요'}
          </h1>
          {selectedNode?.type === 'scene' && (
            <p className="text-sm text-gray-500 mt-1">
              상태: {selectedNode.status} • 글자 수: {selectedNode.wordCount?.toLocaleString()}
            </p>
          )}
        </header>

        <main className="flex-1 overflow-auto bg-gray-50 p-8">
          {selectedNode?.type === 'scene' ? (
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
                <p className="text-lg">왼쪽에서 씬을 선택하세요</p>
              </div>
            </div>
          )}
        </main>

        <footer className="bg-white border-t border-gray-200 p-4">
          <div className="text-sm text-gray-600">
            단어 수: {wordCount}
          </div>
        </footer>
      </div>
    </div>
  )
}
