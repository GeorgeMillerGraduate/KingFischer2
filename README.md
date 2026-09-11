# JengaFish 0.1.0

A Java 17 command-line UCI chess engine, packaged as a NetBeans-compatible Maven project. No GUI is included. JengaFish searches its own moves and does not invoke Stockfish at runtime.

**Release status:** a working first engine release, with a scalar port of the current Stockfish NNUE evaluator and an adapted selective search. It is **not a complete Stockfish port**, and does not promise identical best moves, depth, speed, Elo, or support for every Stockfish option. Read [the implementation status](docs/PORT-STATUS.md).

## Start on Windows

1. Extract the entire ZIP. Do not run files inside the ZIP preview.
2. Install/use a **64-bit Java 17 or newer** runtime. Your JDK 17 installation for NetBeans is suitable.
3. Double-click **Open-JengaFish.bat** for a command window, or open Command Prompt in the extracted `JengaFish` folder and enter:

```bat
java -Xmx768m -jar JengaFish.jar
```

Keep the **networks** folder beside the JAR. It contains the actual trained NNUE weights, approximately 94 MiB. The executable JAR is deliberately small; it contains all engine code but keeps the network separate to avoid duplicating it in this download.

If `java` is not on PATH, use the full JDK executable path, for example:

```bat
"C:\Program Files\Java\jdk-17\bin\java.exe" -Xmx768m -jar JengaFish.jar
```

Now enter commands, one line at a time:

```text
uci
isready
position startpos moves e2e4 e7e5 g1f3
go depth 6
```

Wait for `bestmove ...`. The engine emits real `info depth ... score ... nodes ... pv ...` lines while searching. Move choices and scores depend on the position and search, so this README does not promise a particular move.

To give it one second:

```text
go movetime 1000
```

For continuous analysis:

```text
go infinite
```

Type `stop` to get the best completed result, or `quit` to exit. The first search loads the network; subsequent searches reuse it. A successful bestmove does not update the game board automatically: send the next complete `position ... moves ...` command as a UCI GUI would.

`run-engine.bat` is the silent protocol launcher for future GUI integration. `Open-JengaFish.bat` adds a human-readable greeting and pause and is intended for double-click use only. On Linux/macOS, use `./run-engine.sh` or the same Java command.

## Open in NetBeans

1. Choose **File → Open Project**.
2. Select the extracted **JengaFish** directory containing `pom.xml`.
3. Set the project Java platform to **JDK 17 or newer**.
4. Use **Clean and Build**, then **Run Project**. The supplied `nbactions.xml` selects the main class and starts a separate Java process.
5. Enter UCI commands in NetBeans' Output/Input console. If your NetBeans console does not offer interactive input, run `Open-JengaFish.bat`; it uses the same engine.

This is a Maven project; NetBeans recognizes `pom.xml` without an Ant `nbproject` directory. Dependencies are downloaded on the first Maven build. The prebuilt JAR can run offline with the included network.

## Build and test

Command-line builds require a JDK and Maven on PATH. NetBeans can use its bundled Maven instead.

```text
mvn clean verify
java -Xmx768m -jar target/JengaFish.jar
```

Run the second command from the project directory so the network is found. Alternatively, copy the built JAR beside the existing `networks` folder. `build.bat` runs the tests and copies the new JAR over the root executable.

The engine has **no runtime Java dependencies**. JUnit and Maven plugins are build/test dependencies only. The project targets Java 17 bytecode.

For an engine GUI launched from another working directory, use the root `JengaFish.jar` beside the network folder, or set `EvalFile` to the network's absolute path.

## Supported interface

The standard UCI command names and response formats are used: `uci`, `uciok`, `isready`, `readyok`, `setoption`, `ucinewgame`, `position`, `go`, `stop`, `ponderhit`, `quit`, `info`, and `bestmove`. `debug` is accepted. `position` accepts `startpos` or all six FEN fields, with an optional legal coordinate-move list. Promotions use suffixes such as `e7e8q`; orthodox castling uses `e1g1` / `e1c1`.

Supported search limits: `depth`, `nodes`, `movetime`, `wtime`, `btime`, `winc`, `binc`, `movestogo`, `infinite`, `ponder`, `mate`, and `searchmoves`. `mate N` caps the depth at 2N and seeks a mate within that limit; this selective engine cannot prove that none exists if it finds none.

Advertised options:

| Option | Supported setting |
| --- | --- |
| Hash | 1–512 MiB requested; power-of-two primitive storage rounds down |
| Threads | 1 only in this release |
| Clear Hash | Button |
| Ponder | Accepted; `go ponder` and `ponderhit` control the lifecycle |
| MultiPV | 1–256, capped by the legal root move count |
| Move Overhead | 0–5000 ms, default 10 |
| EvalFile | Compatible network path; default `nn-1a298aa575a0.nnue` |
| SearchTrace | Actual search counters; default false |

`Ponder` currently does not increase the ordinary thinking-time budget. Unsupported options produce `info string Error: Unsupported option ...`; they are not advertised as working.

Development commands: `eval` (raw NNUE and scaled evaluation), `d` (FEN), `perft N`, `divide N`, `go perft N`, and `bench [depth]`. Perft/divide/bench are synchronous developer commands; use modest depths. UCI `stop` applies to ordinary asynchronous `go` searches, not these synchronous diagnostics.

## Verification included

- 29 JUnit tests, including starting-position perft through depth 6 (119,060,324), difficult castling/promotion/en-passant cases, state restoration, hashes, repetition, mate/stalemate, NNUE updates, and node limits.
- 2,000 deterministic positions: legal moves and perft depth 2 matched the reference Stockfish executable. Legal move sets also matched python-chess.
- 1,872 non-check positions: raw NNUE totals and normalized, zero-optimism evaluation matched the reference exactly. Positions in check are excluded from that evaluation comparison because Stockfish's `eval` declines to evaluate them.
- Executable protocol tests: depth 7 PV legality, MultiPV, restricted moves, short node/time limits, readiness during search, stop, ponder, malformed input recovery, and quit.

Details and measured timing are in [VALIDATION.md](docs/VALIDATION.md), with machine-readable results and the exact FEN corpus. These checks are a regression baseline, not an Elo or all-position correctness proof.

## Sources and licence

Stockfish reference: https://github.com/official-stockfish/Stockfish

Pinned commit: `59aae690f91d6f69aac194f447d84b4a2c3be778` (development build dated 2026-09-09, retrieved 2026-09-11).

JengaFish is an unofficial Java derivative/reimplementation. Adapted algorithms and NNUE code retain attribution to the Stockfish developers. Project owner/requester: George Miller. Java implementation and integration were prepared with AI assistance.

GNU GPL v3 or later; see `COPYING.txt`, `NOTICE.md`, and `STOCKFISH-AUTHORS`. The complete source for the supplied Java executable is included under `src/main/java`; the network used to run it is included under `networks`. There is no hidden native engine or platform-specific native library.

A future JavaFX GUI can launch this engine and communicate over UCI, without moving search or NNUE code into the GUI.
