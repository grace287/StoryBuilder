"use client";

import { TreeNode, TreeNodeData } from "./TreeNode";
import { Plus } from "lucide-react";

interface BinderProps {
  projectData: TreeNodeData;
  onSelectNode: (node: TreeNodeData) => void;
  selectedNodeId?: string;
}

export const Binder = ({ projectData, onSelectNode, selectedNodeId }: BinderProps) => {
  return (
    <div className="h-full flex flex-col bg-white border-r border-gray-200">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-gray-900">프로젝트 구조</h2>
          <button
            className="p-1.5 hover:bg-gray-100 rounded-lg transition-colors"
            title="새 항목 추가"
          >
            <Plus className="w-5 h-5 text-gray-600" />
          </button>
        </div>
      </div>

      {/* Tree */}
      <div className="flex-1 overflow-y-auto p-2">
        <TreeNode
          node={projectData}
          level={0}
          onSelect={onSelectNode}
          selectedId={selectedNodeId}
        />
      </div>

      {/* Stats Footer */}
      <div className="p-4 border-t border-gray-200 bg-gray-50">
        <div className="text-xs text-gray-600 space-y-1">
          <div className="flex justify-between">
            <span>총 단어 수</span>
            <span className="font-medium">{projectData.wordCount?.toLocaleString() || 0}자</span>
          </div>
          <div className="flex justify-between">
            <span>완료된 씬</span>
            <span className="font-medium">
              {countCompletedScenes(projectData)} / {countTotalScenes(projectData)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper functions
function countTotalScenes(node: TreeNodeData): number {
  if (node.type === "scene") return 1;
  if (!node.children) return 0;
  return node.children.reduce((sum, child) => sum + countTotalScenes(child), 0);
}

function countCompletedScenes(node: TreeNodeData): number {
  if (node.type === "scene" && node.status === "completed") return 1;
  if (!node.children) return 0;
  return node.children.reduce((sum, child) => sum + countCompletedScenes(child), 0);
}
