# KingFischer2 0.1.0

A Java 17 command-line UCI chess engine, packaged as a NetBeans-compatible Maven project. No GUI is included. **KingFischer2** searches its own moves and does not invoke Stockfish at runtime.

> **Release status:** A working first engine release, with a scalar port of the current Stockfish NNUE evaluator and an adapted selective search.
>
> It is **not a complete Stockfish port**, and does not promise identical best moves, depth, speed, Elo, or support for every Stockfish option.
>
> See [Implementation Status](docs/PORT-STATUS.md) for further details.

---

## Start on Windows

1. Extract the entire ZIP. Do not run files from inside the ZIP preview.
2. Install or use a **64-bit Java 17 or newer** runtime.
3. Double-click **`Open-KingFischer2.bat`** to open the engine in a command window.

Alternatively, open Command Prompt inside the extracted `KingFischer2` directory and run:

~~~bat
java -Xmx768m -jar KingFischer2.jar
~~~

Keep the **`networks`** folder beside the JAR.

It contains the trained NNUE weights, approximately **94 MiB**. The executable JAR is deliberately small: it contains the engine code while keeping the neural-network data separate to avoid duplicating it in the download.

### Java not on PATH?

If `java` is not on your PATH, specify the Java executable directly:

~~~bat
"C:\Program Files\Java\jdk-17\bin\java.exe" -Xmx768m -jar KingFischer2.jar
~~~

---

## Basic UCI Usage

After starting KingFischer2, enter commands one line at a time:

~~~text
uci
isready
position startpos moves e2e4 e7e5 g1f3
go depth 6
~~~

Wait for:

~~~text
bestmove ...
~~~

The engine emits standard UCI search information:

~~~text
info depth ... score ... nodes ... pv ...
~~~

Move choices and scores depend on the position and search parameters, so this README does not promise a particular move.

### Search for one second

~~~text
go movetime 1000
~~~

### Continuous analysis

~~~text
go infinite
~~~

Then enter:

~~~text
stop
~~~

to return the best completed result.

Enter:

~~~text
quit
~~~

to terminate the engine.

The first search loads the NNUE network. Subsequent searches reuse it.

A successful `bestmove` does **not** automatically update the internal game position. Send the next complete `position ... moves ...` command as a normal UCI chess GUI would.

---

## Launchers

### `Open-KingFischer2.bat`

Human-friendly Windows launcher intended for double-click use. It provides a greeting and pauses appropriately.

### `run-engine.bat`

Silent UCI protocol launcher intended for integration with chess GUIs and other applications.

### `run-engine.sh`

Linux/macOS launcher.

The engine can also always be launched directly with:

~~~bash
java -Xmx768m -jar KingFischer2.jar
~~~

---

## Open in NetBeans

1. Open **NetBeans**.
2. Select **File → Open Project**.
3. Select the extracted **`KingFischer2`** directory containing `pom.xml`.
4. Set the project Java platform to **JDK 17 or newer**.
5. Select **Clean and Build**.
6. Select **Run Project**.

The supplied `nbactions.xml` selects the main class and starts a separate Java process.

Enter UCI commands through NetBeans' Output/Input console.

If your NetBeans console does not provide interactive input, run:

~~~text
Open-KingFischer2.bat
~~~

instead. Both methods use the same engine.

KingFischer2 is a standard **Maven project**. NetBeans recognises `pom.xml` directly, so an Ant `nbproject` directory is not required.

Dependencies are downloaded during the first Maven build.

The prebuilt JAR can run offline provided the included NNUE network is available.

---

## Build and Test

Command-line builds require a JDK and Maven on your PATH.

NetBeans can alternatively use its bundled Maven installation.

Build and run:

~~~bash
mvn clean verify
java -Xmx768m -jar target/KingFischer2.jar
~~~

Run the second command from the project directory so that the NNUE network can be located.

Alternatively, copy the newly built JAR beside the existing `networks/` directory.

The supplied `build.bat` runs the tests and copies the newly built JAR over the root executable.

### Runtime dependencies

KingFischer2 has **no runtime Java dependencies**.

JUnit and the Maven plugins are required only for building and testing.

The project targets **Java 17 bytecode**.

For a chess GUI launched from another working directory, use the root `KingFischer2.jar` beside the network directory, or set `EvalFile` to the absolute path of the NNUE network.

---

## Supported UCI Interface

KingFischer2 implements the standard UCI command names and response formats.

Supported commands include:

~~~text
uci
uciok
isready
readyok
setoption
ucinewgame
position
go
stop
ponderhit
quit
info
bestmove
debug
~~~

`position` accepts either:

~~~text
position startpos
~~~

or all six FEN fields.

An optional legal coordinate-move list may follow.

For example:

~~~text
position startpos moves e2e4 e7e5 g1f3 b8c6
~~~

Promotions use suffixes such as:

~~~text
e7e8q
~~~

Orthodox castling uses:

~~~text
e1g1
e1c1
~~~

---

## Search Limits

Supported search limits include:

- `depth`
- `nodes`
- `movetime`
- `wtime`
- `btime`
- `winc`
- `binc`
- `movestogo`
- `infinite`
- `ponder`
- `mate`
- `searchmoves`

Examples:

~~~text
go depth 10
go nodes 100000
go movetime 5000
go infinite
~~~

