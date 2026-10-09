# NVDA Add-on: Developer Status Panel

An NVDA add-on that keeps browse/focus mode, virtual buffer state and the focused object visible at all times. Key guides use your actual NVDA modifier key (e.g. NonConvert+Space). English and Japanese UI.

## Why

When verifying web pages or apps with NVDA, it is often hard to tell why something is not being read: is NVDA in browse mode or focus mode? Is there a virtual buffer at all, and has it finished loading? This add-on shows that information in a small floating panel, so you can see NVDA's state at a glance while testing.

## Features

- Always-visible panel that is shown when NVDA starts, without taking focus
- Shows the following, updated every 0.3 seconds:
  - Current mode (browse mode / focus mode)
  - Virtual buffer state (present or not, ready or loading, class name such as `Chromium`)
  - Name, role and states of the focused object
  - App name
  - Active NVDA modifier keys
- Key guides use the actual key names of your NVDA modifier key settings, including the NonConvert, Convert and Escape keys of the Japanese version of NVDA
- "Toggle mode" and "Refresh virtual buffer" buttons that return focus to the previous app and run NVDA's own commands
- While you operate the panel, it keeps showing the state of the previous app
- "Enable monitoring" checkbox to pause updates (almost zero load while paused)
- "Keep this panel on top" checkbox
- Font selection
- Remembers panel size, position and settings
- English and Japanese UI, following NVDA's language setting

## Requirements

- NVDA 2026.1 or later
- Tested with the Japanese version of NVDA 2026.2jp

## Installation

1. Download the latest `.nvda-addon` file from [Releases](../../releases).
2. Open the downloaded file, or install it from the Add-on Store in NVDA ("Install from external source").
3. Restart NVDA when prompted.

## Usage

- The panel is shown automatically when NVDA starts.
- To show or hide the panel, press **NVDA modifier key+Ctrl+Shift+D** (NonConvert+Ctrl+Shift+D or Insert+Ctrl+Shift+D by default in the Japanese version of NVDA). You can also use **NVDA menu > Tools > Developer Status Panel**.
- Closing the panel with the × button only hides it. Show it again with the shortcut or the menu.
- The shortcut can be changed in NVDA's Input Gestures dialog, under the "Developer Status Panel" category.

## Settings file

Panel size, position, font and checkbox states are saved in `devStatusPanel.json` in NVDA's user configuration folder.

- Installed NVDA: `%APPDATA%\nvda\devStatusPanel.json`
- Portable NVDA: `userConfig\devStatusPanel.json` in the portable folder

Delete this file to reset the panel to its defaults. Nothing is written in secure mode (e.g. on the sign-in screen).

## Repository structure

```
nvda-dev-status-panel/
├─ addon/                          Contents of the .nvda-addon package
│  ├─ manifest.ini                 Add-on manifest (English)
│  ├─ globalPlugins/
│  │  └─ devStatusPanel/
│  │     └─ __init__.py            Add-on code
│  └─ locale/
│     └─ ja/
│        ├─ manifest.ini           Add-on name and description (Japanese)
│        └─ LC_MESSAGES/
│           ├─ nvda.po             Japanese translation
│           └─ nvda.mo             Compiled translation
├─ devStatusPanel.pot              Translation template
├─ CHANGELOG.md                    Changelog (English)
├─ CHANGELOG.ja.md                 Changelog (Japanese)
└─ README.md                       This file
```

## Building

