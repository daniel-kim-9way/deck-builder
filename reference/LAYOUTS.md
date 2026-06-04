# 레이아웃 카탈로그

모든 함수는 첫 인자로 `Deck` 인스턴스(`d`)를 받고 슬라이드 1장을 추가한다.
`import layouts as L` 후 `L.함수(d, ...)` 로 호출.
**색 인자를 생략하면 코랄→틸→앰버 자동 순환.** 색은 토큰명 문자열
(`"primary"`, `"accent_teal"`, `"accent_amber"`, `"surface_dark"`, `"ink"` 등).

## 표지 · 전환 · 메시지

### `cover(d, title, subtitle="", eyebrow="", brand="", title2=None, title2_color="primary", meta="")`
표지. `title2`를 주면 2번째 줄을 강조색 ExtraBold로(1번째 줄은 Light).
- 예: `L.cover(d, title="강점으로 일하는 법", title2="잠재력 발견", subtitle="...", brand="9WAY", meta="문의...")`

### `section_divider(d, number, title, subtitle="", dark=True)`
챕터 전환. 큰 번호 + 제목. `number=""`이면 번호 없이 중앙 좌측 제목만.
- 예: `L.section_divider(d, "01", "강점의 이해", "왜 중요한가")`

### `statement(d, lines, bg="surface_cream_strong")`
큰 중앙 메시지(도트 장식). 줄바꿈 `\n` 사용. 임팩트 전환용.
- 예: `L.statement(d, "인재 전쟁의 시대,\n어떻게 일하는가가\n운명을 결정한다")`

### `quote(d, quote_text, author="", bg="surface_cream_strong")`
인용/명언. 큰 따옴표 + Light 본문 + 출처.

## 학습 · 개념

### `objectives(d, title, goals, eyebrow="Learning Objectives")`
체크리스트형 학습 목표. `goals`: 문자열 리스트(권장 3~5개).

### `concept(d, term, definition, formula="", example="", eyebrow="Key Concept")`
핵심 개념: 큰 용어(Black) + 정의 + (공식 박스) + (다크 예시 콜아웃).
- 예: `L.concept(d, "강점", "재능에 지식·기술이...", formula="재능 × (지식+기술) = 강점", example="...")`

### `question(d, question_text, sub="")`
풀코랄 빅 퀘스천. `\n`으로 줄나눔. 청중 환기용(푸터 없음).

### `takeaways(d, title, items, eyebrow="Key Takeaways")`
핵심 N가지(최대 4). `items`: `[(소제목, 설명)]`. 넘버 + 색 라인.

## 카드 · 통계

### `three_up(d, title, cards, eyebrow="")`
3-up 피처 카드. `cards`: `[(제목, 본문)]` 또는 `[(제목, 본문, 색)]` (최대 3).

### `stat_cards(d, title, stats, eyebrow="")`
통계 카드(최대 4). `stats`: `[(숫자, 라벨, 설명)]` 또는 `[(..., 색)]`.
- 예: `L.stat_cards(d, "문제", [("13%","낮은 몰입도","설명"), ("67%","이직률","설명")])`

### `big_stat(d, number, pre="", post="", note="")`
단일 빅 통계. 거대한 숫자 1개 + 상하 설명.
- 예: `L.big_stat(d, "560%", pre="강점을 인식하면", post="더 높은 몰입도", note="* Gallup")`

## 표 · 프로세스 · 타임라인

### `comparison_table(d, title, data, highlight_col=None, eyebrow="", header_color="dark", label_col=True, intro="")`
네이티브 비교 표(편집 가능). `data`: 2차원 리스트(첫 행=헤더, 첫 열=행 라벨).
`highlight_col`: 강조할 열 인덱스(0-base). `header_color`: `"dark"` 또는 `"coral"`.
- 예: `L.comparison_table(d, "A vs B", [["","A","B"],["속도","느림","빠름"]], highlight_col=2)`

### `process(d, title, steps, eyebrow="Process")`
가로 프로세스 타임라인. `steps`: `[(제목, 설명)]` 또는 `[(..., 색)]`. 권장 3~5단계.

### `vsteps(d, title, steps, eyebrow="Process")`
세로 단계(연결선). `steps`: `[(제목, 설명)]`. 권장 3~5단계.

### `timeline(d, title, nodes, eyebrow="Timeline")`
가로 타임라인(위/아래 교차). `nodes`: `[(라벨, 제목, 보조)]`. 마지막 노드는 코랄 강조.
- 예: `L.timeline(d, "역사", [("1998","긍정심리학","셀리그만"), ("2024","9WAY","")])`

## 프레임워크 · 가이드

### `matrix_2x2(d, title, quads, note="", eyebrow="Framework", axis_label="")`
2×2 사분면. `quads`: 4개 `[(라벨, 보조)]` 순서=좌상,우상,좌하,우하.
`note`를 주면 우측에 다크 해설 패널. `axis_label`: 하단 축 라벨.

### `do_dont(d, title, dos, donts, eyebrow="Guide")`
DO/DON'T 2단. `dos`·`donts`: 문자열 리스트(각 3~4개). 초록 체크 / 빨강 X.

### `keyword_grid(d, title, words, cols=3, eyebrow="")`
키워드 그리드. `words`: `[문자열]` 또는 `[(라벨, 색)]`. `cols`로 열 수.

## 무드 · 콘텐츠

### `poster(d, headline, eyebrow="", sub="", dark=True)`
Black weight 임팩트 포스터(다크 기본). `headline`에 `\n`으로 줄나눔.

### `editorial(d, headline, columns, eyebrow="Essay")`
Thin weight 매거진/에세이. `headline`(Thin) + `columns`(본문 1~2개 리스트).

### `bullets_slide(d, title, items, eyebrow="", marker="—")`
제목 + 불릿. `items`: `[문자열]` 또는 `[(마커, 문자열)]`.

### `two_col(d, title, left, right, eyebrow="")`
2단 대비. `left`/`right`: `(헤딩, 본문, [fill], [accent])`.
본문은 문자열 또는 리스트(리스트면 불릿). fill 미지정 시 좌=크림카드, 우=다크.

### `checklist(d, title, items, dark=True, eyebrow="Summary")`
요약 체크리스트(다크 기본). `items`: 문자열 리스트.

### `worksheet(d, title, prompts, eyebrow="Activity", action="")`
활동지(빈칸). `prompts`: `[(라벨, 힌트)]`. `action`: 하단 코랄 액션 배너.

## 차트

### `chart(d, title, categories, series, kind="column", eyebrow="", note="")`
네이티브 차트(편집 가능). `categories`: 문자열 리스트.
`series`: `[(이름, [값들])]`. `kind`: `"column"` | `"line"` | `"donut"`.
시리즈 색은 코랄/틸/앰버/다크 자동 적용.
- 예: `L.chart(d, "분포", ["발상","탐색","평가"], [("팀", (6,4,5))], kind="column")`
- 도넛: `L.chart(d, "비중", ["A","B","C"], [("점유율", (40,35,25))], kind="donut")`

## 마무리

### `closing(d, title, sub="", contact="")`
코랄 CTA 클로징 밴드. `contact`를 주면 크림 버튼에 표시.

---

## 새 레이아웃 추가 방법
1. `deck/layouts.py`에 `def 새이름(deck, ...):` 함수 추가
   (`deck.add(bg)`로 슬라이드 생성, `helpers`의 `rect/oval/text/...` 사용,
   끝에 `deck.footer(s)` 호출).
2. 이 문서에 시그니처·설명 추가.
3. 좌표계는 1280×720 px. `LX=80`, 콘텐츠 폭 `CW=1120`.
