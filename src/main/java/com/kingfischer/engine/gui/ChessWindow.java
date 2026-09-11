// SPDX-License-Identifier: GPL-3.0-or-later
package com.kingfischer.engine.gui;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.*;

public final class ChessWindow extends Application {
  private GameView game;
  private Stage window;

  @Override
  public void start(Stage stage) {
    window = stage;
    stage.setTitle("KingFischer 2.0 · Your chess room");
    stage.setMinWidth(860);
    stage.setMinHeight(720);
    showWelcome(new SetupDialog.Settings(0, 1500, BoardTheme.SAGE));
    stage.setOnCloseRequest(
        e -> {
          if (game != null) game.close();
        });
    stage.show();
  }

  private void showWelcome(SetupDialog.Settings settings) {
    Scene s = new Scene(SetupDialog.content(settings, this::startGame, null), 880, 740);
    Ui.style(s);
    window.setScene(s);
    window.sizeToScene();
    window.centerOnScreen();
  }

  private void startGame(SetupDialog.Settings settings) {
    if (game != null) game.close();
    game = new GameView(settings, this::newGame);
    Scene s = new Scene(game, 1160, 840);
    Ui.style(s);
    window.setScene(s);
    window.setMinWidth(900);
    window.setMinHeight(760);
    window.sizeToScene();
    window.centerOnScreen();
    game.begin();
  }

  private void newGame(SetupDialog.Settings settings) {
    Stage setup = new Stage();
    setup.initOwner(window);
    setup.initModality(Modality.WINDOW_MODAL);
    setup.setTitle("KingFischer 2.0 · New game");
    setup.setResizable(false);
    Scene s =
        new Scene(
            SetupDialog.content(
                settings,
                next -> {
                  setup.close();
                  startGame(next);
                },
                setup::close),
            880,
            760);
    Ui.style(s);
    setup.setScene(s);
    setup.show();
  }

  @Override
  public void stop() {
    if (game != null) game.close();
  }

  public static void launchGui() {
    Application.launch(ChessWindow.class);
  }
}
