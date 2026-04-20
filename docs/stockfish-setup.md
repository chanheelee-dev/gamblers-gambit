# Stockfish Setup

이 게임은 포지션 평가에 [Stockfish](https://stockfishchess.org/) 엔진을 사용한다. UCI 프로토콜을 지원하는 네이티브 바이너리가 필요하며, `python-chess` 가 서브프로세스로 호출한다.

## 설치

> 공식 안내: ["We only recommend downloading from the official GitHub releases."](https://github.com/official-stockfish/Stockfish/wiki/Download-and-usage)
> 
> 릴리스 페이지: https://github.com/official-stockfish/Stockfish/releases/latest

### macOS

**Step 1. 칩 확인**

```bash
uname -m
# arm64   → Apple Silicon (M1/M2/M3)
# x86_64  → Intel
```

**Step 2. 릴리스 페이지에서 파일 선택**

https://github.com/official-stockfish/Stockfish/releases/latest 의 Assets 목록에서 선택:

| 칩 | 선택 기준 |
|---|---|
| Apple Silicon (arm64) | `stockfish-macos-m1-apple-silicon` 포함 파일 |
| Intel (x86_64) | `stockfish-macos-x86-64-avx2` 우선, 구형이면 `x86-64-modern` |

AVX2 지원 여부 확인: `sysctl -a | grep avx2` 출력이 있으면 avx2.

**Step 3. 압축 해제 & PATH 등록**

```bash
# 다운로드 폴더에서
tar -xf <다운로드한 파일명>.tar

# 바이너리를 PATH에 복사
sudo mv stockfish/stockfish /usr/local/bin/stockfish
```

**Step 4. Gatekeeper 해제**

처음 실행 시 macOS가 "개발자 미확인 앱" 으로 차단할 수 있음:

```bash
xattr -d com.apple.quarantine /usr/local/bin/stockfish
```

### Linux (패키지 매니저 — 간단하지만 버전 느릴 수 있음)

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install stockfish

# Arch
sudo pacman -S stockfish

# Fedora
sudo dnf install stockfish
```

**Debian/Ubuntu 주의**: 바이너리가 `/usr/games/stockfish` 에 설치된다. `/usr/games` 가 PATH 에 없으면 아래 "PATH 이슈 해결" 참조.

### Linux (GitHub 릴리스 — 최신 버전)

패키지 매니저 버전이 오래됐다면 macOS와 동일하게 직접 받는다.

https://github.com/official-stockfish/Stockfish/releases/latest 에서 `stockfish-ubuntu-x86-64-avx2` 등 본인 환경에 맞는 파일 선택.

```bash
tar -xf <다운로드한 파일명>.tar
sudo mv stockfish/stockfish /usr/local/bin/stockfish
```


## 동작 확인

```bash
stockfish
```

프롬프트가 뜨면 UCI 명령을 테스트:

```
uci
```

`id name Stockfish 16` 같은 응답 뒤 `uciok` 이 떠야 정상. `quit` 으로 종료.

PATH 에서 못 찾으면 전체 경로로 직접 실행:

```bash
/usr/games/stockfish        # Debian/Ubuntu
/opt/homebrew/bin/stockfish # Apple Silicon mac
```

## PATH 이슈 해결

### 영구 해결 (Debian/Ubuntu)

`~/.bashrc` 또는 `~/.zshrc` 에 추가:

```bash
export PATH="$PATH:/usr/games"
```

새 셸을 열거나 `source ~/.bashrc`.

### 일회성: 환경 변수 오버라이드

이 프로젝트의 엔진 래퍼는 `STOCKFISH_PATH` 환경 변수를 우선으로 읽는다. PATH 를 건드리기 싫으면:

```bash
STOCKFISH_PATH=/usr/games/stockfish uv run python -m gamblers_gambit
```

엔진 탐색 순서는 `mvp/gamblers_gambit/engine.py` 의 `find_stockfish()` 참조:

1. `STOCKFISH_PATH` 환경 변수
2. `shutil.which("stockfish")` — PATH 검색
3. 알려진 폴백 경로 (`/usr/games/stockfish`, `/usr/local/bin/stockfish`)

## 버전

python-chess 는 UCI 프로토콜만 쓰므로 Stockfish 버전은 크게 가리지 않는다. 다만:

- **너무 구 버전** (Stockfish 10 이전): `info` 메시지 포맷이 다른 경우 있음. 15+ 권장.
- **NNUE (신경망) 지원 버전** 은 평가가 훨씬 정확. 최신 패키지 매니저 배포본은 모두 NNUE 포함.
- 현 문서 기준 안정 버전: **Stockfish 16+**.

## 트러블슈팅

| 증상 | 원인 / 해결 |
|---|---|
| `FileNotFoundError: Stockfish binary not found` | `which stockfish` 로 확인. PATH 이슈면 위 "PATH 이슈 해결" 참조. |
| `Permission denied` | 바이너리 실행권한: `chmod +x /path/to/stockfish`. |
| 엔진이 매우 느림 | depth 파라미터를 낮추거나, NNUE 가중치가 로드되는지 확인 (`setoption name Use NNUE value true` 가 기본). |

## 관련 문서

- [`design/game-concept.md`](./design/game-concept.md) §Metric 선택 — cp ↔ wp 변환 공식이 엔진 출력을 어떻게 소비하는지.
- [`background/chess-primer.md`](./background/chess-primer.md) — Stockfish, UCI, depth, PV 등 엔진 용어.
- [`mvp/README.md`](./mvp/README.md) — 설치 후 MVP 실행법.
