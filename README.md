# PPT Design

**디자인 시스템 기반 PPTX 덱 생성기** — Claude Code / Claude Agent 스킬.
폰트와 색(테마)을 정의하면, 같은 콘텐츠 코드가 그 스타일의 수정 가능한 `.pptx`로 나온다.
제안서·보고서·강의·가이드북 등 **덱 유형**별 구성을 지원한다.

> 한국어 슬라이드에 최적화(가독성 보정 내장). 네이티브 표·차트(데이터 편집 가능).

---

## ⚡ 5분 시작 (신규 사용자)

### 1) 내 덱 프리셋 고르기 (~2분)
먼저 **어떤 스타일의 덱을 만들지** 정합니다. 가장 쉬운 방법은
[getdesign.md/design-md](https://getdesign.md/design-md)에서 원하는 사이트를 고르고,
그 사이트의 `DESIGN.md`를 내 덱 프리셋으로 쓰는 것입니다.

예:
- 깔끔한 SaaS 제안서: Linear, Attio, Stripe 계열 스타일
- 차분한 보고서: Notion, Apple 계열 스타일
- 강한 다크 톤: Vercel, Raycast 계열 스타일

가져온 `DESIGN.md`는 작업 프로젝트 루트나 Claude가 읽을 수 있는 위치에 둡니다.

```text
my-project/
  DESIGN.md
```

Claude에게는 이렇게 말하면 됩니다:

```text
DESIGN.md를 이 프로젝트의 덱 프리셋으로 사용해줘.
앞으로 만드는 PPT는 이 스타일을 기준으로 만들어줘.
```

스타일을 아직 고르지 않았다면 기본 `cream-coral` 테마로 시작할 수 있습니다.

### 2) 설치 (한 번만, ~2분)
```bash
# (1) 이 폴더를 스킬 디렉터리에 배치
#     Claude Code:  ~/.claude/skills/ppt-design/
# (2) 의존성 설치
pip install python-pptx
# (3) 폰트 설치 — 기본은 Pretendard (https://github.com/orioncactus/pretendard)
#     ※ 없어도 동작하지만 시스템 폰트로 대체되어 글꼴이 달라짐
```
> 사용자 전역 스킬이라 **한 번 넣으면 모든 프로젝트에서 자동 인식**됩니다.

### 3) 첫 덱 만들기 (~1분)
Claude에게 그냥 말하세요:
```
DESIGN.md 스타일로 이 웹사이트를 분석해서 제안서 덱 만들어줘:
https://example.com
```
Claude가 알아서: **유형·테마 확인 → 슬라이드 기획 → 빌드 → 렌더 검증 → 전달**.
결과물은 작업 폴더의 `OUTPUT/<프로젝트>/<파일>.pptx` 에 생깁니다.

또는 원고/메모를 바로 붙여넣어도 됩니다:

```text
DESIGN.md 스타일로 강의안 만들어줘.
내용은 아래와 같아: ...
```

### 4) 내 스타일 지정 방법
원하는 만큼만 주면 됩니다:

| 이렇게 말하면 | 결과 |
|---|---|
| "`DESIGN.md` 스타일로" | getdesign.md에서 가져온 사이트 스타일 |
| (그냥 만들어줘) | 기본 **cream-coral** 테마 |
| "**slate-blue** 테마로" | 프리셋 그대로 |
| "주색 **#2563EB**, 폰트 **Pretendard**로" | 색·폰트 시드 → 전체 팔레트 자동 생성 |
| "이 **디자인 시스템 명세** 붙여넣을게 →" + (MD 첨부) | 명세의 색·폰트로 테마 변환 |

### 5) 수정
"3번 슬라이드 문구 바꿔줘", "다크로 바꿔줘", "차트 추가" →
`OUTPUT/<프로젝트>/build.py` 한 줄 고쳐 재실행하면 즉시 반영됩니다.

### 고를 수 있는 것
- **덱 유형**: `제안서` · `보고서` · `강의` · `가이드북` (유형별 구성·톤 자동)
- **테마**: `cream-coral`(기본) · `slate-blue` · `ink-mono` · `voltagent-dark`(다크) · 커스텀

### 자주 막히는 곳
- 글꼴이 이상해요 → 테마 폰트가 PC에 **미설치**(시스템 폰트 대체). 폰트 설치하면 해결.
- 다른 PC에서 깨져요 → 그 PC에도 **폰트 설치** 필요(PPTX는 폰트를 품지 못함).
- 결과가 안 보여요 → `현재 작업 폴더`의 `OUTPUT/` 아래를 확인하세요.

---

## 특징
- 🎨 **테마 교체**: 프리셋(`cream-coral`·`slate-blue`·`ink-mono`·`voltagent-dark`) 또는
  폰트+시드색 몇 개로 전체 팔레트 자동 생성(`theme.from_seeds`). 라이트/다크 모두 지원.
- 📥 **디자인 명세 → 테마**: getdesign.md 형식의 디자인 시스템 마크다운을 붙여넣으면
  그 색·폰트로 테마를 만든다(`reference/DESIGN-MD.md`).
- 🧩 **레이아웃 카탈로그 45종**: 표지/통계/3·N-up/비교표/프로세스/타임라인/매트릭스/
  Do-Dont/인용/활동지/포스터/에디토리얼/차트/클로징 +
  **목차·KPI·가격표·팀·로고월·로드맵·SWOT·진행바·VS 대비·콜아웃**(제안서·보고서 공통) +
  **스크린샷·단계 안내(가이드북)** `split_image`·`steps_image`·`index_list`·
  `feature_cards`·`check_cards`·`image_full`·`image_grid`(전부 파라미터화).
- 📑 **덱 유형 4종**: proposal / report / lecture / guidebook — 유형별 추천 흐름.
- ✏️ **수정 가능 산출물**: 모든 텍스트·표·차트가 네이티브 PPTX 객체.
- 🔤 **폰트 고정/교체**: 기본 Pretendard, 테마로 임의 폰트.

## 설치
```bash
# 1) 스킬 폴더를 사용자 스킬 디렉터리에 배치
#    Claude Code:  ~/.claude/skills/ppt-design/
# 2) 의존성
pip install python-pptx
# 3) 테마 폰트 설치 (기본: Pretendard). 미설치 시 시스템 폰트로 대체.
```

## 빠른 사용 (스킬)
처음에는 [getdesign.md/design-md](https://getdesign.md/design-md)에서 원하는 사이트의
`DESIGN.md`를 가져와 덱 프리셋으로 정하는 것을 권장합니다.

Claude에게 자연어로:
- "`DESIGN.md` 스타일로 이 웹사이트를 분석해서 **제안서** 만들어줘 — https://example.com"
- "이 내용으로 **제안서** 만들어줘 — 우리 브랜드 색은 #2563EB, 폰트는 Pretendard"
- "**강의안** 만들어줘" (기본 cream-coral 테마)
- "이 보고서를 **slate-blue** 테마로"

Claude가 ① 유형·테마 확인 → ② (커스텀이면) 테마 생성 → ③ 슬라이드 기획 →
④ 빌드 스크립트 작성 → ⑤ 실행·렌더 검증 → ⑥ `OUTPUT/<프로젝트>/`에 전달.

## 직접 사용 (코드)
```python
import os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"),
                                ".claude", "skills", "ppt-design", "deck"))
from builder import Deck
import layouts as L

d = Deck(theme="slate-blue", kind="proposal", brand="ACME")
L.cover(d, title="제안서", title2="핵심 가치", subtitle="부제", brand="ACME")
L.stat_cards(d, "왜 지금인가", [("3x","속도","...")])
L.process(d, "도입 절차", [("진단","..."),("설계","..."),("적용","...")])
L.closing(d, "함께 시작하시죠", contact="hello@acme.com")
print(d.save_project("acme-proposal", "ACME.pptx"))
# → ./OUTPUT/acme-proposal/ACME.pptx
```

## 커스텀 테마
```python
import theme as th
t = th.from_seeds(font="Pretendard", primary="#2563EB", canvas="#FFFFFF",
                  ink="#0F172A", dark="#0B1220", name="acme")
th.save(t, "OUTPUT/acme/theme.json")
# Deck(theme="OUTPUT/acme/theme.json", ...)
```
자세한 건 `reference/THEMES.md`.

## 문서
- `SKILL.md` — 에이전트 워크플로
- `reference/LAYOUTS.md` — 레이아웃 카탈로그
- `reference/THEMES.md` — 테마 스키마·생성
- `reference/DECK-TYPES.md` — 유형별 구성

## 한계
- python-pptx는 폰트를 파일에 임베드하지 못함 → 보는 PC에 폰트 설치 필요.
- 16:9(1280×720) 전용. 밝은 캔버스 가정(다크모드 테마는 별도 정의 필요).
- 렌더 검증엔 PowerPoint(Windows) 또는 LibreOffice 필요(생성 자체는 불필요).

## License
MIT — see `LICENSE`.
