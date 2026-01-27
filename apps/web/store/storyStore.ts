import { create } from 'zustand'
import { Project, Chapter, Scene, Manuscript } from '@/lib/api'

interface StoryState {
  // 현재 선택된 항목
  currentProjectId: string | null
  currentChapterId: string | null
  currentSceneId: string | null

  // 데이터
  projects: Project[]
  chapters: Record<string, Chapter[]> // key: project_id
  scenes: Record<string, Scene[]>     // key: chapter_id
  currentManuscript: Manuscript | null

  // 로딩/에러 상태
  loading: boolean
  error: string | null

  // Actions
  setCurrentProject: (id: string | null) => void
  setCurrentChapter: (id: string | null) => void
  setCurrentScene: (id: string | null) => void
  
  setProjects: (projects: Project[]) => void
  setChapters: (projectId: string, chapters: Chapter[]) => void
  setScenes: (chapterId: string, scenes: Scene[]) => void
  setCurrentManuscript: (manuscript: Manuscript | null) => void
  
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
}

export const useStoryStore = create<StoryState>((set) => ({
  // 초기 상태
  currentProjectId: null,
  currentChapterId: null,
  currentSceneId: null,
  
  projects: [],
  chapters: {},
  scenes: {},
  currentManuscript: null,
  
  loading: false,
  error: null,

  // Actions
  setCurrentProject: (id) => set({ currentProjectId: id }),
  setCurrentChapter: (id) => set({ currentChapterId: id }),
  setCurrentScene: (id) => set({ currentSceneId: id }),
  
  setProjects: (projects) => set({ projects }),
  setChapters: (projectId, chapters) => 
    set((state) => ({ 
      chapters: { ...state.chapters, [projectId]: chapters } 
    })),
  setScenes: (chapterId, scenes) => 
    set((state) => ({ 
      scenes: { ...state.scenes, [chapterId]: scenes } 
    })),
  setCurrentManuscript: (manuscript) => set({ currentManuscript: manuscript }),
  
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}))