An `.nvda-addon` file is a zip archive of the contents of the `addon/` folder (not the folder itself). Requires [GNU gettext](https://www.gnu.org/software/gettext/) for translations and `zip` (e.g. Git Bash or WSL on Windows).

```sh
# 1. Compile the translation
msgfmt -o addon/locale/ja/LC_MESSAGES/nvda.mo addon/locale/ja/LC_MESSAGES/nvda.po

# 2. Package the add-on
mkdir -p dist
cd addon && zip -r ../dist/devStatusPanel-1.0.0.nvda-addon . -x '*__pycache__*' && cd ..
```

Build output in `dist/` is not committed. Releases are published as assets on the [Releases](../../releases) page.

## Translation

All UI strings in the code are in English and are translated through gettext. To update the template after changing strings:

```sh
xgettext --language=Python --from-code=UTF-8 --add-comments=Translators: --keyword=_ \
  --package-name=devStatusPanel -o devStatusPanel.pot addon/globalPlugins/devStatusPanel/__init__.py
```

To add a new language, create `addon/locale/<lang>/LC_MESSAGES/nvda.po` from `devStatusPanel.pot`, and optionally `addon/locale/<lang>/manifest.ini` with a translated `summary` and `description`.

## License

Copyright (C) 2026 securecat

Licensed under the GNU General Public License, version 2 or (at your option) any later version (GPL-2.0-or-later), the same license family as NVDA. See [LICENSE](LICENSE).

## Changelog

### [1.0.0] - 2026-10-09

#### Added

- First stable release.
- English and Japanese user interface. The language follows NVDA's language setting automatically.
- In English, NVDA modifier key names are also shown in English (e.g. NonConvert+Space).
- English and Japanese versions of the add-on name and description shown in the Add-on Store and elsewhere.
- Translation template (`devStatusPanel.pot`).

#### Changed

- All strings in the code are now in English, and Japanese is provided through translation files (`locale/ja`). The Japanese UI is unchanged from v0.4.1.

See [CHANGELOG.md](CHANGELOG.md) for full history.

---

# NVDAアドオン: 開発者ステータスパネル

NVDAのブラウズモード／フォーカスモード、仮想バッファの状態、フォーカス中のオブジェクトを常時表示するNVDAアドオンです。操作ガイドは、実際に設定されているNVDA制御キーで表示します（例：無変換+Space）。日本語と英語に対応しています。

## 作った理由

NVDAでWebページやアプリを検証していると、読み上げられない原因がわからないことがよくあります。今はブラウズモードなのかフォーカスモードなのか、そもそも仮想バッファはあるのか、読み込みは終わっているのか、といったことが画面からはわかりません。このアドオンは、それらの情報を小さなパネルに常時表示して、検証中にNVDAの状態をひと目で確認できるようにします。

## 機能

- NVDAの起動時に、フォーカスを奪わずにパネルを常時表示
- 次の情報を0.3秒ごとに更新して表示
  - 現在のモード（ブラウズモード／フォーカスモード）
  - 仮想バッファの状態（有無、準備完了／読み込み中、`Chromium` などのクラス名）
  - フォーカス中のオブジェクトの名前、ロール、状態
  - アプリ名
  - 有効なNVDA制御キー
- 操作ガイドを、実際のNVDA制御キーの設定に合わせたキー名で表示（日本語版独自の無変換・変換・Escapeにも対応）
- 「モード切替」「仮想バッファ再読み込み」ボタン（直前のアプリにフォーカスを戻してから、NVDA本来のコマンドを実行）
- パネルを操作している間は、直前のアプリの状態を表示し続ける
- 「監視を有効にする」チェックボックスで更新を一時停止（停止中の負荷はほぼゼロ）
- 「このパネルを最前面に表示」チェックボックス
- フォントの変更
- パネルのサイズ、位置、設定を記憶
- 日本語と英語に対応（NVDAの言語設定に従って切り替え）

## 動作環境

- NVDA 2026.1 以降
- NVDA日本語版 2026.2jp で動作確認済み

## インストール

1. [Releases](../../releases) から最新の `.nvda-addon` ファイルをダウンロードします。
2. ダウンロードしたファイルを開くか、NVDAのアドオンストアの「外部ソースからインストール」でインストールします。
3. 確認が表示されたら、NVDAを再起動します。

## 使い方

- NVDAを起動すると、パネルが自動で表示されます。
- パネルの表示／非表示は **NVDA制御キー+Ctrl+Shift+D** で切り替えられます（日本語版NVDAの既定では 無変換+Ctrl+Shift+D または Insert+Ctrl+Shift+D）。**NVDAメニュー ＞ ツール ＞ 開発者ステータスパネル** からも切り替えられます。
- ×ボタンでパネルを閉じた場合は非表示になるだけです。ショートカットかメニューから再表示できます。
- ショートカットは、NVDAの「入力ジェスチャー」ダイアログの「開発者ステータスパネル」カテゴリで変更できます。

## 設定ファイル

パネルのサイズ、位置、フォント、チェックボックスの状態は、NVDAのユーザー設定フォルダ内の `devStatusPanel.json` に保存されます。

- インストール版のNVDA：`%APPDATA%\nvda\devStatusPanel.json`
- ポータブル版のNVDA：ポータブル版フォルダ内の `userConfig\devStatusPanel.json`

このファイルを削除すると、パネルは初期状態に戻ります。セキュアモード（サインイン画面など）では書き込みを行いません。

## ファイル構成

```
nvda-dev-status-panel/
├─ addon/                          .nvda-addon パッケージの中身
│  ├─ manifest.ini                 アドオンのマニフェスト（英語）
│  ├─ globalPlugins/
│  │  └─ devStatusPanel/
│  │     └─ __init__.py            アドオン本体のコード
│  └─ locale/
│     └─ ja/
│        ├─ manifest.ini           アドオンの名前と説明（日本語）
│        └─ LC_MESSAGES/
│           ├─ nvda.po             日本語の翻訳
│           └─ nvda.mo             コンパイル済みの翻訳
├─ devStatusPanel.pot              翻訳テンプレート
├─ CHANGELOG.md                    変更履歴
└─ README.md                       このファイル
```

## ビルド方法

`.nvda-addon` ファイルは、`addon/` フォルダの中身（フォルダそのものではありません）をzipにしたものです。翻訳のコンパイルには [GNU gettext](https://www.gnu.org/software/gettext/) を、パッケージ化には `zip` を使います（WindowsではGit BashやWSLなど）。

```sh
# 1. 翻訳をコンパイル
msgfmt -o addon/locale/ja/LC_MESSAGES/nvda.mo addon/locale/ja/LC_MESSAGES/nvda.po

# 2. アドオンをパッケージ化
mkdir -p dist
cd addon && zip -r ../dist/devStatusPanel-1.0.0.nvda-addon . -x '*__pycache__*' && cd ..
```

`dist/` に出力されたビルド結果はコミットしません。リリースは [Releases](../../releases) ページにアセットとして公開します。

## 翻訳

コード内のUI文字列はすべて英語で書かれていて、gettextで翻訳されます。文字列を変更した後は、次のコマンドでテンプレートを更新します。

```sh
xgettext --language=Python --from-code=UTF-8 --add-comments=Translators: --keyword=_ \
  --package-name=devStatusPanel -o devStatusPanel.pot addon/globalPlugins/devStatusPanel/__init__.py
```

新しい言語を追加するときは、`devStatusPanel.pot` をもとに `addon/locale/<言語>/LC_MESSAGES/nvda.po` を作成します。必要に応じて、翻訳した `summary` と `description` を書いた `addon/locale/<言語>/manifest.ini` も追加します。

## ライセンス

Copyright (C) 2026 securecat

GNU General Public License バージョン2、またはそれ以降のバージョン（GPL-2.0-or-later）で公開しています。NVDAと同じGPL系のライセンスです。[LICENSE](LICENSE) を参照してください。

## 変更履歴

### [1.0.0] - 2026-10-09

#### 追加

- 正式リリース。
- 日本語と英語の両方に対応しました。表示言語はNVDAの言語設定に従って自動で切り替わります。
- 英語表示では、NVDA制御キーの名前も英語で表示します（例：NonConvert+Space）。
- アドオンストアなどに表示されるアドオンの名前と説明も、日本語版と英語版を用意しました。
- 翻訳テンプレート（`devStatusPanel.pot`）を追加しました。

#### 変更

- コード内の文字列を英語にし、日本語は翻訳ファイル（`locale/ja`）から表示するようにしました。日本語表示の内容はv0.4.1から変わりません。

全履歴は [CHANGELOG.md](CHANGELOG.md) を参照。

