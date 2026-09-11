# KingFischer2 0.1.0

A Java 17 UCI chess engine written in Java and packaged as a NetBeans-oriented Maven project.

KingFischer2 searches its own moves and does not invoke Stockfish at runtime.

> **Release status:** A working first engine release, with a scalar port of the current Stockfish NNUE evaluator and an adapted selective search.
>
> It is **not a complete Stockfish port**, and does not promise identical best moves, depth, speed, Elo, or support for every Stockfish option.
>
> See [Implementation Status](docs/PORT-STATUS.md) for further details.

---

## Quick Start on Windows

A prebuilt Windows executable is included:

~~~text
run_chess_engine.exe
~~~

This is the simplest way to start KingFischer2 on Windows.

1. Download or clone the complete repository.
2. Keep the project files and `networks` directory together.
3. Double-click:

~~~text
run_chess_engine.exe
~~~

A Windows Command Prompt window will open and start the chess engine.

You can also launch it manually from Command Prompt.

Open Command Prompt in the KingFischer2 directory and enter:

~~~bat
run_chess_engine.exe
~~~

You can then communicate with the engine using standard UCI commands.

For example:

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

The engine emits standard UCI search information while searching:

~~~text
info depth ... score ... nodes ... pv ...
~~~

Move choices and scores depend on the position and search parameters, so this README does not promise a particular move.

---

## Windows Executable

The supplied Windows executable is:

~~~text
run_chess_engine.exe
~~~

It provides a convenient way to run KingFischer2 from a normal Windows Command Prompt without opening the project in an IDE.

The executable is intended for **64-bit Windows**.

The underlying chess engine itself is written in Java.

Keep the supplied `networks` directory with the engine files. It contains the trained NNUE network used by the evaluation system.

The network is approximately **94 MiB**.

---

## Other Operating Systems

A precompiled executable is currently provided **only for Windows**.

There are currently no packaged macOS or Linux executables.

Because the engine itself is written in Java, the source code can be compiled on other platforms using a suitable Java IDE or Maven environment.

The project is primarily configured and tested using:

- **NetBeans**
- **Maven**
- **Java 17**

Users on Linux, macOS, or other Java-compatible platforms should compile the source code themselves.

Although other Java IDEs should be capable of importing the Maven project, **NetBeans is the primary development environment for KingFischer2**.

---

## Open and Compile in NetBeans

KingFischer2 is primarily designed as a **NetBeans Maven project**.

### Requirements

- NetBeans
- JDK 17 or newer
- Maven, or the Maven installation bundled with NetBeans

### Opening the project

1. Open **NetBeans**.
2. Select **File → Open Project**.
3. Select the **`KingFischer2`** directory containing `pom.xml`.
4. Set the project Java platform to **JDK 17 or newer**.
5. Select **Clean and Build**.
6. Select **Run Project**.

The supplied `nbactions.xml` configures the project for NetBeans.

Because this is a Maven project, NetBeans recognises the project through:

~~~text
pom.xml
~~~

An old-style Ant `nbproject` directory is not required.

Dependencies required for building and testing are downloaded by Maven.

---

## Compile from Source

The project can also be compiled directly with Maven if Java and Maven are installed.

From the KingFischer2 project directory:

~~~bash
mvn clean verify
~~~

The compiled JAR will be created under:

~~~text
target/
~~~

The engine can then be run using Java.

For example:

~~~bash
java -Xmx768m -jar target/KingFischer2.jar
~~~

Run the engine from the project directory so that the NNUE network can be located.

The exact JAR filename is determined by the Maven configuration in `pom.xml`.

The Windows `run_chess_engine.exe` is provided for convenience; the Java source remains the underlying implementation.

---

## Basic UCI Usage

KingFischer2 uses the **Universal Chess Interface (UCI)** protocol.

After starting:

~~~text
run_chess_engine.exe
~~~

enter commands one line at a time.

### Initialise UCI

