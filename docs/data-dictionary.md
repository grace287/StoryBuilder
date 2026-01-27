# StoryBuilder 데이터 딕셔너리

> 모든 테이블과 필드의 상세 명세

---

## 📋 목차
- [User](#user)
- [Project](#project)
- [Chapter](#chapter)
- [Scene](#scene)
- [Manuscript](#manuscript)
- [Character](#character)
- [CharacterRelation](#characterrelation)
- [Timeline](#timeline)
- [Setting](#setting)

---

## User

**작가 계정**

| 컬럼명 | 타입 | 제약 | 설명 | 예시 |
|--------|------|------|------|------|
| id | UUID | PK | 사용자 고유 ID | `550e8400-e29b-41d4-a716-446655440000` |
| email | VARCHAR(255) | UK, NOT NULL | 이메일 (로그인) | `grace@storybuilder.com` |
| username | VARCHAR(50) | NOT NULL | 작가명 | `Grace Kim` |
| password_hash | VARCHAR(255) | NOT NULL | 해시된 비밀번호 | `$2b$12$...` |
| created_at | TIMESTAMP | NOT NULL | 가입일 | `2026-01-27 10:00:00` |
| last_login | TIMESTAMP | NULL | 마지막 로그인 | `2026-01-27 15:30:00` |

**비즈니스 규칙**
- 이메일 중복 불가
- username은 변경 가능, email은 인증 후 변경

---

## Project

**작품 (소설/시나리오 프로젝트)**

| 컬럼명 | 타입 | 제약 | 설명 | 예시 |
|--------|------|------|------|------|
| id | UUID | PK | 작품 고유 ID | `660e8400-...` |
| user_id | UUID | FK(User), NOT NULL | 작가 ID | `550e8400-...` |
| title | VARCHAR(200) | NOT NULL | 작품 제목 | `어둠 속의 빛` |
| description | TEXT | NULL | 시놉시스 | `2145년 미래 서울을 배경으로...` |
| genre | VARCHAR(50) | NULL | 장르 | `SF`, `판타지`, `로맨스` |
| status | ENUM | NOT NULL | 상태 | `draft`, `active`, `completed`, `archived` |
| metadata | JSON | NULL | 추가 설정 | `{"target_words": 100000, "deadline": "2026-12-31"}` |
| created_at | TIMESTAMP | NOT NULL | 생성일 | `2026-01-27 10:00:00` |
| updated_at | TIMESTAMP | NOT NULL | 수정일 | `2026-01-27 15:00:00` |

**비즈니스 규칙**
- 한 작가는 여러 작품 소유 가능
- status 기본값: `draft`
- 삭제는 soft delete (status = `archived`)

**metadata JSON 스키마 예시**
```json
{
  "target_words": 100000,
  "deadline": "2026-12-31",
  "writing_days": 90,
  "themes": ["정체성", "생존", "희망"],
  "inspiration": "1984 + 블레이드러너"
}
```

---

## Chapter

**장 (작품의 큰 단위 구분)**

| 컬럼명 | 타입 | 제약 | 설명 | 예시 |
|--------|------|------|------|------|
| id | UUID | PK | 장 고유 ID | `770e8400-...` |
| project_id | UUID | FK(Project), NOT NULL | 작품 ID | `660e8400-...` |
| order_index | INTEGER | NOT NULL | 장 순서 (1부터) | `1`, `2`, `3` |
| title | VARCHAR(200) | NOT NULL | 장 제목 | `1장. 깨어남` |
| summary | TEXT | NULL | 장 요약 | `주인공이 냉동수면에서 깨어나...` |
| status | VARCHAR(20) | NULL | 진행 상태 | `draft`, `writing`, `revision`, `done` |
| word_count | INTEGER | DEFAULT 0 | 총 단어 수 | `8500` |
| created_at | TIMESTAMP | NOT NULL | 생성일 | `2026-01-27 10:00:00` |
| updated_at | TIMESTAMP | NOT NULL | 수정일 | `2026-01-27 15:00:00` |

**비즈니스 규칙**
- order_index는 같은 project_id 내에서 유니크
- word_count는 하위 Scene들의 합계 (자동 계산)
- 장 삭제 시 하위 Scene들도 cascade delete

**인덱스**
```sql
UNIQUE INDEX uk_chapter_order ON chapter(project_id, order_index);
INDEX idx_chapter_project ON chapter(project_id);
```

---

## Scene

**씬 (실제 집필 단위, 보통 한 장소/시간)**

| 컬럼명 | 타입 | 제약 | 설명 | 예시 |
|--------|------|------|------|------|
| id | UUID | PK | 씬 고유 ID | `880e8400-...` |
| chapter_id | UUID | FK(Chapter), NOT NULL | 장 ID | `770e8400-...` |
| order_index | INTEGER | NOT NULL | 씬 순서 | `1`, `2`, `3` |
| title | VARCHAR(200) | NULL | 씬 제목 | `냉동실에서의 깨어남` |
| summary | TEXT | NULL | 씬 요약 | `주인공 민준이 500년 만에...` |
| pov_character_id | UUID | FK(Character), NULL | 관점 인물 | `990e8400-...` |
| location | VARCHAR(200) | NULL | 장소 | `코스모스 함 냉동실 3구역` |
| scene_time | TIMESTAMP | NULL | 작중 시간 | `2145-03-15 06:00:00` |
| word_count | INTEGER | DEFAULT 0 | 단어 수 | `1200` |
| tags | JSON | NULL | 태그 | `["액션", "갈등", "복선"]` |
| created_at | TIMESTAMP | NOT NULL | 생성일 | `2026-01-27 10:00:00` |
| updated_at | TIMESTAMP | NOT NULL | 수정일 | `2026-01-27 15:00:00` |

**비즈니스 규칙**
- Scene = 최소 집필 단위 (하나의 에디터 문서)
- pov_character_id: 1인칭/3인칭 제한 관점 인물
- scene_time: 타임라인 정렬용 (NULL 허용)
- word_count는 Manuscript의 최신 버전에서 계산

**tags JSON 예시**
```json
["액션", "복선-민준의 기억", "전환점", "인물-수진 등장"]
```

---

## Manuscript

**원고 (실제 텍스트, 버전 관리)**

| 컬럼명 | 타입 | 제약 | 설명 | 예시 |
|--------|------|------|------|------|
| id | UUID | PK | 원고 고유 ID | `aa0e8400-...` |
| scene_id | UUID | FK(Scene), NOT NULL | 씬 ID | `880e8400-...` |
| version | INTEGER | NOT NULL | 버전 번호 | `1`, `2`, `3` |
| content | TEXT | NOT NULL | 실제 원고 | `민준은 눈을 떴다. 하얀 천장이...` |
| format | VARCHAR(20) | DEFAULT 'markdown' | 포맷 | `markdown`, `html`, `plain` |
| word_count | INTEGER | DEFAULT 0 | 단어 수 | `1200` |
| created_at | TIMESTAMP | NOT NULL | 생성일 | `2026-01-27 10:00:00` |
| auto_saved_at | TIMESTAMP | NULL | 자동저장 시간 | `2026-01-27 15:30:42` |

**비즈니스 규칙**
- 한 Scene에 여러 버전 존재 가능 (Git 커밋처럼)
- version은 같은 scene_id 내에서 자동 증가
- 최신 버전 = MAX(version)
- 자동저장은 2초마다, auto_saved_at 업데이트

**인덱스**
```sql
INDEX idx_manuscript_scene ON manuscript(scene_id, version DESC);
FULLTEXT INDEX idx_manuscript_content ON manuscript(content);
```

---

## Character

**인물 (등장인물)**

| 컬럼명 | 타입 | 제약 | 설명 | 예시 |
|--------|------|------|------|------|
| id | UUID | PK | 인물 고유 ID | `990e8400-...` |
| project_id | UUID | FK(Project), NOT NULL | 작품 ID | `660e8400-...` |
| name | VARCHAR(100) | NOT NULL | 이름 | `이민준` |
| role | VARCHAR(20) | NULL | 역할 | `protagonist`, `antagonist`, `supporting`, `minor` |
| description | TEXT | NULL | 한줄 소개 | `냉동수면에서 깨어난 우주 탐험가` |
| personality | JSON | NULL | 성격 | `{"mbti": "INTJ", "traits": ["신중함", "고집"]}` |
| appearance | JSON | NULL | 외모 | `{"age": 35, "height": 178, "특징": "왼쪽 눈 흉터"}` |
| background | JSON | NULL | 배경 | `{"출신": "서울", "직업": "우주선 기관사"}` |
| avatar_url | VARCHAR(500) | NULL | 프로필 이미지 | `https://cdn.../minjun.jpg` |
| created_at | TIMESTAMP | NOT NULL | 생성일 | `2026-01-27 10:00:00` |
| updated_at | TIMESTAMP | NOT NULL | 수정일 | `2026-01-27 15:00:00` |

**비즈니스 규칙**
- 한 작품에 여러 인물
- role 기본값: `supporting`
- JSON 필드는 유연하게 확장 가능

**personality JSON 예시**
```json
{
  "mbti": "INTJ",
  "traits": ["신중함", "고집", "책임감"],
  "values": ["생존", "진실", "충성"],
  "flaws": ["완벽주의", "감정 억압"],
  "arc": "고립 → 연대"
}
```

---

## CharacterRelation

**인물 관계 (Many-to-Many 관계 테이블)**

| 컬럼명 | 타입 | 제약 | 설명 | 예시 |
|--------|------|------|------|------|
| id | UUID | PK | 관계 고유 ID | `bb0e8400-...` |
| character_a_id | UUID | FK(Character), NOT NULL | 인물 A | `990e8400-...` (민준) |
| character_b_id | UUID | FK(Character), NOT NULL | 인물 B | `aa0e8400-...` (수진) |
| relation_type | VARCHAR(50) | NOT NULL | 관계 유형 | `lover`, `enemy`, `family`, `mentor` |
| description | TEXT | NULL | 관계 설명 | `과거 연인, 현재 갈등` |
| strength | INTEGER | DEFAULT 0 | 관계 강도 | `-100` (적대) ~ `100` (친밀) |
| created_at | TIMESTAMP | NOT NULL | 생성일 | `2026-01-27 10:00:00` |

**비즈니스 규칙**
- A → B 단방향 관계 (양방향은 2개 행으로 표현)
- strength: 음수=적대, 양수=우호
- 같은 인물 간 여러 관계 가능 (ex: 형제이자 경쟁자)

**인덱스**
```sql
INDEX idx_relation_a ON character_relation(character_a_id);
INDEX idx_relation_b ON character_relation(character_b_id);
```

---

## Timeline

**타임라인 (작중 시간 순서 사건)**

| 컬럼명 | 타입 | 제약 | 설명 | 예시 |
|--------|------|------|------|------|
| id | UUID | PK | 타임라인 고유 ID | `cc0e8400-...` |
| project_id | UUID | FK(Project), NOT NULL | 작품 ID | `660e8400-...` |
| title | VARCHAR(200) | NOT NULL | 사건명 | `코스모스 함 출발` |
| event_time | TIMESTAMP | NOT NULL | 작중 시간 | `2140-06-01 09:00:00` |
| description | TEXT | NULL | 사건 설명 | `목적지 알파센타우리로...` |
| type | VARCHAR(20) | NULL | 타입 | `plot`, `world`, `character` |
| created_at | TIMESTAMP | NOT NULL | 생성일 | `2026-01-27 10:00:00` |

**비즈니스 규칙**
- event_time으로 정렬하여 타임라인 생성
- type으로 필터링 (플롯/세계관/인물별)
- Scene과 연결하여 "이 씬의 타임라인상 위치" 표시

**type 분류**
- `plot`: 핵심 플롯 사건
- `world`: 세계관 역사
- `character`: 인물 개인사

---

## Setting

**세계관 설정**

| 컬럼명 | 타입 | 제약 | 설명 | 예시 |
|--------|------|------|------|------|
| id | UUID | PK | 설정 고유 ID | `dd0e8400-...` |
| project_id | UUID | FK(Project), NOT NULL | 작품 ID | `660e8400-...` |
| category | VARCHAR(50) | NOT NULL | 카테고리 | `world`, `magic`, `tech`, `social` |
| name | VARCHAR(200) | NOT NULL | 설정명 | `워프 드라이브` |
| description | TEXT | NULL | 설명 | `빛보다 빠른 이동을 가능하게...` |
| details | JSON | NULL | 상세 정보 | `{"발견년도": 2080, "원리": "..."}` |
| created_at | TIMESTAMP | NOT NULL | 생성일 | `2026-01-27 10:00:00` |
| updated_at | TIMESTAMP | NOT NULL | 수정일 | `2026-01-27 15:00:00` |

**비즈니스 규칙**
- 위키 페이지처럼 동작
- category로 분류하여 검색
- details는 자유 형식 JSON

**category 분류**
- `world`: 세계관 기본 설정
- `magic`: 마법 체계
- `tech`: 기술/과학
- `social`: 사회/정치
- `culture`: 문화/언어

---

## 🔗 연결 테이블 (Many-to-Many)

### scene_characters (씬-인물 등장)

| 컬럼명 | 타입 | 제약 | 설명 |
|--------|------|------|------|
| scene_id | UUID | FK(Scene), NOT NULL | 씬 ID |
| character_id | UUID | FK(Character), NOT NULL | 인물 ID |
| role_in_scene | VARCHAR(50) | NULL | 씬에서의 역할 |

```sql
PRIMARY KEY (scene_id, character_id)
```

**비즈니스 규칙**
- 한 씬에 여러 인물 등장
- role_in_scene: `main`, `background`, `mentioned`

---

## 📊 데이터 예시 (연결된 데이터)

### 작품: "어둠 속의 빛"
```
Project: 어둠 속의 빛
  ├─ Chapter 1: 깨어남
  │   ├─ Scene 1-1: 냉동실 (민준 POV)
  │   │   └─ Manuscript v3: "민준은 눈을 떴다..."
  │   └─ Scene 1-2: 함장실 (수진 POV)
  │
  ├─ Character: 이민준 (주인공)
  ├─ Character: 박수진 (주인공)
  └─ Timeline: 
      - 2140-06-01: 출발
      - 2145-03-15: 민준 깨어남 (← Scene 1-1)
```

---

**다음 단계**
→ 이 딕셔너리 기반으로 SQLAlchemy 모델 생성
