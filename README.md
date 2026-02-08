# StoryBuilder

> Narrative IDE — 작가용 Story Operating System

**Notion ❌ · Google Docs ❌**  
**Scrivener + VSCode + Notion + AI = ✔**

VSCode가 개발자에게 있듯, StoryBuilder는 작가에게.  
작가용 **개발툴** · **Narrative IDE** 수준 설계.

---

## 🎯 제품 정의

- 장편 소설·시나리오 작가를 위한 전문 집필 도구
- **4층 구조**: Editor Engine · Graph Data · AI Narrative Engine · SaaS Platform
- 작품-장-씬 계층, 인물 관계도, 타임라인, 세계관 위키 통합

---

## 🏗 최종 기술 스택 (Production)

### Frontend
- **Next.js 15+** · TypeScript
- **TipTap** (에디터) · **Zustand** · **TanStack Query**
- **Tailwind + Radix** (UI·접근성)

### Backend (Hybrid Microservice)
- **API Gateway** — NestJS or FastAPI
- **Story Engine** — FastAPI (Python)
- **AI Engine** — FastAPI (Python)

### Database
- **PostgreSQL** (Core)
- **Redis** (Realtime / Autosave)
- **Neo4j** (Graph, 선택)

### Infra
- **Turborepo** · **pnpm** · **Docker** · **GitHub Actions**
- **Vercel** (FE) · **Railway or AWS ECS** (BE) · **Cloudflare R2**

---

## 📁 프로젝트 구조 (모노레포 목표)

```
StoryBuilder/
├── .cursor/rules/     # PRD·아키텍처·프론트/백엔드 규칙
├── docs/              # ERD, 데이터 딕셔너리, MVP 로드맵
├── backend/           # FastAPI (Story Engine / API)
│   ├── models/        # SQLAlchemy
│   ├── api/           # REST 라우터
│   └── alembic/       # 마이그레이션
├── apps/
│   └── web/           # Next.js 프론트엔드
└── docker-compose.yml # Postgres, Redis, Backend
```

---

## 📊 데이터 모델 개요

```
User → Project → Chapter → Scene → Manuscript
                    ↓
                 Character (관계도)
                 Timeline (작중 시간)
                 Setting (세계관)
```

상세: [docs/erd.md](docs/erd.md) · [docs/data-dictionary.md](docs/data-dictionary.md)

---

## 🚀 빠른 시작

> ⚠️ 프론트엔드는 **`apps/`가 아니라 `apps/web/`** 안에서 실행합니다. `apps/`에는 `package.json`이 없습니다.

```bash
# 1. 인프라 + 백엔드
docker-compose up -d

# 2. API 문서
# 브라우저에서 http://localhost:8000/docs

# 3. 프론트엔드 (반드시 apps/web 기준)
cd apps/web
npm install
npm run dev
# → http://localhost:3000
```

**루트에서 한 번에 실행할 때:**
```bash
docker-compose up -d
cd apps/web && npm install && npm run dev
```

---

## 🎯 진행 상황

- ✅ ERD · SQLAlchemy 모델 · Docker · FastAPI 기본 구조 · Project CRUD
- ✅ Next.js 앱 · 바인더(계층 트리) · TipTap 에디터 · Zustand
- ⏳ TanStack Query · Radix · Turborepo/pnpm 루트 · API 연동

---

## 📖 문서

| 문서 | 설명 |
|------|------|
| [docs/erd.md](docs/erd.md) | ERD 다이어그램 |
| [docs/data-dictionary.md](docs/data-dictionary.md) | 데이터 딕셔너리 |
| [docs/mvp-roadmap.md](docs/mvp-roadmap.md) | MVP 기능 정의·Phase 1~3 |
| [docs/architecture.md](docs/architecture.md) | Hybrid 아키텍처·CTO 설계 단계 |
| [docs/scrivener-benchmark.md](docs/scrivener-benchmark.md) | 스크리브너 벤치마킹·기능 매핑 |
| [backend/README.md](backend/README.md) | 백엔드 실행·API |

---

## 🌱 로드맵 (MVP → Pro → 장기)

- **MVP**: 바인더·에디터·자동저장·캐릭터/태그 기반 설정 아카이브
- **Pro**: 타임라인 시각화·관계도 그래프·AI 플롯 분석
- **장기**: 협업·출판 포맷·Desktop(Tauri)·플랫폼 비전

---

## 🔧 개발 가이드 (Cursor)

PRD·아키텍처·스택은 `.cursor/rules/`에 반영되어 있습니다.  
- **storybuilder-prd.mdc** · **architecture.mdc** — 항상 적용  
- **frontend-standards.mdc** — `apps/web` 작업 시  
- **backend-standards.mdc** — `backend` 작업 시  
- **commit-conventions.mdc** — Git 커밋 메시지 (이모지 + 타입)  

---

**Made for writers who build worlds** 🌍✨
