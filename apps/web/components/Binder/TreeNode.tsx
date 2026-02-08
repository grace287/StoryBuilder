"use client";

import { ChevronRight, ChevronDown, FileText, FolderClosed, FolderOpen } from "lucide-react";
import { useState } from "react";

export type TreeNodeType = "project" | "chapter" | "scene";

export type TreeNodeStatus = "draft" | "in-progress" | "completed" | "on-hold";

export interface TreeNodeData {
  id: string;
  title: string;
  type: TreeNodeType;
  status?: TreeNodeStatus;
  wordCount?: number;
  children?: TreeNodeData[];
}

interface TreeNodeProps {
  node: TreeNodeData;
  level: number;
  onSelect: (node: TreeNodeData) => void;
  selectedId?: string;
}

const StatusBadge = ({ status }: { status?: TreeNodeStatus }) => {
  if (!status) return null;

  const colors = {
    draft: "bg-gray-200 text-gray-700",
    "in-progress": "bg-blue-200 text-blue-700",
    completed: "bg-green-200 text-green-700",
    "on-hold": "bg-yellow-200 text-yellow-700",
  };

  const labels = {
    draft: "초안",
    "in-progress": "작업중",
    completed: "완료",
    "on-hold": "보류",
  };

  return (
    <span className={`px-2 py-0.5 text-xs rounded-full ${colors[status]}`}>
      {labels[status]}
    </span>
  );
};

export const TreeNode = ({ node, level, onSelect, selectedId }: TreeNodeProps) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const hasChildren = node.children && node.children.length > 0;
  const isSelected = node.id === selectedId;

  const getIcon = () => {
    if (node.type === "scene") {
      return <FileText className="w-4 h-4 text-gray-600" />;
    }
    return isExpanded && hasChildren ? (
      <FolderOpen className="w-4 h-4 text-blue-600" />
    ) : (
      <FolderClosed className="w-4 h-4 text-gray-600" />
    );
  };

  return (
    <div className="select-none">
      <div
        className={`
          flex items-center gap-2 px-2 py-1.5 rounded cursor-pointer
          hover:bg-gray-100 transition-colors
          ${isSelected ? "bg-blue-50 border-l-2 border-blue-500" : ""}
        `}
        style={{ paddingLeft: `${level * 20 + 8}px` }}
        onClick={() => onSelect(node)}
      >
        {hasChildren && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              setIsExpanded(!isExpanded);
            }}
            className="p-0.5 hover:bg-gray-200 rounded"
          >
            {isExpanded ? (
              <ChevronDown className="w-4 h-4" />
            ) : (
              <ChevronRight className="w-4 h-4" />
            )}
          </button>
        )}
        
        {!hasChildren && <div className="w-5" />}
        
        {getIcon()}
        
        <span className="flex-1 text-sm font-medium truncate">{node.title}</span>
        
        {node.wordCount !== undefined && (
          <span className="text-xs text-gray-500">{node.wordCount.toLocaleString()}자</span>
        )}
        
        <StatusBadge status={node.status} />
      </div>

      {isExpanded && hasChildren && (
        <div>
          {node.children!.map((child) => (
            <TreeNode
              key={child.id}
              node={child}
              level={level + 1}
              onSelect={onSelect}
              selectedId={selectedId}
            />
          ))}
        </div>
      )}
    </div>
  );
};
