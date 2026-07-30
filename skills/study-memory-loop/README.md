# Study Memory Navigator

> 뭘 모르는지도 몰라서 AI에게 무엇을 어떻게 물어봐야 할지 막막한 사람을 위한 학습 내비게이터.

이 스킬은 이미 좋은 질문을 가진 사람만을 위한 답변 도구가 아닙니다. “AI를 알고 싶어”, “회사에서 AX를 하라는데 하나도 모르겠어” 같은 막연한 출발점에서 사용자의 목적을 추정하고, 아직 인식하지 못한 지식의 빈칸을 발견하고, AI에게 물어볼 질문의 순서를 만들어줍니다.

그다음 필요한 만큼만 설명하고, 학습자가 자기 말로 회상하게 하고, 틀린 부분을 교정한 뒤, 다음 복습일과 최소 기억 기록을 남깁니다.

## 우리가 해결하는 문제

초보자는 답을 모르는 것보다 **무엇을 물어봐야 하는지 모르는 것**에서 먼저 막힙니다.

```text
막연한 관심사
→ 내가 모르는 영역 발견
→ 지금 필요한 질문 생성
→ 최소 지식 지도
→ 이해와 적용
→ 회상과 복습
```

일반적인 AI 답변은 사용자가 질문을 잘 정의했다고 가정합니다. Study Memory Navigator는 질문을 만들기 전의 혼란부터 다룹니다.

## 핵심 기능

- 사용자의 막연한 표현에서 실제 학습 목적과 도착점 추정
- `이미 아는 것 / 지금 필요한 것 / 곧 필요한 것 / 아직 몰라도 되는 것` 구분
- 방향·구조·작동·경계·적용 순서의 질문 사다리 생성
- 복사해서 다른 AI 대화에서도 사용할 수 있는 질문 제공
- 한 턴에 새 핵심 개념을 기본 3개 이하로 제한
- 설명 직후 빈칸·비교·예측·자기 말 설명 중 하나로 능동 회상
- `즉시 → 1일 → 3일 → 7일 → 14일 → 30일` 간격 반복
- 완전 회상·부분 회상·실패에 따라 다음 복습 난이도 조정
- 전체 대화 대신 핵심 사실, 오개념, 회상 결과만 저장
- 관련 인덱스와 기한이 된 복습 항목만 읽어 토큰 사용 절약
- 선택한 Git 저장소에 학습 ledger 자동 커밋 및 선택적 push

## 호환성

이 스킬의 핵심은 공개 Agent Skills 형식인 `SKILL.md`와 선택적 `scripts/`, `references/`로 구성됩니다.

| 환경 | 설치 | 학습 대화 | Git 자동 기록 | 참고 |
|---|---:|---:|---:|---|
| OpenAI Codex CLI/Desktop | 지원 | 지원 | 지원 | `agents/openai.yaml` 메타데이터 사용 |
| Anthropic Claude Code | 지원 | 지원 | 지원 | `agents/openai.yaml`은 무시해도 됨 |
| Google Antigravity CLI/IDE | 지원 | 지원 | 지원 | 로컬 Python·Git 실행 권한 필요 |
| 기타 Agent Skills 호환 도구 | 대부분 지원 | 지원 | 환경에 따라 다름 | 스크립트 실행과 파일 권한 확인 필요 |
| claude.ai / Claude API | 별도 업로드 필요 | 일부 지원 | 기본적으로 비권장 | 로컬 Git 저장소를 직접 다루는 CLI 환경과 다름 |

핵심 학습 루프는 `SKILL.md`만 읽어도 작동합니다. Git 자동 기록 기능은 Python 3.10 이상, Git, 쓰기 가능한 로컬 저장소가 있어야 합니다.

## 가장 쉬운 설치