~~~text
uci
~~~

The engine should eventually respond with:

~~~text
uciok
~~~

### Check readiness

~~~text
isready
~~~

The engine responds:

~~~text
readyok
~~~

### Set a position

For the starting position:

~~~text
position startpos
~~~

With moves:

~~~text
position startpos moves e2e4 e7e5 g1f3
~~~

### Start a search

For a fixed depth:

~~~text
go depth 6
~~~

The engine searches the position and eventually returns:

~~~text
bestmove ...
~~~

---

## Search Examples

### Search to depth 10

~~~text
go depth 10
~~~

### Search 100,000 nodes

~~~text
go nodes 100000
~~~

### Think for one second

~~~text
go movetime 1000
~~~

### Think for five seconds

~~~text
go movetime 5000
~~~

### Continuous analysis

~~~text
go infinite
~~~

Stop continuous analysis with:

~~~text
stop
~~~

Exit KingFischer2 with:

~~~text
quit
~~~

The first search loads the NNUE network. Subsequent searches reuse it.

A successful `bestmove` does **not** automatically update the game position.

Send the next complete:

~~~text
position ... moves ...
~~~

command as a normal UCI chess GUI would.

---

## Supported UCI Interface

KingFischer2 implements standard UCI command names and response formats.

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

or a complete FEN position.

An optional coordinate-move list may follow.

Example:

~~~text
position startpos moves e2e4 e7e5 g1f3 b8c6
~~~

Promotions use standard UCI suffixes:

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

For example:

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

KingFischer2 includes several additional commands for development and testing.

### Evaluate the current position

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

Perft, divide, and benchmark commands are synchronous developer operations.

Use reasonable depths.

UCI `stop` applies to ordinary asynchronous `go` searches and not to these synchronous diagnostic commands.

---

## Verification

KingFischer2 includes an automated regression and validation suite.

### JUnit Tests

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

See:

[VALIDATION.md](docs/VALIDATION.md)

for detailed validation results, measured timings, machine-readable results, and the exact FEN corpus.

These tests provide a regression baseline.

They are **not** an Elo measurement or a proof of correctness for every possible chess position.

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
- Does **not** contain a hidden native Stockfish engine.
- Does **not** require Stockfish to be installed to search positions.

It should not be interpreted as an official Stockfish release.

---

## Project Information

**Project:** KingFischer2  
**Version:** 0.1.0  
**Language:** Java  
**Minimum Java version:** Java 17  
**Build system:** Maven  
**Primary interface:** UCI  
**Primary IDE:** NetBeans  
**Windows executable:** `run_chess_engine.exe`  
**Project owner/requester:** George Miller  

Java implementation and integration were prepared with AI assistance.

---

## Licence

KingFischer2 is distributed under the **GNU General Public License version 3 or later (GPLv3+)**.

See:

- [`COPYING.txt`](COPYING.txt)
- [`NOTICE.md`](NOTICE.md)
- [`STOCKFISH-AUTHORS`](STOCKFISH-AUTHORS)

The complete Java source code is included under:

~~~text
src/main/java/
~~~

The NNUE network required by the supplied engine is included under:

~~~text
networks/
~~~

---

## Platform Support

| Platform | Current Support |
| --- | --- |
| **Windows 64-bit** | Prebuilt `run_chess_engine.exe` provided |
| **Windows + NetBeans** | Full source project supported |
| **Linux** | Compile Java source yourself |
| **macOS** | Compile Java source yourself |
| **Other Java platforms** | May work when compiled with Java 17+, but are not currently packaged or tested |

The repository is primarily intended as a **NetBeans-oriented Java project**.

Users on platforms other than Windows should import or compile the Maven source project using a suitable Java development environment.

---

## Future Development

Possible future development includes:

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

A future JavaFX GUI can communicate with KingFischer2 over **UCI**, keeping the chess engine, search, and NNUE implementation independent from the graphical interface.
