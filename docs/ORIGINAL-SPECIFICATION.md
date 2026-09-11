Create a complete Java port/reimplementation of the CURRENT official Stockfish chess engine.

This is NOT merely a request to create a generic chess engine inspired by Stockfish.

Use the official Stockfish source code as the primary technical reference:

https://github.com/official-stockfish/Stockfish

Study the complete current Stockfish codebase before implementing the Java version.

The objective is to reproduce as much of Stockfish's actual architecture, algorithms, search behaviour, evaluation system, heuristics, optimisations and UCI behaviour as technically practical in Java.

The resulting project must comply with Stockfish's GNU GPL v3 licensing requirements and clearly acknowledge that it is derived from/ported from Stockfish.

Do not disguise copied or translated Stockfish logic as independently invented code.

Call the engine:

JengaFish

Use:

Java 17+
Maven
JUnit
64-bit JVM

NO GUI yet.

The first release must be a command-line UCI chess engine like Stockfish itself.

\==================================================

1. RESEARCH STOCKFISH BEFORE WRITING THE PORT
   \==================================================

Before implementing the Java engine, inspect the CURRENT official Stockfish source tree in detail.

Do not rely primarily on generic descriptions of chess programming.

Study the actual implementation.

At minimum investigate the current equivalents of:

types
bitboards
attacks
position
move generation
move picking
history tables
search
evaluation
NNUE
NNUE accumulator
NNUE feature transformer
NNUE layers
transposition table
time management
threads
engine
UCI
UCI options
Syzygy probing
benchmarking

Build an internal dependency map showing how Stockfish works.

The Java architecture should be based on that understanding.

Do not blindly translate C++ syntax line-by-line where Java requires a different implementation strategy.

Instead:

Stockfish C++ semantics
↓
understand algorithm
↓
identify performance assumptions
↓
design Java equivalent
↓
implement
↓
verify against Stockfish

Preserve algorithmic behaviour wherever practical.

# ================================================== 2. PROJECT ARCHITECTURE

Create a substantial Maven project with packages corresponding logically to Stockfish's subsystems.

For example:

src/main/java/com/jengacode/jengafish/

```
Main.java

engine/
    Engine.java
    EngineOptions.java
    EngineCallbacks.java

uci/
    UciEngine.java
    UciCommand.java
    UciParser.java
    UciOptions.java
    UciScore.java

chess/
    Position.java
    StateInfo.java
    Move.java
    MoveType.java
    Piece.java
    PieceType.java
    Color.java
    Square.java
    CastlingRights.java

bitboard/
    Bitboards.java
    Attacks.java
    SlidingAttacks.java

movegen/
    MoveGenerator.java
    MoveList.java
    MovePicker.java

search/
    Search.java
    SearchWorker.java
    SearchManager.java
    SearchStack.java
    RootMove.java
    SearchLimits.java
    SearchResult.java
    SearchConstants.java

history/
    HistoryTable.java
    CaptureHistory.java
    ContinuationHistory.java
    PawnHistory.java

tt/
    TranspositionTable.java
    TTEntry.java
    TTWriter.java

eval/
    Evaluation.java

nnue/
    Network.java
    NetworkReader.java
    Accumulator.java
    AccumulatorStack.java
    AccumulatorCache.java
    FeatureTransformer.java
    NnueArchitecture.java

    features/
        HalfKAv2.java
        FullThreats.java
        PP3Wide.java

    layers/
        AffineTransform.java
        SparseAffineTransform.java
        ClippedReLU.java
        SqrClippedReLU.java

time/
    TimeManager.java

threading/
    ThreadPool.java
    SearchThread.java

syzygy/
    Tablebase.java
    TablebaseProbe.java

util/
    Fen.java
    Perft.java
    Benchmark.java
    Zobrist.java

```

This is illustrative rather than mandatory.

If the current Stockfish architecture suggests a better mapping, use it.

# ================================================== 3. PERFORMANCE PRINCIPLE

This is a chess ENGINE.

Do not write ordinary allocation-heavy enterprise Java.

The hot search path must be designed like performance software.

Prefer:

long
int
short
byte
boolean
primitive arrays
fixed-size structures
preallocated buffers
mutable reusable objects

Avoid:

boxing
streams
lambdas in hot loops
temporary collections
String manipulation during search
creating Move objects for every move
creating Position objects for every node
unnecessary polymorphism in hot loops

