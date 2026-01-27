# StoryBuilder

> 작가용 IDE - 장편 서사 집필 도구

VSCode가 개발자에게 있듯, StoryBuilder는 작가에게.

## 🎯 프로젝트 개요

장편 소설, 시나리오 작가를 위한 전문 집필 도구.
작품-장-씬 구조로 체계적 관리, 인물 관계도, 타임라인, 세계관 위키를 통합.

## 🏗 기술 스택

### Frontend
- Next.js + TypeScript
- TipTap (에디터)
- React Flow (관계도)
- TailwindCSS

### Backend
- FastAPI + Python
- PostgreSQL (작품 데이터)
- Redis (실시간 저장)

### Infrastructure
- Docker Compose
- Alembic (마이그레이션)

## 🚀 빠른 시작

```bash
# 전체 시스템 시작
docker-compose up -d

# API 문서: http://localhost:8000/docs
```

## 📁 프로젝트 구조

```
storybuilder/
├── docs/              # ERD, 데이터 딕셔너리
├── backend/           # FastAPI 서버
│   ├── models/       # SQLAlchemy 모델
│   ├── api/          # REST API
│   └── alembic/      # DB 마이그레이션
├── apps/             # (예정) Next.js 프론트엔드
└── docker-compose.yml
```

## 📊 데이터 구조

```
User → Project → Chapter → Scene → Manuscript
                     ↓
                  Character (관계도)
                  Timeline (작중 시간)
                  Setting (세계관)
```

자세한 내용: [docs/erd.md](docs/erd.md)

## 🎯 현재 진행 상황

✅ ERD 설계 완료  
✅ SQLAlchemy 모델 완성  
✅ Docker 인프라 세팅  
✅ FastAPI 백엔드 기본 구조  
✅ Project CRUD API 구현  
⏳ Next.js 프론트엔드 (다음 단계)

## 📖 문서

- [ERD 다이어그램](docs/erd.md)
- [데이터 딕셔너리](docs/data-dictionary.md)
- [Backend README](backend/README.md)

## 🌱 로드맵

### Phase 1 (MVP)
- [x] 데이터 설계
- [x] 백엔드 기본 구조
- [ ] 에디터 UI
- [ ] 자동저장
- [ ] 캐릭터 관리

### Phase 2
- [ ] 타임라인 시각화
- [ ] 관계도 그래프
- [ ] AI 플롯 분석

### Phase 3
- [ ] 협업 기능
- [ ] 출판 포맷 변환
- [ ] Desktop 앱 (Tauri)

---

**Made for writers who build worlds** 🌍✨