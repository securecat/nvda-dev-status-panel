# Accessibility

Last updated: 2026-11-07

## Priorities and Goals

Developer Status Panel is a tool for checking accessibility. When you test web pages or apps with NVDA, NVDA's state, such as browse mode or focus mode and whether the virtual buffer has finished loading, is not shown on screen, so it is hard to tell why something is not being read. This add-on shows that state in a small panel. The panel runs inside NVDA, so it also has to be usable for the people who use NVDA, such as developers and testers who are blind or have low vision.

This statement covers:

- The panel (its buttons, checkboxes and status rows)
- The "Developer Status Panel" item in the Tools menu of the NVDA menu, and the shortcut to show or hide the panel

For the UI, we target WCAG 2.2 Level AA, and we treat it as a minimum, not a ceiling. Some of our own rules are stricter than AA (see [Contributor Expectations](#contributor-expectations)). We have not had a third-party evaluation, so this is a target, not a claim of conformance.

## How the Panel Behaves

- The panel does not take focus when it appears, either when NVDA starts or when you show it with the shortcut or the menu. To move to the panel, use Alt+Tab
- The Tab key moves through the "Toggle mode" and "Refresh virtual buffer" buttons, and then the "Enable monitoring" and "Keep this panel on top" checkboxes, in the order they appear
- The status rows (Mode, Virtual buffer, NVDA key, App and Focus) are text, so the Tab key does not move to them. With NVDA, read them with object navigation
- The status rows update every 0.3 seconds. To stop the updates, turn off "Enable monitoring"
- The "Toggle mode" and "Refresh virtual buffer" buttons return focus to the previous app before running NVDA's own commands

## Supported Environments

- Operating systems: tested on Windows 11. We have not yet tested Windows 10
- Screen readers: tested with NVDA 2026.2 (international version) and the Japanese version of NVDA 2026.2jp, with both the English and Japanese interface. This is an NVDA add-on, so it does not run with other screen readers
- Display settings: tested with a Windows contrast theme and with display scaling (such as 150%)
- All features can be operated with a keyboard alone

## Known Limitations

- **When focus moves within the panel, NVDA's focus highlight and speech may not follow it.** This happens when you switch to the panel, and when you turn on "Keep this panel on top." The focus itself is on the expected control, so pressing Space or Enter works as usual.
- The panel's font is fixed to Meiryo 10 pt (or the system's sans-serif font if Meiryo is not available), and you cannot change its size in the panel.
  - Workaround: Windows display scaling enlarges the panel as well.

## Reporting Accessibility Barriers

Please report barriers through [GitHub Issues](https://github.com/securecat/nvda-dev-status-panel/issues). You can write in English or Japanese.

The following details help us, but all of them are optional:

- What you were trying to do
- The screen or feature you were using
- What happened, and what you expected
- Your OS version, NVDA version (international or Japanese version), and Developer Status Panel version
- Any assistive technology you use other than NVDA

You don't need to tell us about any disability. Screenshots and recordings are not required.

## Response Process

Developer Status Panel is developed by an individual, so we can't promise a deadline for replies or fixes. We will respond as quickly as we can.

- We will reply on the issue once we've seen your report
- If there is a workaround, we will share it
- Before releasing a fix, we may ask you to confirm that it works for you
- Fixes are recorded in [CHANGELOG.md](../CHANGELOG.md)

## Contributor Expectations

These expectations apply equally to human contributors and coding agents.

The panel is built with wxPython and is not a web page. Even so, when you change the UI, keep the following accessibility principles in mind and follow them as closely as you can:

- Use standard wx controls (`wx.Button`, `wx.CheckBox` and so on). Don't draw your own controls that NVDA cannot recognize
- Don't disable controls with `Disable()` or `Enable(False)`
- Don't remove or replace the system's focus indicator
- Keep text contrast at 7:1 or higher for body text and 4.5:1 or higher for secondary text, and check the panel with a Windows contrast theme as well
- Keep non-text elements, such as borders and icons, at 3:1 or higher against adjacent colors
- Use a minimum font size of 16px for Japanese and 14px for English
- Use a sans-serif font
- Don't dismiss status messages automatically
- Don't add anything that moves on its own, other than the status rows. Keep the "Enable monitoring" checkbox, which stops their updates

After the change, check that everything can be operated with a keyboard alone, and that NVDA reads the content correctly.

Create controls in the order they appear on screen, because the creation order becomes the Tab order and the order of NVDA's object navigation. Keep showing the panel without taking focus (`ShowWithoutActivating()`). Test with both the international and Japanese versions of NVDA, and with both the English and Japanese interface.

## Ownership and Maintenance

This statement is maintained by the maintainer, securecat. We update it when we add features or when the tested environments change.

## Feedback on This Statement

Suggestions about this statement or our approach to accessibility are also welcome through [GitHub Issues](https://github.com/securecat/nvda-dev-status-panel/issues).

---

# アクセシビリティ

最終更新：2026-11-07

## 優先事項と目標

開発者ステータスパネルは、アクセシビリティを検証するための道具です。NVDAでWebページやアプリを検証するとき、ブラウズモードかフォーカスモードか、仮想バッファの読み込みは終わっているか、といったNVDAの状態は画面に表示されないため、読み上げられない原因がわかりにくくなります。このアドオンは、その状態を小さなパネルに表示します。パネルはNVDAの中で動くので、NVDAを使う人（視覚障害のある開発者や検証者など）にとっても使えるものである必要があります。

この文書が対象とするのは、次のとおりです。

- パネル（ボタン、チェックボックス、状態表示）
- NVDAメニューの「ツール」にある「開発者ステータスパネル」と、パネルの表示／非表示を切り替えるショートカット

UIは WCAG 2.2 のレベル AA を目標とし、これを上限ではなく下限と考えています。AAより厳しい独自の基準もあります（[貢献者への期待](#貢献者への期待)を参照）。第三者による試験は受けていないため、これは目標であり、適合を表明するものではありません。

## パネルの動作

- パネルは、NVDAの起動時にも、ショートカットやメニューで表示したときにも、フォーカスを奪いません。パネルに移るには Alt+Tab を使います
- Tabキーでは、「モード切替」「仮想バッファ再読み込み」ボタン、「監視を有効にする」「このパネルを最前面に表示」チェックボックスの順に、表示どおりの順序で移動します
- 状態表示（モード、仮想バッファ、NVDA制御キー、アプリ、フォーカス）はテキストなので、Tabキーでは移動しません。NVDAでは、オブジェクトナビゲーションで読みます
- 状態表示は0.3秒ごとに更新されます。更新を止めるには、「監視を有効にする」をオフにします
- 「モード切替」「仮想バッファ再読み込み」ボタンは、直前のアプリにフォーカスを戻してから、NVDA本来のコマンドを実行します

## 対応している環境

- OS：Windows 11 で動作を確認済み。Windows 10 ではまだ試していません
- スクリーンリーダー：NVDA 2026.2（国際版）と NVDA日本語版 2026.2jp で、英語表示と日本語表示の両方を確認済み。NVDAのアドオンなので、ほかのスクリーンリーダーでは動きません
- 表示の設定：Windows のコントラストテーマと、表示スケールの拡大（150%など）で確認済み
- すべての機能を、キーボードだけで操作できます

## 既知の制限

- **パネル内でフォーカスが移ったときに、NVDAのフォーカスのハイライトや読み上げが追いつかないことがあります。** パネルに切り替えたときと、「このパネルを最前面に表示」をオンにしたときに起こります。フォーカス自体は目的のコントロールにあるので、SpaceキーやEnterキーはいつもどおり使えます。
- パネルのフォントはメイリオ 10pt（メイリオがない場合はシステムのsans-serif系フォント）に固定で、パネルの中では大きさを変えられません。
  - 回避策：Windows の表示スケールを拡大すると、パネルも大きくなります。

## アクセシビリティの問題を報告する

問題は [GitHub Issues](https://github.com/securecat/nvda-dev-status-panel/issues) で報告してください。日本語でも英語でも構いません。

次のことを書いてもらえると助かりますが、どれも任意です。

- 何をしようとしていたか
- 使っていた画面や機能
- 何が起きたか、どうなると思っていたか
- OSのバージョン、NVDAのバージョン（国際版か日本語版か）、開発者ステータスパネルのバージョン
- NVDA以外に使っている支援技術

障害の有無や内容を書く必要はありません。スクリーンショットや録画も必須ではありません。

## 対応の流れ

開発者ステータスパネルは個人で開発しているため、返信や修正の期限はお約束できません。それでも、できるかぎり早く対応します。

- 報告を確認したら、Issue で返信します
- 回避策があれば、お知らせします
- 修正をリリースする前に、問題が解消したかどうかの確認をお願いすることがあります
- 修正の内容は [CHANGELOG.md](../CHANGELOG.md) に記載します

## 貢献者への期待

ここに挙げることは、人間の貢献者にもコーディングエージェントにも、同じように求めます。

パネルは wxPython で作っていて、ウェブページではありません。それでも、UIを変更するときは、次のアクセシビリティの考え方を意識して、できるだけ守ってください。

- wx の標準のコントロール（`wx.Button`・`wx.CheckBox` など）を使う。NVDAが認識できない独自のコントロールを描かない
- `Disable()` や `Enable(False)` でコントロールを無効にしない
- システムのフォーカスインジケーターを消したり、置き換えたりしない
- テキストのコントラスト比は、本文で 7:1 以上、補足的なテキストで 4.5:1 以上にする。Windows のコントラストテーマでも確認する
- 境界線やアイコンなど、テキスト以外の要素も、隣り合う色に対して 3:1 以上にする
- 文字サイズは、日本語で 16px 以上、英語で 14px 以上にする
- sans-serif 系のフォントを使う
- ステータスメッセージを自動で消さない
- 状態表示のほかに、ひとりでに動くものを作らない。状態表示の更新を止められる「監視を有効にする」チェックボックスは残す

変更したあとは、キーボードだけですべて操作できること、NVDAで内容が正しく読み上げられることを確認してください。

コントロールは、画面に表示する順に作ってください。作った順序が、Tabキーの移動順とNVDAのオブジェクトナビゲーションの順序になるためです。パネルは、フォーカスを奪わずに表示する（`ShowWithoutActivating()`）ままにしてください。確認は、NVDAの国際版と日本語版の両方、英語表示と日本語表示の両方で行ってください。

## 責任者と保守

この文書は、メンテナーの securecat が管理しています。機能を追加したときや、動作を確認した環境が変わったときに更新します。

## この文書へのフィードバック

この文書やアクセシビリティへの取り組み方についての提案も、[GitHub Issues](https://github.com/securecat/nvda-dev-status-panel/issues) で受け付けています。
