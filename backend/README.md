# StoryBuilder Backend

## 시작하기

### 1. 환경 변수 설정
```bash
cp .env.example .env
```

### 2. Docker로 시작 (추천)
```bash
# 루트 디렉토리에서
docker-compose up -d
```

### 3. 로컬 개발
```bash
# 의존성 설치
pip install -r requirements.txt

# PostgreSQL, Redis 시작 (Docker)
docker-compose up -d postgres redis

# DB 마이그레이션
alembic upgrade head

# 서버 시작
uvicorn main:app --reload
```

## API 문서

서버 시작 후:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 구조

```
backend/
├── main.py              # FastAPI 진입점
├── core/               # 핵심 설정
│   ├── config.py      # 환경 변수
│   └── database.py    # DB 연결
├── models/            # SQLAlchemy 모델
├── schemas/           # Pydantic 스키마
├── api/              # API 라우터
└── alembic/          # DB 마이그레이션
```
