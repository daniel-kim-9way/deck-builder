---
name: deck-builder
description: 발표자료(PPTX)를 디자인 시스템 기반으로 생성한다. 사용자가 폰트와 색/스타일을 주면 그 테마로, 안 주면 기본(크림·코랄) 테마로 만든다. 제안서·보고서·강의·가이드북 등 덱 유형별 구성을 지원한다. 파라미터화된 레이아웃 라이브러리로 수정 가능한 .pptx를 만든다. "PPT/발표자료/강의안/제안서/보고서/가이드북 만들어줘", "이 스타일로 슬라이드", "우리 브랜드 색으로 덱" 등에 사용.
---

# Deck Builder — 테마 가능한 PPTX 덱 생성기

디자인 시스템(색·폰트·레이아웃)을 코드로 정의해 일관된 `.pptx`를 찍어낸다.
**테마(폰트+스타일)는 교체 가능**하고, **덱 유형(제안서/보고서/강의/가이드북)**별로
구성을 다르게 가져간다. 하드코딩이 아니라 파라미터화된 레이아웃을 조합한다.

## 사전 요건
- Python + `python-pptx` (`pip install python-pptx`)
- 테마 폰트 설치(미설치 시 시스템 폰트로 대체). 기본 테마는 Pretendard.
- 렌더 검증(선택): PowerPoint COM(Windows) 또는 LibreOffice

## 라이브러리 위치
이 SKILL.md 옆 `deck/`:
- `builder.py` — `Deck(theme=..., kind=...)`, `save_project()`
- `layouts.py` — 레이아웃 카탈로그 → **`reference/LAYOUTS.md`**
- `theme.py` — 테마 로드/생성/적용 → **`reference/THEMES.md`**
- `decktypes.py` — 유형별 추천 구성 → **`reference/DECK-TYPES.md`**
- 디자인 명세(getdesign.md) → 테마 변환 → **`reference/DESIGN-MD.md`**
- `themes/*.json` — 프리셋(cream-coral, slate-blue, ink-mono, voltagent-dark)
- `tokens.py` / `helpers.py` — 스케일·저수준 드로잉

## 워크플로

### 1) 유형 + 테마 정하기 (첫 사용 시 질문)
사용자에게 두 가지를 확인한다(이미 말했으면 생략):
- **덱 유형**: 제안서 / 보고서 / 강의 / 가이드북 (`proposal|report|lecture|guidebook`)
- **디자인 테마**:
  - (a) 프리셋 사용: `cream-coral`(기본) / `slate-blue` / `ink-mono`
  - (b) **사용자 스타일 제공**: 폰트명 + 핵심 색 몇 개(주색·배경·글자색·다크색)
    또는 참고 이미지/URL의 색. → `theme.from_seeds(...)`로 전체 팔레트 자동 생성.
  - (c) **디자인 시스템 명세(getdesign.md) 붙여넣음**: `{colors.*}`·`{typography.*}`
    토큰을 쓰는 마크다운을 받으면 → **`reference/DESIGN-MD.md`의 매핑대로 테마로 변환**.
    near-black 캔버스면 `mode:"dark"`(카드 자동 hairline). 예: `voltagent-dark` 프리셋.

### 2) (사용자 스타일일 때) 테마 파일 생성
```python
import theme as th
t = th.from_seeds(
    font="Pretendard",          # 설치된 폰트명
    primary="#2563EB",          # 주색(CTA·강조)
    canvas="#FFFFFF",           # 배경
    ink="#0F172A",              # 본문 글자
    dark="#0B1220",             # 다크 서피스
    accent2="#0EA5E9", accent3="#F59E0B",   # 보조 강조(생략 가능)
    name="acme")
th.save(t, "OUTPUT/<프로젝트>/theme.json")   # 프로젝트에 함께 저장
```
시드 4~6색에서 26개 의미 슬롯(surface/hairline/muted/on_dark 등)을 자동 파생한다.
굵기별 폰트 패밀리가 있으면 `weights={...}`로 지정(없으면 bold로 근사).

### 3) 슬라이드 기획 (유형 흐름 참고)
`decktypes.flow("<유형>")`의 추천 구성을 참고해 슬라이드 리스트를 짠다.
같은 레이아웃을 3장 이상 연속 쓰지 않는다. 다크/포스터로 리듬을 준다.

### 4) 빌드 스크립트 작성 → `OUTPUT/deck-builder/<프로젝트>/build.py`
```python
import os, sys
sys.path.insert(0, r"D:\futuretalent_ai\.claude\skills\deck-builder\deck")
from builder import Deck
import layouts as L

PROJECT = "acme-proposal"
d = Deck(theme="slate-blue", kind="proposal", brand="ACME · 제안서")
#   theme=프리셋이름 | "OUTPUT/acme-proposal/theme.json" | dict
L.cover(d, title="...", title2="...", subtitle="...", brand="ACME")
L.stat_cards(d, "...", [("…","…","…"), ...])
# ... 유형 흐름대로 레이아웃 조합 ...
print(d.save_project(PROJECT, "ACME_Proposal.pptx"))
```

### 5) 실행 & 검증
현재 폴더에서 `python OUTPUT/<프로젝트>/build.py` 실행 → `OUTPUT/<프로젝트>/`에 생성.
PowerPoint COM으로 `render/`에 PNG를 내보내 Read로 확인하고, 잘림/오버플로를 고친다.

### 6) 전달
`.pptx` 경로 + 구성 요약 + 폰트 의존성(다른 PC에서 해당 폰트 필요)을 보고한다.

## 출력 위치 규칙 (필수)
모든 결과물은 **`<root>/deck-builder/<프로젝트명>/`** 에 모은다.
(root = 환경변수 `FT_OUTPUT_ROOT`, 없으면 `현재폴더(cwd)/OUTPUT`)
```
<root>/deck-builder/<프로젝트명>/
  build.py · <파일명>.pptx · theme.json(커스텀일 때) · render/
```
- `d.save_project("<프로젝트명>","<파일>.pptx")` → 위 경로 자동 생성.
- 이 프로젝트에선 `D:\futuretalent_ai\OUTPUT\deck-builder\<프로젝트명>\` 로 떨어진다(cwd=프로젝트 루트 기준).

## 위치 · 이식성
이 스킬은 **프로젝트 로컬**(`D:\futuretalent_ai\.claude\skills\deck-builder`)에 있다(전역 아님, 자급자족).
다른 PC로 옮길 땐 이 폴더째 복사 + `python-pptx`·Pretendard 폰트 설치, 그리고 build.py의
`sys.path` 절대경로만 새 위치에 맞게 바꾼다. (card-news-builder가 이 스킬을 형제 폴더로 참조)

## 가이드라인
- 색 절제: 주색(primary)은 강조·CTA에만. 다크 서피스로 대비/리듬.
- 텍스트 분량: 카드/셀엔 한두 문장(길면 잘림).
- 유형별 톤: 제안서=설득, 보고서=객관·데이터, 강의=몰입·활동, 가이드북=차분·읽힘.
- 새 레이아웃은 `layouts.py`에 추가하고 `reference/LAYOUTS.md`에 기록.