Use packed primitive representations where appropriate.

The JVM implementation should attempt to allow JIT optimisation and escape analysis to work effectively.

# ================================================== 4. BITBOARDS

Reproduce Stockfish-style bitboard functionality in Java using long.

Implement efficient:

square masks
files
ranks
diagonals
anti-diagonals
pawn attacks
knight attacks
king attacks
bishop attacks
rook attacks
queen attacks

Use:

Long.bitCount()
Long.numberOfTrailingZeros()

and appropriate bit manipulation.

Investigate how CURRENT Stockfish generates sliding-piece attacks and implement an efficient Java equivalent.

Precompute data where beneficial.

# ================================================== 5. POSITION REPRESENTATION

Port the concepts represented by Stockfish Position and StateInfo.

Position must efficiently maintain:

piece placement
piece bitboards
piece counts
occupancy
side to move
castling rights
en-passant square
halfmove/rule-50 counter
game ply
Zobrist position key
pawn key where useful
material information where useful
checkers
pinned pieces where appropriate

Moves must support:

normal
promotion
en passant
castling

Implement extremely efficient:

doMove()
undoMove()

and equivalent null-move operations.

Do NOT copy the entire board for every search node.

# ================================================== 6. MOVE GENERATION

Port Stockfish's move-generation strategy.

Correctly generate:

captures
quiet moves
evasions
checks where required
promotions
castling
en passant

Correctly deal with:

pins
check
double check
discovered attacks
illegal king moves
en-passant discovered checks
Chess960 considerations if supported

Provide legal-move filtering consistent with the engine architecture.

# ================================================== 7. PERFT BEFORE SEARCH

Do not trust the search until move generation is proven correct.

Implement:

perft N

and:

divide N

Starting position must produce:

1 = 20
2 = 400
3 = 8,902
4 = 197,281
5 = 4,865,609
6 = 119,060,324

Add recognised difficult perft positions covering:

castling
en passant
promotions
pins
checks

Create automated JUnit regression tests.

# ================================================== 8. ZOBRIST HASHING

Implement deterministic high-performance Zobrist hashing.

Update hashes incrementally during make/unmake.

Test that:

make move
undo move

returns EXACTLY to the original:

position
state
hash

# ================================================== 9. TRANSPOSITION TABLE

Study the current Stockfish TT implementation.

Create a Java equivalent optimised for memory efficiency.

Avoid creating millions of Java objects.

Prefer packed primitive arrays or similarly compact storage.

Store appropriate information including:

key/signature
depth
bound
score
static evaluation
best move
generation/age

Support:

EXACT
LOWER
UPPER

Handle mate-score conversion correctly between search ply and TT representation.

Implement:

setoption name Hash value N

# ================================================== 10. MOVE PICKER

Do not merely sort every generated move using Collections.sort().

Study Stockfish's MovePicker architecture.

Port the staged move-selection concept.

The move picker should prioritise appropriate categories such as:

TT move
good captures
promotions
killer/high-history quiets
remaining quiets
bad captures

Port/adapt Stockfish's actual scoring concepts.

# ================================================== 11. HISTORY HEURISTICS

This is important.

Investigate CURRENT Stockfish history structures rather than implementing only a simplistic killer heuristic.

Reproduce Java equivalents for relevant concepts such as:

main history
capture history
continuation history
pawn history
countermove/continuation relationships
correction histories

where they exist in the current engine.

Study:

how entries are indexed
how bonuses are calculated
how maluses are applied
how values are bounded/decayed
where search updates them

Do not replace Stockfish's sophisticated history system with one HashMap.

Use primitive multidimensional arrays or flattened arrays.

# ================================================== 12. ITERATIVE DEEPENING

Port Stockfish's iterative-deepening root search.

Search:

depth 1
depth 2
depth 3
...

Maintain RootMove information.

Preserve the principal variation.

Support MultiPV where practical.

Implement aspiration-window behaviour based on the current Stockfish design.

# ================================================== 13. CORE SEARCH

This is the heart of the project.

Study CURRENT search.cpp carefully.

Recreate the actual search architecture in Java.

Implement the equivalent of Stockfish's recursive alpha-beta/PVS search.

Distinguish appropriately between:

PV nodes
non-PV nodes
root nodes
cut nodes

Correctly implement:

