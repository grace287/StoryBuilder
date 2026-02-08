# StoryBuilder MVP 기능 정의서

**버전**: 1.0  
**작성일**: 2026-01-27  
**목표**: 스크리브너를 넘어선 현대적 작가용 IDE

---

## 🎯 MVP 개발 전략

### Phase 1: 구조적 집필 기반 (Core Structure)
**목표**: 바인더 + 에디터로 기본 집필 플로우 완성

#### 1.1 계층형 바인더 (Hierarchical Binder)
```
📁 Project
  📖 Chapter 1
    📄 Scene 1-1 [초안]
    📄 Scene 1-2 [완료]
  📖 Chapter 2
    📖 Section 2.1
      📄 Scene 2-1-1 [수정중]
```

**핵심 기능**:
- 무한 계층 구조 (Project → Chapter → Section → Scene)
- 드래그 앤 드롭 순서 변경
- 각 노드별 상태 표시 (초안/수정중/완료/보류)
- 실시간 글자 수 표시
- 아이콘 커스터마이징

**기술 스택**:
- `@dnd-kit/core` - 드래그 앤 드롭
- `lucide-react` - 아이콘
- Zustand로 트리 상태 관리

#### 1.2 스플릿 뷰 에디터 (Split View Editor)
**핵심 기능**:
- 화면 2분할 (좌측: 참조 문서, 우측: 현재 작성 중인 씬)
- 참조 문서 타입: 이전 장면, 캐릭터 카드, 타임라인, 설정집
- 독립적 스크롤 + 동기 스크롤 토글
- 반응형 리사이징

#### 1.3 포커스 모드 (Zen Mode)
**핵심 기능**:
- UI 최소화 (바인더/툴바 숨김)
- 타입라이터 스크롤 (커서 항상 중앙 고정)
- 현재 문단 강조 (나머지 희미하게)
- 단축키 `Ctrl+Shift+F`

---

### Phase 2: 설정 아카이브 (Lore Bible)
**목표**: 세계관 일관성 유지 도구

#### 2.1 캐릭터 카드 시스템
**데이터 구조**:
```typescript
interface CharacterCard {
  id: string;
  name: string;
  avatar?: string;
  role: "주인공" | "조연" | "악역";
  profile: {
    age?: number;
    appearance?: string;
    personality?: string;
    motivation?: string;
  };
  relatedScenes: string[];  // 등장 씬 ID 배열
}
```

**UI 기능**:
- 카드 그리드 뷰
- 빠른 검색 및 필터링
- 에디터 옆 사이드 패널로 고정

#### 2.2 태깅 시스템
**태그 타입**:
- `#인물:홍길동` - 특정 캐릭터 등장
- `#시점:1인칭` - 서술 시점
- `#복선:열쇠` - 복선 요소
- `#시간:2026-03-15` - 사건 발생 시각

**기능**:
- 씬 에디터에서 태그 자동완성
- 태그별 씬 필터링 뷰
- 태그 클라우드 시각화

---

### Phase 3: 분석 및 통계 (Analytics)
**목표**: 데이터 기반 집필 관리

#### 3.1 집필 대시보드
**표시 항목**:
- 📊 일일 목표 달성률 (목표: 3,000자 / 달성: 2,450자)
- 📈 최근 7일 집필량 그래프
- ⏱️ 총 집필 시간
- 📝 프로젝트별 진행률 (완료된 씬 / 전체 씬)

#### 3.2 스마트 검색
**기능**:
- 전체 프로젝트에서 정규식 검색
- 캐릭터 이름 일괄 치환
- 검색 결과를 씬 단위로 그룹화

---

## 🚀 개발 우선순위

### Week 1-2: Phase 1 (바인더 + 에디터)
- [x] 기본 CRUD API
- [ ] 계층형 트리 컴포넌트
- [ ] 드래그 앤 드롭
- [ ] 스플릿 뷰 레이아웃
- [ ] 포커스 모드

### Week 3: Phase 2 (설정 아카이브)
- [ ] 캐릭터 카드 CRUD
- [ ] 태그 모델 및 API
- [ ] 태그 UI

### Week 4: Phase 3 (분석)
- [ ] 집필 통계 API
- [ ] 대시보드 차트
- [ ] 검색 기능

---

## 💡 차별화 포인트

### StoryBuilder만의 강점
1. **타임라인 트래커** (스릴러 특화)
   - 사건 발생 시각과 원고 순서를 분리 관리
   - 시간순 정렬 vs 원고순 정렬 토글

2. **AI 어시스턴트** (향후 확장)
   - "이 씬에서 홍길동의 감정 상태는?" 
   - "앞서 언급된 복선 요소는?"
   - Claude API 기반 컨텍스트 분석

3. **협업 모드** (장편 공동 집필)
   - 실시간 동시 편집 (WebSocket)
   - 씬별 담당자 지정
   - 변경 이력 추적

---

## 📐 기술 아키텍처

### 프론트엔드 추가 컴포넌트
```
apps/web/
├── components/
│   ├── Binder/
│   │   ├── TreeNode.tsx        # 재귀적 트리 노드
│   │   ├── DragHandle.tsx      # 드래그 핸들
│   │   └── StatusBadge.tsx     # 상태 배지
│   ├── Editor/
│   │   ├── SplitView.tsx       # 분할 에디터
│   │   ├── FocusMode.tsx       # 몰입 모드
│   │   └── TypewriterScroll.ts # 타입라이터 스크롤
│   ├── Archive/
│   │   ├── CharacterCard.tsx   # 캐릭터 카드
│   │   ├── TagInput.tsx        # 태그 입력
│   │   └── TagCloud.tsx        # 태그 클라우드
│   └── Dashboard/
│       ├── StatsCard.tsx       # 통계 카드
│       └── WritingChart.tsx    # 집필량 차트
```

### 백엔드 추가 엔드포인트
```python
# backend/api/
tags.py           # 태그 CRUD
statistics.py     # 집필 통계
timeline.py       # 타임라인 이벤트
search.py         # 전체 검색
```

---

## ✅ 검증 시나리오

### 사용자 스토리: 스릴러 작가 김00
1. 프로젝트 "어둠 속의 진실" 생성
2. Chapter 1-10 구조 생성 (드래그로 순서 변경)
3. Scene 1-1 작성 중 → 우측에 캐릭터 "형사 박민준" 카드 띄움
4. `#복선:빨간신발` 태그 추가
5. Chapter 5에서 같은 태그 검색하여 앞뒤 맥락 확인
6. 대시보드에서 오늘 목표 달성 확인

---

**다음 단계**: Phase 1.1 계층형 바인더 구현 시작
