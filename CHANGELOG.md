# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
## [1.0.0] - 2026-10-09

### Added

- First stable release.
- English and Japanese user interface. The language follows NVDA's language setting automatically.
- In English, NVDA modifier key names are also shown in English (e.g. NonConvert+Space).
- English and Japanese versions of the add-on name and description shown in the Add-on Store and elsewhere.
- Translation template (`devStatusPanel.pot`).

### Changed

- All strings in the code are now in English, and Japanese is provided through translation files (`locale/ja`).
- The labels of the "Toggle mode" and "Refresh virtual buffer" buttons now show the key in parentheses on a second line. This keeps the buttons from becoming too wide and makes them easier to click.
- The initial height of the panel now also includes room for the note shown while the panel is in use.

### Removed

- The "Font…" button. The panel now always uses Meiryo 10 pt (or the system's sans-serif font if Meiryo is not available). Font settings saved by earlier versions are ignored.

## [0.4.1] - 2026-10-09

### Fixed

- Fixed the panel window title from 「NVDA 開発者ステータス」 to 「NVDA 開発者ステータスパネル」 (versions up to 0.4.1 had a Japanese-only UI).

## [0.4.0] - 2026-10-09

### Changed

- The initial height of the panel is now determined automatically from its contents. If the saved height is not enough to show the buttons, the panel is enlarged when it is shown. The panel size does not change while in use, even when the displayed contents change.
- After changing the font, the panel also checks that its height is enough to show all contents.
- Moved the notes (shown while monitoring is paused or while the panel is in use) to the top of the panel and displayed them in red. When there is no note, the row is removed.
- Changed the wording of the notes.
- The default font candidates are now Meiryo only.

## [0.3.0] - 2026-10-09

### Added

- The panel now remembers its size and position. Settings are saved in `devStatusPanel.json` in NVDA's user configuration folder. If the saved position is off screen (e.g. after a change in monitor layout), the position is not restored.
- "Keep this panel on top" checkbox (on by default).
- "Font…" button. The chosen typeface and size are saved.
- The on/off state of "Enable monitoring" is now saved.

### Changed

- The default font of the panel is now a sans-serif font such as Meiryo instead of the Windows UI font.
- Added a one-line space above the buttons. Its height follows the font size.
- Settings are not written in secure mode (e.g. on the sign-in screen).

## [0.2.0] - 2026-10-09

### Added

- "Enable monitoring" checkbox. Turning it off stops status updates, reducing the load to almost zero.

### Fixed

- Long contents were cut off at the right edge of the panel. All values now wrap at the right edge, and the wrap position follows the panel width.
- Button labels could not be read because the buttons were narrower than their labels.
- Slightly enlarged the initial size of the panel.

## [0.1.0] - 2026-10-09

### Added

- Initial release. A verification panel for developers that always shows NVDA's status.
- The panel is shown on top when NVDA starts, without taking focus.
- The following information is updated every 0.3 seconds:
  - Current mode (browse mode / focus mode)
  - Whether there is a virtual buffer, and its state (ready / loading, class name)
  - Name, role and states of the focused object
  - App name
  - Active NVDA modifier keys
- Key guides are shown with the actual key names of the current NVDA modifier key settings (e.g. NonConvert+Space). The NonConvert, Convert and Escape settings specific to the Japanese version of NVDA are also supported.
- While the panel is in use, it keeps showing the state of the previous app.
- "Toggle mode" and "Refresh virtual buffer" buttons. They return focus to the previous app and then run NVDA's own commands.
- Shortcut to show or hide the panel (NVDA modifier key+Ctrl+Shift+D; NonConvert+Ctrl+Shift+D by default in the Japanese version).
- "Developer Status Panel" item in the Tools submenu of the NVDA menu.
- Closing the panel with the × button only hides it; it can be shown again with the shortcut or from the menu.

---

# 更新履歴

## [1.0.0] - 2026-10-09

### 追加

- 正式リリース。
- 日本語と英語の両方に対応しました。表示言語はNVDAの言語設定に従って自動で切り替わります。
- 英語表示では、NVDA制御キーの名前も英語で表示します（例：NonConvert+Space）。
- アドオンストアなどに表示されるアドオンの名前と説明も、日本語版と英語版を用意しました。
- 翻訳テンプレート（`devStatusPanel.pot`）を追加しました。

### 変更

- コード内の文字列を英語にし、日本語は翻訳ファイル（`locale/ja`）から表示するようにしました。
- 「モード切替」「仮想バッファ再読み込み」ボタンのラベルを2行にし、括弧内のキー名を2行目に表示するようにしました。ボタンが横に長くなりすぎず、クリックしやすくなります。
- パネルの初期の高さに、パネル操作中に表示される注釈の分も含めるようにしました。

### 削除

- 「フォント…」ボタンを削除しました。パネルのフォントは常にメイリオ 10pt（メイリオがない場合はシステムのsans-serif系フォント）になります。以前のバージョンで保存したフォント設定は使用しません。

## [0.4.1] - 2026-10-09

### 修正

- パネルのウィンドウタイトルを「NVDA 開発者ステータス」から「NVDA 開発者ステータスパネル」に修正しました。

## [0.4.0] - 2026-10-09

### 変更

- パネルの初期の高さを、内容に合わせて自動で決めるようにしました。保存済みの高さがボタンまで表示するのに足りない場合も、表示時に自動で広げます。使用中は表示内容が変わってもパネルのサイズは変わりません。
- フォントを変更したときも、内容がすべて見える高さになるよう確認するようにしました。
- 注釈文（監視停止中・パネル操作中の表示）をパネルの一番上に移動し、赤字で表示するようにしました。注釈がないときは行を詰めて表示します。
- 注釈文の文言を変更しました。
  - 「※監視を停止しています。監視を有効にすると再開します。」
  - 「※パネル操作中のため、直前のアプリの状態を表示しています。」
- 既定フォントの候補をメイリオのみにしました。

## [0.3.0] - 2026-10-09

### 追加

- パネルのサイズと位置を記憶するようにしました。設定はNVDAのユーザー設定フォルダ内の `devStatusPanel.json` に保存されます。モニター構成の変更などで保存位置が画面外になる場合は、位置を復元しません。
- 「このパネルを最前面に表示」チェックボックスを追加しました（既定でオン）。
- 「フォント…」ボタンを追加しました。選んだ書体とサイズは保存されます。
- 「監視を有効にする」のオン／オフも保存されるようにしました。

### 変更

- パネルの既定フォントを、WindowsのUIフォントからメイリオなどのsans-serif系フォントに変更しました。
- ボタンの上に1行分の空きを設けました。空きの高さはフォントサイズに追従します。
- セキュアモード（ログオン画面など）では設定ファイルに書き込まないようにしました。

## [0.2.0] - 2026-10-09

### 追加

- 「監視を有効にする」チェックボックスを追加しました。オフにすると状態の更新を停止し、負荷をほぼゼロにします。

### 修正

- 長い内容がパネルの右端で切れてしまう問題を修正しました。すべての値が右端で折り返して表示され、パネルの幅を変えると折り返し位置も追従します。
- ボタンの幅がラベルより狭く、ラベルが読めない問題を修正しました。
- パネルの初期サイズを少し大きくしました。

## [0.1.0] - 2026-10-09

### 追加

- 初回リリース。NVDAの状態を常時表示する、開発者の検証用パネルです。
- NVDAの起動時に、フォーカスを奪わずに最前面へパネルを表示します。
- 次の情報を0.3秒ごとに更新して表示します。
  - 現在のモード（ブラウズモード／フォーカスモード）
  - 仮想バッファの有無と状態（準備完了／読み込み中、クラス名）
  - フォーカス中のオブジェクトの名前、ロール、状態
  - アプリ名
  - 有効なNVDA制御キー
- 操作ガイドを、現在のNVDA制御キーの設定に合わせた実キー名（例：無変換+Space）で表示します。日本語版独自の無変換・変換・Escapeの設定にも対応しています。
- パネルを操作している間は、直前のアプリの状態を表示し続けます。
- 「モード切替」「仮想バッファ再読み込み」ボタンを追加しました。直前のアプリにフォーカスを戻してから、NVDA本来のコマンドを実行します。
- パネルの表示／非表示を切り替えるショートカットを追加しました（NVDA制御キー+Ctrl+Shift+D。日本語版の既定では無変換+Ctrl+Shift+D）。
- NVDAメニューの「ツール」に「開発者ステータスパネル」を追加しました。
- ×ボタンでパネルを閉じた場合は非表示になるだけで、ショートカットやメニューから再表示できます。