[Vercel Skills CLI](https://github.com/vercel-labs/skills)를 사용하면 지원되는 에이전트를 선택해 설치할 수 있습니다.

```bash
npx skills add AIjunja/Are-You-Human --skill study-memory-loop
```

명령 실행 후 설치할 에이전트와 전역 또는 프로젝트 범위를 선택합니다.

## 수동 설치 위치

`skills/study-memory-loop` 폴더 전체를 아래 위치 중 하나로 복사하세요. `SKILL.md`만 떼어내면 주제 렌즈와 Git 동기화 스크립트를 사용할 수 없습니다.

| 환경 | 프로젝트 범위 | 전역 범위 |
|---|---|---|
| Codex | `<project>/.agents/skills/study-memory-loop/` | `~/.codex/skills/study-memory-loop/` |
| Claude Code | `<project>/.claude/skills/study-memory-loop/` | `~/.claude/skills/study-memory-loop/` |
| Antigravity | `<project>/.agents/skills/study-memory-loop/` | `~/.gemini/config/skills/study-memory-loop/` |

Antigravity의 과거 버전은 `.agent/skills/` 같은 이전 경로를 사용할 수 있습니다. 최신 버전에서는 `.agents/skills/`를 우선하세요.

## 바로 사용하기

설치 후 에이전트를 새로 시작하거나 새 대화를 열고 다음처럼 말합니다.

```text
AI를 배우고 싶은데 뭘 물어봐야 할지도 모르겠어.
회사에서 AX를 하라는데 내가 먼저 알아야 할 걸 찾아줘.
데이터센터를 공부하려면 내가 모르는 영역부터 지도처럼 보여줘.
study-memory-loop로 TCP와 UDP를 10분 안에 공부하자.
AI 에이전트와 워크플로 자동화의 차이를 설명하고 바로 문제 내줘.
오늘 배운 영어 표현만 회상 테스트해줘.
데이터센터 전력과 냉각을 초보자 비유로 설명해줘.
```

스킬은 기본적으로 다음 순서로 진행합니다.

1. 막연한 관심사에서 구체적인 학습 도착점 추정
2. 사용자가 아직 인식하지 못한 핵심 빈칸 발견
3. `지금 필요 / 곧 필요 / 아직 불필요`로 지식 지도 구성
4. 방향·구조·작동·경계·적용 질문의 사다리 생성
5. 지금 가장 유용한 질문에 핵심 개념 3개 이하로 답변
6. 정답을 숨긴 능동 회상 질문
7. 오개념 교정, 다음 복습일과 기억 패킷 생성

## Git 학습 기록 설정

### 1. 학습 내용을 저장할 Git 저장소 준비

기존 저장소를 사용하거나 학습 기록 전용 저장소를 만듭니다. 스크립트는 해당 저장소의 `study-ledger/` 폴더만 stage합니다.

### 2. 저장소 위치 지정

가장 명확한 방법은 실행할 때 `--repo`를 지정하는 것입니다. 전역 설정이 필요하면 `STUDY_MEMORY_REPO` 환경변수를 사용합니다.

macOS/Linux:

```bash
export STUDY_MEMORY_REPO="$HOME/path/to/my-study-repo"
```

PowerShell:

```powershell
$env:STUDY_MEMORY_REPO = "C:\path\to\my-study-repo"
```

환경변수가 없으면 현재 작업 중인 Git 저장소를 사용합니다. 이전 버전과의 호환성을 위해 `CODEX_STUDY_REPO`도 계속 인식합니다.

### 3. 자동 push 활성화

최초 학습 기록이 만들어진 뒤 `study-ledger/config.json`을 다음처럼 설정합니다.

```json
{
  "auto_push": true
}
```

원격 저장소가 없거나 Git 인증이 실패하면 로컬 커밋까지만 수행하고 push 성공으로 표시하지 않습니다. force push는 사용하지 않습니다.

## 생성되는 기록

```text
study-ledger/
├── index.md
├── review-queue.jsonl
├── config.json
├── packets/
│   └── YYYY-MM-DD-topic-title.json
└── topics/
    └── topic.md
```

- `index.md`: 학습 주제 목록
- `review-queue.jsonl`: 복습 기한과 마지막 회상 결과
- `packets/`: 한 학습 턴의 최소 구조화 기록
- `topics/`: 사람이 읽기 쉬운 주제별 누적 노트

전체 대화 원문, API 키, 토큰, 개인정보는 기록하지 않도록 설계되어 있습니다.

## 직접 동기화 스크립트 실행

```bash
python skills/study-memory-loop/scripts/study_sync.py \
  --repo /path/to/study-repo \
  --packet /path/to/memory-packet.json
```

옵션은 다음 명령으로 확인합니다.

```bash
python skills/study-memory-loop/scripts/study_sync.py --help
```

## 제한사항

- “자동 암기”를 생물학적으로 보장하지는 않습니다. 능동 회상과 간격 반복을 자동화해 기억 가능성을 높입니다.
- 대화가 중간에 종료되어 회상 답변이 없으면 암기 완료로 기록하지 않습니다.
- 최신 기술 지식은 에이전트가 공식 자료를 확인할 수 있는 환경에서만 검증됩니다.
- Git 자동 기록은 사용자의 Git 이름, 이메일, 인증, 원격 저장소 설정을 대신 만들어주지 않습니다.
- 서로 다른 에이전트가 같은 ledger를 동시에 수정하면 Git 충돌이 발생할 수 있습니다.

## 파일 구성

```text
study-memory-loop/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   └── topic-lenses.md
└── scripts/
    └── study_sync.py
```

## 관련 공식 문서

- [OpenAI Codex: Save workflows as skills](https://developers.openai.com/codex/use-cases)
- [Anthropic Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Google Antigravity Agent Skills](https://antigravity.google/docs/skills)
- [Vercel Skills CLI](https://github.com/vercel-labs/skills)
