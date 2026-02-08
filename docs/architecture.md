# StoryBuilder 아키텍처

> PRD 확정 기술 스택 및 CTO 설계 단계 정리

---

## Hybrid 구조 (확정)

| 레이어 | 역할 | 스택 |
|--------|------|------|
| Editor Engine | 바인더·에디터·스플릿뷰·포커스 모드 | Next.js, TipTap, Zustand |
| Graph Data | 관계도·타임라인·태그·검색 | PostgreSQL, Redis, Neo4j(선택) |
| AI Narrative Engine | 플롯 분석·복선·캐릭터 컨텍스트 | FastAPI (Python) |
| SaaS Platform | 인증·프로젝트·배포·과금 | API Gateway, Vercel, Railway/AWS |

단일 스택(NestJS Only / Python Only)으로 축소하지 않음.

---

## 다음 설계 단계 (CTO 레벨)

1. **ERD 실테이블 설계** — 현재 ERD를 실제 마이그레이션·인덱스·제약까지 반영
2. **API Spec (Swagger 수준)** — 엔드포인트·요청/응답·에러 코드 문서화
3. **Microservice 분리 기준** — 도메인 경계(Project/Chapter/Scene vs Character/Timeline vs AI)별 서비스 분리 시점·인터페이스
4. **Infra Production** — AWS ECS/Railway 실제 설계, R2 버킷, GitHub Actions 파이프라인

---

## 현재 구현 상태

- **백엔드**: 단일 FastAPI 앱 (API Gateway + Story Engine 역할 통합). 도메인별 라우터 분리됨.
- **프론트**: Next.js 앱, 바인더·에디터·Zustand. TanStack Query·Radix 도입 예정.
- **인프라**: Docker Compose (Postgres, Redis, Backend). Turborepo/pnpm 루트·Vercel 배포는 미구성.

이 문서는 위 4단계 진행 시 기준 문서로 활용.
