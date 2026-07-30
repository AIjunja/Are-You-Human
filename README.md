# Are You Human?

사람이 실제로 **이해하고 기억하도록** 돕는 AI 학습 스킬 저장소입니다.

첫 번째 스킬은 `study-memory-loop`입니다. 네트워크, AI, 데이터센터, 영어, AX를 포함한 어떤 주제든 짧은 대화 단위로 가르치고, 능동 회상과 간격 반복으로 복습하며, 최소 학습 기록을 Git에 남깁니다.

## Study Memory Loop

- 한 번에 핵심 개념 3개 이하
- 설명 직후 능동 회상 질문
- `즉시 → 1일 → 3일 → 7일 → 14일 → 30일` 복습
- 오개념 교정과 난이도 조절
- 필요한 인덱스와 복습 큐만 읽는 토큰 관리
- 전체 대화 대신 최소 기억 패킷만 Git에 기록
- 설정된 원격 저장소로 선택적 자동 push

자세한 호환성, 설치법, 설정법은 [스킬 README](skills/study-memory-loop/README.md)를 참고하세요.

## 설치

Codex, Claude Code, Antigravity CLI 등 지원되는 에이전트에 한 번에 설치하려면:

```bash
npx skills add AIjunja/Are-You-Human --skill study-memory-loop
```

또는 사용하는 에이전트에게 다음처럼 요청하세요.

```text
AIjunja/Are-You-Human 저장소의 skills/study-memory-loop 스킬을 설치해줘.
```

## 사용 예시

```text
네트워크를 기초부터 공부하자.
오늘 배운 AI 내용을 5분 복습으로 돌려줘.
데이터센터 전력과 냉각을 비유로 설명하고 문제 내줘.
영어 회화에서 내가 틀린 표현만 다시 회상시켜줘.
```

학습자는 대화에만 집중합니다. 스킬은 설명, 회상, 복습 일정, 학습 ledger 관리를 맡습니다.