alpha
beta
depth
ply
mate bounds
draw handling
TT probing
TT cutoffs
static evaluation
move generation
move ordering
extensions
reductions
pruning
PV construction

Do not replace Stockfish's search with textbook minimax.

# ================================================== 14. QUIESCENCE SEARCH

Implement Stockfish-style quiescence search.

Include appropriate handling of:

stand pat
captures
promotions
checks/evasions where required
TT information
delta/futility concepts where applicable

Maintain correct mate/stalemate behaviour.

# ================================================== 15. SEARCH SELECTIVITY

Study the exact current Stockfish conditions and mathematical formulas associated with its selective search.

Port/adapt relevant mechanisms including, where present:

Late Move Reductions

Null Move Pruning

Reverse Futility Pruning

Futility Pruning

Late Move Pruning

Razoring

ProbCut

Singular Extensions

Check extensions

TT-based pruning

History-based pruning

SEE pruning

Internal iterative concepts where applicable

Mate-distance pruning

Do not merely implement techniques because their names are well known.

Read the current Stockfish implementation.

For every technique determine:

WHEN it activates
WHEN it is forbidden
what depth requirements apply
what margins are used
how history affects it
how improving/worsening positions affect it
how PV status affects it
how TT information affects it
how reductions are calculated

Translate those actual relationships into Java.

# ================================================== 16. LATE MOVE REDUCTIONS

Treat LMR as a major subsystem.

Study Stockfish's current reduction formulas/tables.

Implement Java equivalents.

Reduction should be influenced by the same kinds of information Stockfish currently uses where applicable, rather than simply:

if moveNumber > 3:
depth--

Reproduce the sophistication of the current design.

# ================================================== 17. STATIC EXCHANGE EVALUATION

Implement efficient Stockfish-style SEE.

Provide functionality equivalent to:

see()
see\_ge()

or their current equivalents.

Use SEE in move ordering and pruning where the current engine does so.

# ================================================== 18. DRAW DETECTION

Correctly support:

threefold repetition
search repetition handling
50-move rule
stalemate
insufficient material where required by engine behaviour

Ensure search cannot incorrectly prefer illegal/repeated positions because state history is incomplete.

# ================================================== 19. NNUE — DO NOT SUBSTITUTE A CLASSICAL EVALUATOR

Current Stockfish strength relies on NNUE.

Therefore the final engine must implement an NNUE inference system.

Study the CURRENT Stockfish NNUE source and documentation.

Understand:

input features
feature indexing
feature transformer
perspective handling
king-dependent features
incremental accumulator updates
refresh logic
network layers
quantisation
integer inference
PSQT component
positional component
network output scaling

Implement these concepts in Java.

# ================================================== 20. INCREMENTALLY UPDATABLE ACCUMULATORS

This is critical.

Do NOT recompute the complete neural network from scratch after every move.

Port the Stockfish accumulator concept.

When a piece moves:

remove old feature
add new feature

Update only affected accumulator components whenever possible.

Correctly handle refreshes when king-dependent feature buckets change.

Design accumulator stacks around the search's doMove/undoMove model.

# ================================================== 21. NNUE NETWORK FILES

Implement a Java NNUE network loader compatible with the network format required by the Stockfish version being targeted, where legally and technically appropriate.

The network must be validated before use.

Do not silently continue with random/uninitialised weights.

Allow something similar to:

setoption name EvalFile value network.nnue

If redistribution of the network requires additional licensing handling, document that clearly.

# ================================================== 22. NNUE PERFORMANCE

NNUE must not be implemented using generic matrix libraries in the search loop.

Implement efficient quantised integer inference.

Investigate Java optimisation opportunities including:

primitive arrays
loop unrolling
cache-friendly layouts
Vector API as an OPTIONAL accelerated implementation

Keep a portable scalar implementation as the correctness baseline.

# ================================================== 23. EVALUATION

Match the current Stockfish evaluation pipeline as closely as practical.

Study how current Stockfish combines/scales NNUE outputs and other search/evaluation context.

Do not resurrect the obsolete handcrafted Stockfish classical evaluator and call it modern Stockfish evaluation.

Provide:

eval

to inspect evaluation.

# ================================================== 24. TIME MANAGEMENT

Study current timeman.cpp and search time-management behaviour.

Support:

go movetime
go depth
go nodes
go infinite

and normal clocks:

