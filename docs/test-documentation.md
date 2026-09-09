# Snake Game Server - Testdokumentation

## Auftrag und Testziel

Diese Dokumentation beschreibt die Anforderungen und Testfälle für den Snake Game
Server. Der aktuelle Anwendungsschwerpunkt ist die Verwaltung von Spielern,
Spielen und WebSocket-Verbindungen.

Die Testfälle prüfen sowohl die Services direkt als auch die WebSocket-Schnittstelle.
Die Spalten `Ist-Ergebnis` und `Status` werden während der Testausführung ergänzt.

## Starten

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.venv\Scripts\Activate.ps1
uvicorn snake_game_server.app:app --reload
```

WebSocket-Endpunkt:

```text
ws://localhost:8000/ws/game?player_id=<player-id>
```

Automatisierte Tests werden mit folgendem Befehl ausgeführt:

```powershell
pytest
```

## Anforderungen

| ANF-ID | Priorität | Anforderung                                                                 |
| ------ | --------- | --------------------------------------------------------------------------- |
| ANF-01 | hoch      | Spieler kann über `player_id` eine WebSocket-Verbindung herstellen.         |
| ANF-02 | mittel    | Neue `player_id` wird angelegt und bei erneuter Verbindung wiederverwendet. |
| ANF-03 | hoch      | Verbindung ohne `player_id` wird mit Statuscode `1008` abgelehnt.           |
| ANF-04 | hoch      | Ein verbundener Spieler kann ein neues Spiel erstellen.                     |
| ANF-05 | hoch      | Neues Spiel erhält eine eindeutige ID und enthält den Ersteller.            |
| ANF-06 | hoch      | Spieler kann einem bestehenden Spiel über dessen ID beitreten.              |
| ANF-07 | mittel    | Beim Beitritt wird die aktuelle Spieleranzahl zurückgegeben.                |
| ANF-08 | hoch      | Beitritt zu einem unbekannten Spiel wird verständlich abgelehnt.            |
| ANF-09 | hoch      | Spieler kann ein Spiel verlassen.                                           |
| ANF-10 | mittel    | Leeres Spiel wird nach dem Entfernen des letzten Spielers gelöscht.         |
| ANF-11 | hoch      | Beim Spielwechsel wird der Spieler zuerst aus dem alten Spiel entfernt.     |
| ANF-12 | hoch      | Unbekannte oder ungültige Nachrichtentypen werden abgelehnt.                |
| ANF-13 | hoch      | Getrennte WebSocket-Verbindung wird aus dem Connection Manager entfernt.    |
| ANF-14 | mittel    | Einzelne Spieler können Nachrichten erhalten; Broadcast erreicht alle.      |

## Äquivalenzklassen und Grenzwerte

| Bereich             | Gültige Klasse                           | Ungültige Klasse                      | Vertreter                                   | Erwartung                                         |
| ------------------- | ---------------------------------------- | ------------------------------------- | ------------------------------------------- | ------------------------------------------------- |
| `player_id`         | Nichtleerer String                       | Fehlender Parameter                   | `player-1` / kein Parameter                 | Verbindung wird angenommen / mit `1008` abgelehnt |
| Spiel-ID            | Vorhandene String-ID                     | Nicht vorhandene ID                   | ID eines erstellten Spiels / `unknown-game` | Beitritt erfolgreich / Fehlermeldung              |
| Nachrichtentyp      | `create_game`, `join_game`, `leave_game` | Unbekannter Typ oder fehlendes `type` | gültiger Typ / `move`                       | Erwartete Antwort / Fehlermeldung                 |
| `join_game.game_id` | String                                   | Fehlendes Feld oder anderer Datentyp  | `"game_id": "..."` / `null`                 | Beitritt / Fehlermeldung                          |
| Spielmitglieder     | Kein, ein oder mehrere Spieler           | Entfernen eines unbekannten Spielers  | 0, 1, 2 Spieler                             | Zustand bleibt konsistent                         |

## Testfälle

### Verbindung und Spieler

| TC-ID | ANF-ID | Testfall                                                                  | Erwartung                                                    | Status |
| ----- | ------ | ------------------------------------------------------------------------- | ------------------------------------------------------------ | ------ |
| TC-01 | ANF-01 | Spieler verbindet sich. `player_id=player-1` verwenden.                   | Verbindung wird akzeptiert und der Spieler wird registriert. | offen  |
| TC-02 | ANF-02 | Spieler wird wiederverwendet. Mit derselben `player_id` erneut verbinden. | Es wird kein zweiter Spieler mit einer anderen ID erzeugt.   | offen  |
| TC-03 | ANF-03 | Verbindung ohne Spieler-ID. WebSocket ohne Query-Parameter öffnen.        | Verbindung wird mit Close-Code `1008` abgelehnt.             | offen  |
| TC-04 | ANF-13 | Verbindung wird entfernt. Verbindung öffnen und danach trennen.           | Spieler ist nicht mehr im Connection Manager registriert.    | offen  |

### Spiele erstellen und beitreten

| TC-ID | ANF-ID         | Testfall                                                                            | Erwartung                                                                  | Status |
| ----- | -------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------ |
| TC-05 | ANF-04, ANF-05 | Spiel erstellen. `{"type": "create_game"}` senden.                                  | Antwort enthält `type: "game_created"` und eine `game_id`.                 | offen  |
| TC-06 | ANF-05         | Spiel-ID ist eindeutig. Zwei Spiele mit verschiedenen Spielern erstellen.           | Die Antworten enthalten unterschiedliche `game_id`-Werte.                  | offen  |
| TC-07 | ANF-05         | Ersteller ist Spielmitglied. Spiel erstellen und Zustand prüfen.                    | Das Spiel enthält den erstellenden Spieler genau einmal.                   | offen  |
| TC-08 | ANF-06, ANF-07 | Bestehendem Spiel beitreten. Spieler B sendet `join_game` mit der ID von Spieler A. | Antwort enthält `type: "game_joined"`, die Spiel-ID und `player_count: 2`. | offen  |
| TC-09 | ANF-08         | Unbekanntem Spiel beitreten. `game_id: "unknown-game"` senden.                      | Verständliche `ValueError`-Meldung; kein Spiel wird angelegt.              | offen  |
| TC-10 | ANF-08         | Spiel-ID fehlt. `{"type": "join_game"}` senden.                                     | Meldung `join_game requires a game_id`.                                    | offen  |
| TC-11 | ANF-08         | Falscher Datentyp. `game_id: 123` senden.                                           | Nachricht wird abgelehnt; es erfolgt kein Beitritt.                        | offen  |

### Spiele verlassen und Spielwechsel

| TC-ID | ANF-ID | Testfall                                                                           | Erwartung                                                       | Status |
| ----- | ------ | ---------------------------------------------------------------------------------- | --------------------------------------------------------------- | ------ |
| TC-12 | ANF-09 | Spiel verlassen. `{"type": "leave_game"}` senden.                                  | Antwort enthält `type: "game_left"` und die bisherige Spiel-ID. | offen  |
| TC-13 | ANF-10 | Letzten Spieler entfernen. Ein-Spieler-Spiel verlassen.                            | Das Spiel wird aus `games` entfernt.                            | offen  |
| TC-14 | ANF-10 | Spiel mit verbleibenden Spielern. Ein Spieler verlässt ein Zwei-Spieler-Spiel.     | Das Spiel bleibt mit genau einem Spieler bestehen.              | offen  |
| TC-15 | ANF-11 | Direkter Spielwechsel. Spieler A tritt Spiel 2 bei, während er in Spiel 1 ist.     | Spieler A ist nur noch Mitglied von Spiel 2.                    | offen  |
| TC-16 | ANF-09 | Spiel verlassen ohne Mitgliedschaft. `leave_game` ohne vorherigen Beitritt senden. | Antwort enthält `type: "game_left"` und `game_id: null`.        | offen  |

### Ungültige Nachrichten und Verteilung

| TC-ID | ANF-ID | Testfall                                                                      | Erwartung                                                             | Status |
| ----- | ------ | ----------------------------------------------------------------------------- | --------------------------------------------------------------------- | ------ |
| TC-17 | ANF-12 | Unbekannter Nachrichtentyp. `{"type": "move"}` senden.                        | Nachricht wird abgelehnt und die Verbindung kontrolliert geschlossen. | offen  |
| TC-18 | ANF-12 | Nachrichtentyp fehlt. `{}` senden.                                            | Nachricht wird abgelehnt und die Verbindung kontrolliert geschlossen. | offen  |
| TC-19 | ANF-14 | Nachricht an einzelnen Spieler. Zwei Spieler verbinden und einen adressieren. | Nur dieser Spieler erhält die Nachricht.                              | offen  |
| TC-20 | ANF-14 | Broadcast. Zwei Spieler verbinden und Broadcast auslösen.                     | Beide Spieler erhalten dieselbe Nachricht.                            | offen  |

## Automatisierte Testdateien

Die Testfälle sollen nach Verantwortungsbereich abgelegt werden:

| Testbereich         | Testdatei                               |
| ------------------- | --------------------------------------- |
| `PlayerService`     | `tests/unit/test_player_service.py`     |
| `Game`-Modell       | `tests/unit/test_game.py`               |
| `GameService`       | `tests/unit/test_game_service.py`       |
| `ConnectionManager` | `tests/unit/test_connection_manager.py` |
| WebSocket-Endpunkt  | `tests/integration/test_game_socket.py` |

## Traceability Matrix

| Requirement | Testfälle           |
| ----------- | ------------------- |
| ANF-01      | TC-01               |
| ANF-02      | TC-02               |
| ANF-03      | TC-03               |
| ANF-04      | TC-05               |
| ANF-05      | TC-05, TC-06, TC-07 |
| ANF-06      | TC-08               |
| ANF-07      | TC-08               |
| ANF-08      | TC-09, TC-10, TC-11 |
| ANF-09      | TC-12, TC-16        |
| ANF-10      | TC-13, TC-14        |
| ANF-11      | TC-15               |
| ANF-12      | TC-17, TC-18        |
| ANF-13      | TC-04               |
| ANF-14      | TC-19, TC-20        |

## Testauswertung

| Kennzahl             | Wert  |
| -------------------- | ----- |
| Anzahl Anforderungen | 14    |
| Anzahl Testfälle     | 20    |
| Bestanden            | offen |
| Fehlgeschlagen       | offen |
| Nicht ausgeführt     | 20    |
