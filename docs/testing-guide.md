# StoryBuilder 통합 테스트 가이드

## 사전 준비

### 1. 백엔드 실행
```bash
cd backend
# 환경변수 설정
cp .env.example .env

# DB 실행 (Docker)
docker-compose up -d postgres redis

# 마이그레이션 (선택)
alembic upgrade head

# 서버 시작
uvicorn main:app --reload
```

→ http://localhost:8000/docs 에서 API 확인

### 2. 프론트엔드 실행
```bash
cd apps/web
npm run dev
```

→ http://localhost:3000 에서 UI 확인

---

## 테스트 시나리오

### 1단계: 회원가입/로그인 (API 직접)
```bash
# 회원가입
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "TestWriter",
    "password": "password123"
  }'

# 로그인
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# 응답에서 access_token 복사
```

### 2단계: 작품 생성
```bash
# 토큰을 환경변수로
export TOKEN="<your_access_token>"

# 작품 생성
curl -X POST http://localhost:8000/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "<user_id>",
    "title": "어둠 속의 빛",
    "description": "2145년 미래 서울을 배경으로...",
    "genre": "SF"
  }'

# 응답에서 project_id 복사
```

### 3단계: 장 생성
```bash
curl -X POST http://localhost:8000/api/chapters \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "<project_id>",
    "order_index": 1,
    "title": "1장. 깨어남",
    "summary": "주인공이 냉동수면에서 깨어나..."
  }'

# 응답에서 chapter_id 복사
```

### 4단계: 씬 생성
```bash
curl -X POST http://localhost:8000/api/scenes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "chapter_id": "<chapter_id>",
    "order_index": 1,
    "title": "냉동실에서의 깨어남",
    "location": "코스모스 함 냉동실 3구역"
  }'
```

### 5단계: 프론트엔드 테스트

1. **브라우저에서** http://localhost:3000 접속
2. **개발자 도구** 열기 (F12)
3. **Console 탭**에서 에러 확인
4. **Network 탭**에서 API 호출 확인

#### 예상 동작:
- ✅ 왼쪽 사이드바에 작품 목록 로드
- ✅ 작품 클릭 → 장 목록 펼쳐짐
- ✅ 장 클릭 → 씬 목록 펼쳐짐
- ✅ 씬 클릭 → 에디터에 원고 로드
- ✅ 에디터 입력 → 2초마다 자동저장

---

## 문제 해결

### CORS 에러
```
Access to XMLHttpRequest blocked by CORS policy
```

**해결:** backend/core/config.py의 ALLOWED_ORIGINS에 `http://localhost:3000` 추가

### 401 Unauthorized
```
Could not validate credentials
```

**해결:** 
1. 로그인 다시 수행
2. 토큰을 localStorage에 저장:
   ```javascript
   localStorage.setItem('access_token', '<your_token>')
   ```

### WebSocket 연결 실패
```
WebSocket connection to 'ws://localhost:8000/...' failed
```

**해결:**
- FastAPI 서버가 실행 중인지 확인
- WebSocket 라우터가 올바르게 등록되었는지 확인

### DB 연결 에러
```
could not connect to server: Connection refused
```

**해결:**
```bash
docker-compose up -d postgres
```

---

## 성공 기준

✅ **1단계:** 작품 목록이 사이드바에 표시됨  
✅ **2단계:** 작품 → 장 → 씬 계층 구조 펼침/접힘 동작  
✅ **3단계:** 씬 클릭 시 에디터에 원고 로드  
✅ **4단계:** 에디터 입력 후 2초 뒤 "자동 저장됨" 메시지  
✅ **5단계:** 페이지 새로고침 후에도 원고 유지됨  

---

## 다음 단계

1. 로그인 UI 페이지 추가
2. 작품/장/씬 생성 UI (모달)
3. 에러 토스트 알림
4. 로딩 스피너
5. 버전 기록 UI
