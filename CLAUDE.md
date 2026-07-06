# music-church-maker — 프로젝트 인수인계 (CLAUDE.md)

교회 예배용 가사/악보 자막 슬라이드를 자동 생성해 PPT·Keynote로 내보내는 도구.
저장소: https://github.com/Chocotea101/music-church-maker
현재 버전: v5.10 (단일 HTML 파일: `music-church-maker.html`)

## v5.10 변경 (2026-07-06)
- **악보 음이름 도레미 입력**: `toPitch()`가 도레미파솔라시(+#/♭, 옥타브) → 영어 표기(C4 등) 정규화. 영어도 그대로 됨. `parseScoreText`는 `=` 기준으로 음절/음이름/길이 분리(기존 정규식 대체).
- **실시간 검증·도움말**: `scoreWarnings`에 못 읽은 토큰(줄번호+토큰) 수집, `updateScoreStatus()`가 `#scoreStatus`에 "✓ N단·M음" 또는 "⚠ …" 표시(`refresh` 내 score 모드에서 호출). 도움말에 도레미 표기·길이 안내, `#scoreExampleBtn`으로 도레미 예시 채우기.

## v5.9 변경 (2026-07-06)
- **악보 렌더링 VexFlow 교체**: `drawPhraseVex()`가 전문 악보 라이브러리로 음자리표·조표·박자표·음표·빔·덧줄을 정위치 렌더, 가사는 음표 x에 맞춰 오선 아래 직접 그림. `renderPhraseCanvas()`가 VexFlow 준비되면 사용, 실패 시 기존 `drawPhrase()`로 폴백. 로더 `ensureVexLib()`: 로컬 `vexflow.js`(오프라인·gitignore됨) → jsdelivr → unpkg 순. 악보 모드 진입 시 로드 후 재렌더. **주의**: VexFlow `renderer.resize()`는 devicePixelRatio를 곱해 캔버스를 키우므로 쓰지 말 것(직접 canvas 크기 지정 + `ctx.scale`). 캔버스 560h, `getYForLine(4)+46`에 가사. `buildScoreSlides`는 각 단 실제 높이로 세로 스택.
- **폰트 미리보기**: 글꼴 칩(명조·궁서)이 각자 글씨체로 표시 + 미리보기 박스(`#fontPreview`)에 고른 글꼴로 샘플. `updateFontPreview()`를 `refresh()`에서 호출.
- **폰트 고르기 편하게**: '직접 입력' 누르면 `detectCommonFonts()`로 팝업 없이 목록 자동 표시, `#fontFilter` 검색으로 거름, 옵션·리스트가 각 글씨체로 보임(`renderFontOptions`/`applyFontFilter`). '더 많이 불러오기' 버튼은 queryLocalFonts(크롬).
- **빈 줄로 슬라이드 나누기 확장**: 2·4줄 모드에서도 빈 줄(엔터 두 번)을 만나면 거기서 끊어 특정 슬라이드만 더 적은 줄 가능(`buildLyricSlides` N모드).
- **새 버전 강제 업데이트**: 온라인에서 새 버전 확인 시 전체화면 `#updateGate`로 막고 최신본 유도. 오프라인이면 안 뜸. 안전장치로 작은 `#gateSkip`(계속 쓰기) 링크 있음 — 완전 차단 원하면 제거.

## v5.8 변경 (2026-07-06)
- **컴퓨터 화면 좌우 2단 레이아웃**: 넓은 화면(≥900px)에서 왼쪽=미리보기+내보내기(sticky 고정), 오른쪽=설정 스크롤. 휴대폰은 세로 1단으로 자동 접힘. (`.layout`/`.col-preview` CSS + body를 `col-preview`/`col-controls`로 감쌈)
- **설정 담은 파일로 저장**: `<script id="mcmEmbedded" type="application/json">`에 설정 JSON을 심어 자기 자신을 통째로 내려받음(`saveFileWithSettings`). 그 파일을 열면 `loadSettings`가 embedded를 localStorage보다 우선 읽어 복원 → 파일만 보내면 설정·가사·배경(업로드 이미지 포함)까지 그대로 이동. `collectSettings(heavy)`: heavy=true면 bgImage까지 포함.
- ⚠️ 주의: 인라인 `<script>` 안(주석 포함)에 `</` + `script>` 문자열을 절대 쓰지 말 것 — HTML 파서가 거기서 스크립트를 끊어 뒤 코드가 전부 죽음. 임베드 JSON은 `<` 문자를 유니코드 이스케이프(백슬래시+u003c)로 치환해 저장(JSON.parse가 도로 읽음).

## v5.7 변경 (2026-07-06)
- 업데이트 다운로드 파일명 한글 → 영문(`music-church-maker-vX.html`), macOS NFD 문제 재발 방지
- 폰트 목록 드롭다운을 화살표로 고를 때 슬라이드가 같이 넘어가던 것 차단(keydown 가드에 SELECT 추가)

## 지금까지 만든 것 (v5.6 기준)

### 가사 자막 모드
- 가사 붙여넣기 → 자동 슬라이드 분할 (빈 줄 기준 / 1·2·4줄씩)
- 폰트 크기 자동 계산 이론:
  - 가로 제약: `크기 ≤ 72 × 가용폭(inch) ÷ 최장 줄 폭계수` (한글 전각 1.02em, 그 외 0.55em)
  - 세로 제약: `크기 ≤ 72 × 가용높이 ÷ (줄수 × 행간 1.5)`
  - 두 제약의 최소값, 상한 60pt / 하한 28pt 경고, 전곡 통일(기본) 또는 슬라이드별
  - 안전 여백: 좌우 7%, 상하 10% (빔 스크린 잘림 대비)
- 수동 크기 조절 슬라이더 (20–80pt, 자동값 초과 시 넘침 경고)
- `*별표*` 감싼 단어 금색 강조 (pptx rich-text runs로 내보냄)

### 악보 자막 모드
- 악보 사진 → Claude API(claude-sonnet-4-6, 아티팩트 내 무키 호출)로 조성/박자/멜로디/가사 추출
- 정확한 가사를 미리 붙여넣으면 AI가 가사는 그대로 쓰고 음정만 읽음
- 다른 AI용 프롬프트 생성기(복사 버튼) — 결과 형식: `[제목]/[조성]/[박자]` + `음절=음이름(/길이)`
- 오선보를 canvas로 직접 렌더링: 높은음자리표(𝄞 glyph), 조표(♯♭ 정위치), 박자표, 음표(w/h/q/8/16, 기둥·꼬리), 덧줄, 임시표, 음표 아래 가사
- 슬라이드당 1/2/3단 합성

### 디자인
- 분위기 배경(정지) 3종: 새벽 빛/밤하늘/따뜻한 빛 — canvas 절차 생성(시드 고정), 비네트
- 움직이는 배경(GIF) 3종: 반짝이는 별/떠오르는 빛/오로라 — gif.js로 20프레임 완벽 루프 인코딩 (sin(2π·정수·phase) 기법), 960×540
- 사용자 이미지/GIF 업로드 배경 + 어둡게 오버레이(0/35/55%)
- 폰트: 고딕(맑은 고딕/Apple SD Gothic Neo), 명조(바탕/AppleMyungjo), 궁서(궁서/GungSeo), 직접 입력
- 설치된 폰트 목록: `queryLocalFonts()`(크롬, 권한 필요) → 실패 시 흔한 한글폰트 40여종 `document.fonts.check()` 감지 폴백
- 제목/부제 슬라이드, 배경 있을 때 텍스트 그림자

### 내보내기
- PptxGenJS 3.12.0 (cdnjs + jsdelivr + unpkg 예비 로딩 `ensurePptxLib()`)
- PowerPoint용 / Keynote용(폰트만 다름) 두 버튼. .key 직접 생성은 불가(애플 비공개 포맷) — Keynote에서 pptx를 열면 변환됨
- 16:9 (13.333×7.5in), GIF 배경은 addImage 전체 채움(슬라이드쇼에서 재생)

### 배포·업데이트 시스템
- `APP_VERSION` 상수 + 헤더 배지
- 실행 시 `https://raw.githubusercontent.com/Chocotea101/music-church-maker/main/version.json` 확인
  - 형식: `{"version":"5.7","file":"새 html raw 주소","link":"레포 주소","notes":"한 줄"}`
  - 원격이 더 높으면 배너 + 원클릭 다운로드(fetch→blob→a.download)
- 설정·작업내용 자동 저장: localStorage `mcm_settings_v1` (try/catch 가드 — claude.ai 아티팩트에선 무동작, 로컬 파일에서 작동)
  - 저장 항목: 분할/크기/폰트(커스텀 포함)/배경/테마/dim/단수/fsMode/fsManual/가사/악보데이터/제목/부제
  - 파일을 새 버전으로 교체해도 같은 브라우저면 복원됨

## 주의사항 (건드릴 때)
- 아티팩트(claude.ai) 환경 제약: 외부 스크립트는 cdnjs만 확실, localStorage 차단, AI 호출은 api.anthropic.com 무키 허용
- 로컬(file://) 환경: 모든 CDN 가능, localStorage 작동, queryLocalFonts는 크롬 계열만
- AI 악보 읽기 max_tokens=1000 제한 → 긴 곡은 페이지 분할 안내 중
- 한글 파일명은 macOS NFD 문제로 레포에는 영문명(music-church-maker.html) 권장

## 로드맵 제안 (다음 단계)
1. **데스크톱 앱 패키징: Tauri 추천** (C 재작성보다 나음 — 이유: UI가 본체인 앱이라 C는 GUI/폰트/한글/PPTX 생태계가 빈약해 배보다 배꼽. Tauri는 지금 HTML/JS를 그대로 감싸 수 MB 네이티브 앱으로 만들고 Rust 백엔드로 파일시스템·자동업데이트(진짜 자기교체)·폰트 열거가 가능)
2. 코드 구조화: 단일 HTML → src/ 모듈 분리(Vite), 상태관리 정리, 테스트
3. 오선보 렌더링을 VexFlow로 교체(이음줄·붙임줄·쉼표·마디선), MusicXML 가져오기 지원
4. 발표자 모드: 듀얼 스크린(조작 화면/출력 화면), 단축키, 다음 슬라이드 미리보기 → 사실상 ProPresenter 라이트
5. 곡 라이브러리(저장/불러오기, 콘티 묶음 내보내기 — 기존 콘티 작업과 연결)
6. AI 악보 읽기 개선: 페이지 자동 분할, 응답 이어받기, 검증 UI(재생해서 들어보기 — Tone.js)

## 커밋·버전 규칙
- 기능 추가 시 APP_VERSION 올리고(5.7, 5.8…) version.json 동기화
- 배포 = html 교체 + version.json 수정 (두 파일)