wtime
btime
winc
binc
movestogo

Port/adapt Stockfish's concepts for:

optimum thinking time
maximum thinking time
remaining time
increment
move overhead
best-move stability
score stability
node distribution where applicable

Search must terminate reliably.

# ================================================== 25. UCI

Implement a genuinely compatible UCI interface.

Required commands include:

uci
debug
isready
setoption
ucinewgame
position
go
stop
ponderhit
quit

where supported by current Stockfish behaviour.

Example:

uci

should produce engine information followed by:

uciok

Then:

isready

must produce:

readyok

Support:

position startpos

position startpos moves e2e4 e7e5 g1f3

position fen

position fen moves ...

Search output should resemble legitimate UCI output:

info depth 18 seldepth 27 multipv 1 score cp 31 nodes 2849123 nps 2190000 hashfull 328 time 1301 pv e2e4 e7e5 g1f3

and ultimately:

bestmove e2e4 ponder e7e5

Do not fake these statistics.

# ================================================== 26. UCI OPTIONS

Implement appropriate equivalents of important Stockfish options, potentially including:

Threads
Hash
Clear Hash
Ponder
MultiPV
Move Overhead
Nodes Time
UCI\_Chess960
UCI\_ShowWDL
SyzygyPath
SyzygyProbeDepth
Syzygy50MoveRule
SyzygyProbeLimit
EvalFile

Use the current Stockfish option set as the reference.

# ================================================== 27. THREADING

Study CURRENT Stockfish thread architecture.

Do not simply parallelise every recursive call using CompletableFuture.

Chess-engine parallel search requires controlled shared-state behaviour.

Implement a Java search thread pool architecture based on Stockfish's design.

Start with one thread if necessary to establish correctness.

Then implement:

setoption name Threads value N

Pay particular attention to:

shared transposition table
thread-local histories
thread-local search stacks
NNUE accumulators
node counters
stop flags
root search
result selection

Use Java concurrency primitives carefully.

Avoid locks in extremely hot paths whenever practical.

# ================================================== 28. SYZYGY

Provide an architecture for Syzygy tablebase probing.

If feasible, implement compatible tablebase access.

Support relevant UCI configuration.

Do not let tablebase work delay basic engine correctness, but keep it as part of the full Stockfish parity target.

# ================================================== 29. BENCHMARK

Implement:

bench

Use deterministic benchmark positions.

Report at least:

nodes
time
nodes per second

Use this constantly while porting.

# ================================================== 30. STOCKFISH DIFFERENTIAL TESTING

Where possible, use the official Stockfish executable as a DEVELOPMENT ORACLE, not as the engine powering JengaFish.

Automate comparisons.

For identical FENs compare:

legal moves
perft
evaluation where meaningful
search results
mate detection
UCI behaviour

JengaFish must calculate its own moves.

Never secretly call Stockfish to obtain bestmove during normal operation.

# ================================================== 31. SEARCH TRACE MODE

Add an optional developer mode:

setoption name SearchTrace value true

or equivalent.

Allow diagnostic information about:

depth
TT hits
cutoffs
null-move attempts
null-move cutoffs
LMR
ProbCut
singular extensions
SEE pruning
history pruning
qsearch nodes
NNUE evaluations

This will make it possible to determine WHY Java and Stockfish diverge.

It must be disabled by default because tracing destroys search performance.

# ================================================== 32. TEST SUITE

Create extensive JUnit tests.

Cover:

FEN
bitboards
attacks
moves
move generation
legal moves
make/unmake
null moves
castling
en passant
promotion
checks
pins
checkmate
stalemate
repetition
rule 50
Zobrist
SEE
TT
history tables
NNUE feature indexing
NNUE accumulator updates
NNUE inference
UCI parsing
time controls
perft

Add randomised make/unmake tests.

After arbitrary sequences:

undo every move

and verify the original position and hashes are exactly restored.

# ================================================== 33. VALIDATION AGAINST STOCKFISH

Create a regression corpus containing thousands of positions.

For each position test appropriate properties against the reference implementation.

Correctness priority:

1. FEN parsing
2. attack generation
3. pseudo-legal moves
4. legal moves
5. make/unmake
6. perft
7. SEE
8. hashing
9. NNUE inference
10. search
11. time management
12. multithreading

Do not tune search around bugs in lower layers.

# ================================================== 34. PERFORMANCE PROFILING

