# JengaFish — JavaFX edition

A replacement GUI for your existing JengaFish 0.1.0 project. Java 17 required.

## Install in NetBeans

1. Back up your existing JengaFish project.
2. Extract this ZIP into the existing **JengaFish project folder** (the folder containing pom.xml). Merge src and replace all supplied files.
3. Keep your original engine sources, networks folder, and src/main/resources/images folder.
4. In NetBeans choose **Clean and Build**, then **Run Project**.

The first build downloads JavaFX dependencies. This archive is an update, not a standalone engine project: it does not repeat the engine sources or the large NNUE network.

All six old GUI filenames are replaced, so you can merge the folders without removing individual Swing files. Additional JavaFX classes are supplied in the same package, com.jengacode.jengafish.gui. Main.java, pom.xml and nbactions.xml are included.

After building, **Open-JengaFish-GUI.bat** launches the new desktop application. It uses target/JengaFish.jar and the dependencies in target/lib. Do not launch the older root-level JengaFish.jar. Retain target/lib alongside the new JAR.

On Linux/macOS: run sh run-gui.sh from the project folder, after building on that computer. Maven chooses platform-specific JavaFX dependencies; build again when switching operating systems.

Alternatively use mvn clean javafx:run to build and launch directly.

## The new interface

- Illustrated welcome screen with original AI-generated chess artwork.
- Choose White or Black; White always makes the first move.
- Strength slider from 100 to 3500.
- Sage, Walnut and Midnight board themes.
- A responsive board, player cards and paired White/Black move columns.
- Click or drag to move, with legal destinations, last-move highlights and check indication.
- Short move animations and a promotion selector.
- Undo turn, flip board, new game, resignation and Copy PGN.
- Click any move or use the history arrows to review a position. Select Live to resume play. Reviewing never changes the live game.
- The engine keeps thinking off the JavaFX thread; cancelled search results cannot modify a new game.

The numeric strength is a difficulty scale, not a calibrated Elo rating. The game is untimed; the infinity symbols indicate no clock. The interface does not imply an online account or connection.

## Move notation

The display uses algebraic notation rather than UCI coordinates:

| Meaning | Example |
| --- | --- |
| Pawn move | e4 |
| Knight move | Nf3 |
| Capture | Bxe5 |
| Pawn capture / en passant | exd6 |
| Rooks sharing a destination | Rae1 / Rhe1 |
| Same-file disambiguation | R1a2 / R3a2 |
| File and rank both needed | Nb1d2 |
| Kingside castling | O-O |
| Queenside castling | O-O-O |
| Check | + |
| Double check | ++ |
| Checkmate | # |
| Promotion | e8=Q |
| Promotion capture with check | axb8=Q+ |

Castling uses the letter O. As requested, the display distinguishes double check with ++. Standard PGN uses + for any non-mating check, so Copy PGN normalizes ++ to +. Mate takes precedence and always ends in #. Disambiguation considers only legal moves, including pinned pieces.

## Your piece artwork

Your existing PNG files are loaded from src/main/resources/images:

PawnW/PawnB, KnightW/KnightB, BishW/BishB, RookW/RookB, QueenW/QueenB, KingW/KingB, all with .png extensions. The existing lowercase rookB.png is also supported.

If a piece image is absent, a chess glyph is drawn instead. The new themes draw the squares directly; BoardEmpty.png and the Spot PNGs are no longer needed but can remain in the folder. The generated welcome artwork is already included at src/main/resources/com/jengacode/jengafish/gui/welcome.png.

## Text engine

Use run-engine.bat or:

    java -Xmx768m -jar target/JengaFish.jar --uci

The engine still receives and returns UCI coordinate moves. Only the GUI's visible move list uses algebraic notation. The original Open-JengaFish.bat text launcher continues to call run-engine.bat.

## Verification

See verification/RESULTS.md for the checks performed. The verification Java files live outside Maven's normal source directories and do not alter the original engine tests.

This release was checked on a Linux JavaFX headless rendering backend, including real search callbacks. Windows launch scripts are provided; their actual desktop appearance and your own PNG files should be checked on your Windows machine.

## Source and artwork

The GUI is GPL-3.0-or-later, consistent with the existing engine. Retain the project's original COPYING and Stockfish notices. The interface is an original design inspired by familiar chess website layouts.

The welcome image was generated using the built-in image-generation tool and is bundled unchanged. ARTWORK.md records its prompt. JavaFX Maven setup reference: https://openjfx.io/openjfx-docs/