`mate N` caps the depth at `2N` and searches for a mate within that limit.

Because KingFischer2 uses a selective search, failure to find a mate does not constitute a mathematical proof that no mate exists.

---

## UCI Options

| Option | Supported Setting |
| --- | --- |
| **Hash** | 1–512 MiB requested; power-of-two primitive storage rounds down |
| **Threads** | 1 only in this release |
| **Clear Hash** | Button |
| **Ponder** | Accepted; `go ponder` and `ponderhit` control the lifecycle |
| **MultiPV** | 1–256, capped by the legal root move count |
| **Move Overhead** | 0–5000 ms, default 10 |
| **EvalFile** | Compatible NNUE network path; default `nn-1a298aa575a0.nnue` |
| **SearchTrace** | Actual search counters; default `false` |

`Ponder` currently does not increase the normal thinking-time budget.

Unsupported options produce:

~~~text
info string Error: Unsupported option ...
~~~

Unsupported options are not advertised as working.

---

## Development Commands

KingFischer2 also includes several commands intended for development and testing.

### Evaluate Position

~~~text
eval
~~~

Displays the raw NNUE and scaled evaluation.

### Display FEN

~~~text
d
~~~

### Perft

~~~text
perft N
~~~

### Divide

~~~text
divide N
~~~

### UCI-style Perft

~~~text
go perft N
~~~

### Benchmark

~~~text
bench [depth]
~~~

Perft, divide, and benchmark commands are synchronous developer operations. Use reasonable depths.

UCI `stop` applies to ordinary asynchronous `go` searches and not to these synchronous diagnostics.

---

## Verification

KingFischer2 includes an extensive automated regression and validation suite.

### JUnit

**29 JUnit tests**, including:

- Starting-position perft through depth 6
- **119,060,324 nodes** at starting-position depth 6
- Castling edge cases
- Promotions
- En passant
- State restoration
- Position hashes
- Repetition detection
- Checkmate
- Stalemate
- NNUE incremental updates
- Search node limits

### Move Generation

**2,000 deterministic positions** were compared against the reference Stockfish executable.

For these positions:

- Legal moves matched Stockfish.
- Perft depth 2 matched Stockfish.
- Legal move sets also matched `python-chess`.

### NNUE Evaluation

For **1,872 non-check positions**:

- Raw NNUE totals matched the reference.
- Normalised zero-optimism evaluation matched the reference exactly.

Positions in check are excluded from this evaluation comparison because Stockfish's `eval` command declines to evaluate them.

### UCI Protocol

Executable protocol tests include:

- Depth 7 PV legality
- MultiPV
- Restricted root moves
- Short node limits
- Short time limits
- Readiness during search
- `stop`
- Pondering
- Malformed input recovery
- `quit`

See [VALIDATION.md](docs/VALIDATION.md) for detailed validation results, measured timings, machine-readable results, and the exact FEN corpus.

These tests provide a regression baseline. They are **not** an Elo measurement or a proof of correctness for every possible chess position.

---

## Stockfish Reference

KingFischer2 uses Stockfish as an algorithmic and validation reference.

**Official Stockfish repository:**

https://github.com/official-stockfish/Stockfish

Reference commit:

~~~text
59aae690f91d6f69aac194f447d84b4a2c3be778
~~~

Development build dated:

~~~text
2026-09-09
~~~

Reference retrieved:

~~~text
2026-09-11
~~~

---

## Relationship to Stockfish

KingFischer2 is an **unofficial Java derivative/reimplementation**.

Adapted algorithms and NNUE-related code retain attribution to the Stockfish developers.

KingFischer2:

- Is implemented in Java.
- Implements its own chess board and move handling.
- Performs its own search.
- Runs its NNUE evaluation from Java.
- Does **not** invoke the Stockfish executable at runtime.
- Does **not** contain a hidden native chess engine.
- Does **not** require a platform-specific native engine library.

It should not be interpreted as an official Stockfish release.

---

## Project Information

**Project:** KingFischer2  
**Version:** 0.1.0  
**Language:** Java  
**Minimum Java version:** Java 17  
**Build system:** Maven  
**Primary interface:** UCI  
**IDE support:** NetBeans / standard Maven-compatible IDEs  
**Project owner/requester:** George Miller  

Java implementation and integration were prepared with AI assistance.

---

## Licence

KingFischer2 is distributed under the **GNU General Public License version 3 or later (GPLv3+)**.

See:

- [`COPYING.txt`](COPYING.txt)
- [`NOTICE.md`](NOTICE.md)
- [`STOCKFISH-AUTHORS`](STOCKFISH-AUTHORS)

The complete source code corresponding to the supplied Java executable is included under:

~~~text
src/main/java/
~~~

The NNUE network required by the supplied engine is included under:

~~~text
networks/
~~~

---

## Future Development

Planned development can include:

- JavaFX chess GUI
- Multi-threaded search
- Search performance optimisation
- Additional Stockfish search heuristics
- Improved time management
- Engine-vs-engine testing
- Elo benchmarking
- Additional UCI options
- Analysis mode
- GUI engine configuration
- Automated regression tournaments

A future JavaFX GUI can launch KingFischer2 and communicate with it over **UCI**, keeping the chess engine, search, and NNUE implementation independent from the graphical interface.