Use JMH or another suitable methodology for isolated performance testing where useful.

Measure:

move generation
doMove/undoMove
attack generation
SEE
TT probes
NNUE updates
NNUE inference
qsearch
full search NPS

Use JVM profiling to identify:

allocation
GC pressure
cache-unfriendly structures
virtual-call overhead
bounds-check overhead
branch-heavy code

Optimise based on measurements.

# ================================================== 35. DEVELOPMENT ORDER

Do NOT attempt to write everything simultaneously without verification.

MILESTONE A

UCI shell
types
Move
Position
FEN
bitboards

MILESTONE B

attack generation
move generation
doMove
undoMove
perft

All major perft tests must pass.

MILESTONE C

Zobrist
TT
SEE
MovePicker
history structures

MILESTONE D

iterative deepening
PVS/alpha-beta
qsearch
basic search

The engine can now genuinely play chess.

MILESTONE E

Stockfish search heuristics
LMR
NMP
ProbCut
futility mechanisms
singular extensions
advanced histories
correction histories

MILESTONE F

NNUE parser
features
accumulators
inference
incremental updates

MILESTONE G

time management
complete UCI options
ponder
MultiPV

MILESTONE H

multithreading

MILESTONE I

Syzygy
benchmarking
profiling
optimisation

# ================================================== 36. CRITICAL RULE: DON'T SIMPLIFY AWAY THE INTERESTING PART

When Stockfish contains a complicated algorithm, do not automatically replace it with a textbook approximation because that is easier.

The entire purpose of this project is to understand and reproduce the sophisticated engineering responsible for Stockfish's strength.

For every significant subsystem:

READ CURRENT STOCKFISH SOURCE
↓
UNDERSTAND IT
↓
DOCUMENT THE MECHANISM
↓
PORT THE SEMANTICS TO JAVA
↓
TEST
↓
BENCHMARK
↓
CONTINUE

If Stockfish uses a complicated formula, history relationship, reduction table, pruning condition or NNUE optimisation that materially affects engine behaviour, investigate it rather than omitting it without explanation.

# ================================================== 37. EQUALLY IMPORTANT RULE: DON'T TRANSLATE C++ BADLY

Java is not C++.

Preserve algorithms, not inappropriate language constructs.

Examples:

C++ templates
→ specialised Java implementations/generics only where they do not hurt performance.

Pointer arithmetic
→ primitive-array indexing.

Compact structs
→ packed primitive arrays or carefully designed Java objects.

Compile-time tables
→ static final precomputed arrays.

SIMD intrinsics
→ scalar baseline plus optional Java Vector API implementation.

std::atomic
→ Java atomics/volatile/VarHandle where appropriate.

Do not turn elegant low-level C++ into thousands of allocation-heavy Java objects.

# ================================================== 38. LICENSING

Because this project deliberately derives from Stockfish, include:

COPYING.txt
LICENSE information
Stockfish attribution
original project URL
appropriate copyright notices
source availability information

Use GNU GPL v3 for the derivative project as required.

Do not remove Stockfish authorship notices from directly translated/adapted material.

Add:

README.md

explaining that JengaFish is a Java port/derivative/reimplementation based on Stockfish and is not an official Stockfish project.

# ================================================== 39. FIRST USABLE BUILD

Produce an executable JAR.

I should eventually be able to run:

java -jar JengaFish.jar

and enter:

uci

then receive something similar to:

id name JengaFish
id author George Miller and Stockfish developers
option name Hash type spin default 16 min 1 max ...
option name Threads type spin default 1 min 1 max ...
...
uciok

Then:

isready

returns:

readyok

Then:

position startpos moves e2e4 e7e5 g1f3

go depth 15

must cause JengaFish itself to perform the search and eventually output:

bestmove ...

# ================================================== 40. END GOAL

The eventual target is not:

"a decent Java chess engine."

The target is:

A serious Java translation/reimplementation of the modern Stockfish engine architecture.

Aim for functional parity first.

Then measure the performance difference caused by Java/JVM versus Stockfish C++.

Do not claim equal Elo or equal performance without empirical testing.

After the command-line engine is stable, a completely separate JavaFX GUI will be built around the UCI engine.

For now:

NO GUI.

Concentrate entirely on chess-engine correctness, Stockfish architectural fidelity, NNUE, search strength, UCI compatibility and performance.