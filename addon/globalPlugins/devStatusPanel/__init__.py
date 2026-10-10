# -*- coding: utf-8 -*-
# Developer Status Panel (devStatusPanel) v1.0.1
# Copyright (C) 2026 securecat
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version. See the file LICENSE for details.
#
# 開発者ステータスパネル：NVDAのモードや仮想バッファの状態を常時表示する検証用アドオン。
# NVDA日本語版 2026.2jp で動作確認。表示言語はNVDAの言語設定に従う（英語／日本語）。

import ctypes
import json
import os

import addonHandler
import api
import browseMode
import config
import core
import globalCommands
import globalPluginHandler
import globalVars
import gui
import NVDAState
import wx
from logHandler import log
from scriptHandler import script

# _() などの翻訳関数を、このアドオンの翻訳（locale/<言語>/LC_MESSAGES/nvda.mo）に向ける
addonHandler.initTranslation()

# ---------------------------------------------------------------------------
# 設定の保存（NVDAの設定フォルダに devStatusPanel.json を置く）
# ---------------------------------------------------------------------------

DEFAULT_SETTINGS = {
	"x": None,
	"y": None,
	"width": 560,
	"height": 345,
	"alwaysOnTop": True,
	"monitoring": True,
}

# パネルのフォントサイズ（pt）
FONT_SIZE = 10
# ボタンの高さ（文字の高さに対する倍率。2行のラベルと上下の余白が収まる高さ）
BUTTON_HEIGHT_RATIO = 2.5
# 使用するsans-serif系フォントの候補（上から順に、インストールされているものを使う）
SANS_SERIF_CANDIDATES = ("Meiryo", "メイリオ")


def _settingsPath():
	return os.path.join(NVDAState.WritePaths.configDir, "devStatusPanel.json")


def loadSettings():
	settings = dict(DEFAULT_SETTINGS)
	try:
		with open(_settingsPath(), encoding="utf-8") as f:
			settings.update(json.load(f))
	except FileNotFoundError:
		pass
	except Exception:
		log.debugWarning("devStatusPanel: failed to load settings", exc_info=True)
	return settings


def saveSettings(settings):
	if globalVars.appArgs.secure:
		# セキュアモード（ログオン画面など）では書き込まない
		return
	try:
		with open(_settingsPath(), "w", encoding="utf-8") as f:
			json.dump(settings, f, ensure_ascii=False, indent=2)
	except Exception:
		log.debugWarning("devStatusPanel: failed to save settings", exc_info=True)


def resolveFontFace():
	for candidate in SANS_SERIF_CANDIDATES:
		if wx.FontEnumerator.IsValidFacename(candidate):
			return candidate
	return None  # 見つからなければ wx の汎用 sans-serif（FONTFAMILY_SWISS）


# ---------------------------------------------------------------------------
# NVDA制御キーの実キー名
# ---------------------------------------------------------------------------

# 本家版の NVDAModifierKeys（ビットフラグ）
_CAPS_LOCK = 1
_NUMPAD_INSERT = 2
_EXTENDED_INSERT = 4


def _confGet(section, key, default):
	try:
		return config.conf[section][key]
	except Exception:
		return default


def getNVDAKeyNames():
	"""現在有効なNVDA制御キーを、表示に使う優先順で返す。"""
	names = []
	# 日本語版独自の設定（本家版には存在しないので既定値付きで読む）
	if _confGet("keyboard", "useNonConvertAsNVDAModifierKey", False):
		# Translators: Name of the IME NonConvert key (無変換) used as an NVDA modifier key.
		names.append(_("NonConvert"))
	if _confGet("keyboard", "useConvertAsNVDAModifierKey", False):
		# Translators: Name of the IME Convert key (変換) used as an NVDA modifier key.
		names.append(_("Convert"))
	if _confGet("keyboard", "useEscapeAsNVDAModifierKey", False):
		# Translators: Name of the Escape key used as an NVDA modifier key.
		names.append(_("Escape"))
	flags = _confGet("keyboard", "NVDAModifierKeys", _NUMPAD_INSERT | _EXTENDED_INSERT)
	if flags & _EXTENDED_INSERT:
		# Translators: Name of the Insert key used as an NVDA modifier key.
		names.append(_("Insert"))
	if flags & _NUMPAD_INSERT:
		# Translators: Name of the numpad Insert key used as an NVDA modifier key.
		names.append(_("Numpad Insert"))
	if flags & _CAPS_LOCK:
		# Translators: Name of the CapsLock key used as an NVDA modifier key.
		names.append(_("CapsLock"))
	return names or ["NVDA"]


def keyLabel(rest):
	"""'F1' -> '無変換+F1'（英語表示では 'NonConvert+F1'）のように、主に使うNVDA制御キーで表記する。"""
	return "%s+%s" % (getNVDAKeyNames()[0], rest)


# ---------------------------------------------------------------------------
# 状態の取得
# ---------------------------------------------------------------------------

_OWN_PID = os.getpid()


def _isOwnProcess(obj):
	try:
		return obj.processID == _OWN_PID
	except Exception:
		return False


def describeState(focus):
	"""フォーカスオブジェクトから表示用の状態を作る。"""
	info = {"mode": "-", "buffer": "-", "object": "-", "app": "-"}
	if focus is None:
		return info
	try:
		ti = focus.treeInterceptor
	except Exception:
		ti = None

	if ti is None:
		# Translators: Mode shown when the focused object has no tree interceptor.
		info["mode"] = _("Normal (browse mode not applicable)")
		# Translators: Virtual buffer status shown when there is no virtual buffer.
		info["buffer"] = _("None")
	elif isinstance(ti, browseMode.BrowseModeTreeInterceptor):
		# Translators: Name of NVDA's focus mode / browse mode.
		info["mode"] = _("Focus mode") if ti.passThrough else _("Browse mode")
		try:
			# Translators: Virtual buffer load state (ready / still loading).
			ready = _("ready") if ti.isReady else _("loading…")
		except Exception:
			# Translators: Virtual buffer load state when it cannot be determined.
			ready = _("unknown")
		# Translators: Virtual buffer status. {state} is the load state, {cls} is the class name (e.g. Chromium).
		info["buffer"] = _("Present ({state} / {cls})").format(state=ready, cls=type(ti).__name__)
	else:
		# Translators: Mode shown when the tree interceptor does not support browse mode.
		info["mode"] = _("TreeInterceptor without browse mode support")
		# Translators: Virtual buffer status. {cls} is the class name of the tree interceptor.
		info["buffer"] = _("Present ({cls})").format(cls=type(ti).__name__)

	try:
		# Translators: Shown when the focused object has no name.
		name = focus.name or _("(no name)")
		role = focus.role.displayString
		states = ", ".join(sorted(s.displayString for s in focus.states))
		if states:
			# Translators: Focused object info. {name}, {role} and {states} come from NVDA.
			info["object"] = _("{name} / {role} ({states})").format(name=name, role=role, states=states)
		else:
			# Translators: Focused object info without states.
			info["object"] = _("{name} / {role}").format(name=name, role=role)
	except Exception:
		log.debugWarning("devStatusPanel: object info failed", exc_info=True)
	try:
		info["app"] = focus.appModule.appName
	except Exception:
		pass
	return info


# ---------------------------------------------------------------------------
# パネル
# ---------------------------------------------------------------------------

_GA_ROOT = 2


def inUseNote():
	# Translators: Note shown while the panel itself has focus.
	return _("Note: Showing the state of the previous app because the panel is in use.")


def pausedNote():
	# Translators: Note shown while monitoring is paused.
	return _("Note: Monitoring is paused. Enable monitoring to resume.")


def wrapText(dc, text, width):
	"""StaticText.Wrap() と同じく、空白の位置でだけ幅に合わせて折り返した文字列を返す。"""
	lines = []
	for paragraph in text.split("\n"):
		line = ""
		for word in paragraph.split(" "):
			candidate = word if not line else line + " " + word
			if line and dc.GetTextExtent(candidate)[0] > width:
				lines.append(line)
				line = word
			else:
				line = candidate
		lines.append(line)
	return "\n".join(lines)


_BASE_STYLE = wx.CAPTION | wx.CLOSE_BOX | wx.RESIZE_BORDER | wx.FRAME_TOOL_WINDOW


class StatusPanel(wx.Frame):
	def __init__(self, plugin):
		self.plugin = plugin
		self.settings = plugin.settings
		style = _BASE_STYLE | (wx.STAY_ON_TOP if self.settings["alwaysOnTop"] else 0)
		super().__init__(gui.mainFrame, title=_("NVDA Developer Status Panel"), style=style)
		self.panel = panel = wx.Panel(self)
		# 折り返し前の元テキスト（Wrap() はラベルに改行を挿入するため別に持つ）
		self._raw = {}
		self._saveTimer = None

		# コントロールは表示順に作る（Tabキーやオブジェクトナビゲーションの順序になるため）
		# 上段：操作ボタン
		self.toggleButton = wx.Button(panel)
		self.refreshButton = wx.Button(panel)
		self.toggleButton.Bind(wx.EVT_BUTTON, lambda e: self.plugin.runOnTarget(self.plugin.doToggleMode))
		self.refreshButton.Bind(wx.EVT_BUTTON, lambda e: self.plugin.runOnTarget(self.plugin.doRefreshBuffer))
		buttons = wx.BoxSizer(wx.HORIZONTAL)
		buttons.Add(self.toggleButton, flag=wx.RIGHT, border=6)
		buttons.Add(self.refreshButton)

		# 中段：チェックボックス（横並び）
		# Translators: Checkbox label.
		self.monitorCheck = wx.CheckBox(panel, label=_("Enable monitoring"))
		self.monitorCheck.SetValue(self.settings["monitoring"])
		self.monitorCheck.Bind(wx.EVT_CHECKBOX, self.onMonitorToggle)
		# Translators: Checkbox label.
		self.topCheck = wx.CheckBox(panel, label=_("Keep this panel on top"))
		self.topCheck.SetValue(self.settings["alwaysOnTop"])
		self.topCheck.Bind(wx.EVT_CHECKBOX, self.onTopToggle)
		checks = wx.BoxSizer(wx.HORIZONTAL)
		checks.Add(self.monitorCheck, flag=wx.RIGHT, border=16)
		checks.Add(self.topCheck)

		divider = wx.StaticLine(panel)

		# 下段：注釈と状態表示
		self.note = wx.StaticText(panel, label="")
		self.note.SetForegroundColour(wx.Colour(200, 0, 0))
		self.grid = grid = wx.FlexGridSizer(cols=2, vgap=4, hgap=8)
		grid.AddGrowableCol(1)
		self.labels = {}
		self.titles = []
		# 行数が変わりやすいフォーカスは最後に置き、増えても下に伸びるだけにする
		for key, title in (
			# Translators: Row labels in the panel.
			("mode", _("Mode:")),
			("buffer", _("Virtual buffer:")),
			("nvdaKey", _("NVDA key:")),
			("app", _("App:")),
			("object", _("Focus:")),
		):
			titleCtrl = wx.StaticText(panel, label=title)
			self.titles.append(titleCtrl)
			grid.Add(titleCtrl)
			text = wx.StaticText(panel, label="-")
			grid.Add(text, flag=wx.EXPAND)
			self.labels[key] = text

		root = wx.BoxSizer(wx.VERTICAL)
		root.Add(buttons, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=8)
		root.Add(checks, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=8)
		root.Add(divider, flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, border=8)
		# 注釈の有無で状態表示がずれないよう、注釈がないときも領域を空けておく
		root.Add(self.note, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=8)
		root.Add(grid, flag=wx.ALL | wx.EXPAND, border=8)
		self.rootSizer = root
		panel.SetSizer(root)

		# ボタンの幅を最初から決めておくため、表示前にラベルを入れておく
		self._updateButtonLabels()
		self.applyFont()
		self.SetMinSize((360, 220))
		self._restoreGeometry()
		# 表示前でも、パネルの幅をウィンドウに合わせてから折り返し位置を決める
		self.Layout()
		self._rewrapAll()

		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(wx.EVT_SIZE, self.onSize)
		self.Bind(wx.EVT_MOVE, self.onMove)

	# --- サイズと位置の記憶 -----------------------------------------------

	def _reserveNoteArea(self):
		"""注釈の領域を、どの注釈を今の幅で折り返して表示しても収まる高さで確保する。"""
		dc = wx.ClientDC(self.note)
		dc.SetFont(self.note.GetFont())
		width = self._wrapWidth(self.note)
		height = dc.GetCharHeight()
		for text in (inUseNote(), pausedNote()):
			height = max(height, dc.GetMultiLineTextExtent(wrapText(dc, text, width))[1])
		self.note.SetMinSize((-1, height))

	def _restoreGeometry(self):
		s = self.settings
		# 設定ファイルがなければ既定のサイズ（DEFAULT_SETTINGS）で開く
		self.SetSize((max(int(s["width"]), 360), max(int(s["height"]), 220)))
		if s["x"] is not None and s["y"] is not None:
			x, y = int(s["x"]), int(s["y"])
			# モニター構成が変わって画面外になっていたら位置は復元しない
			if wx.Display.GetFromPoint(wx.Point(x + 40, y + 10)) != wx.NOT_FOUND:
				self.SetPosition((x, y))

	def _scheduleSave(self):
		if self.IsIconized() or self.IsMaximized():
			return
		if self._saveTimer:
			self._saveTimer.Stop()
		self._saveTimer = wx.CallLater(500, self.saveGeometry)

	def saveGeometry(self):
		if not self:
			return
		x, y = self.GetPosition()
		w, h = self.GetSize()
		self.settings.update({"x": x, "y": y, "width": w, "height": h})
		saveSettings(self.settings)

	def onSize(self, evt):
		evt.Skip()
		# 幅が変わったら折り返し位置を計算し直す
		wx.CallAfter(self._rewrapAll)
		self._scheduleSave()

	def onMove(self, evt):
		evt.Skip()
		self._scheduleSave()

	# --- フォント ---------------------------------------------------------

	def applyFont(self):
		face = resolveFontFace()
		info = wx.FontInfo(FONT_SIZE)
		info = info.FaceName(face) if face else info.Family(wx.FONTFAMILY_SWISS)
		font = wx.Font(info)
		for ctrl in [*self.titles, *self.labels.values(), self.note,
				self.monitorCheck, self.topCheck,
				self.toggleButton, self.refreshButton]:
			ctrl.SetFont(font)
		self.labels["mode"].SetFont(font.Bold().Larger())
		for button in (self.toggleButton, self.refreshButton):
			self._fitButton(button)
		self._rewrapAll()

	# --- チェックボックス -------------------------------------------------

	def onMonitorToggle(self, evt):
		enabled = self.monitorCheck.GetValue()
		self.settings["monitoring"] = enabled
		saveSettings(self.settings)
		self.plugin.setMonitoring(enabled)

	def onTopToggle(self, evt):
		onTop = self.topCheck.GetValue()
		self.settings["alwaysOnTop"] = onTop
		saveSettings(self.settings)
		style = self.GetWindowStyleFlag()
		self.SetWindowStyleFlag(style | wx.STAY_ON_TOP if onTop else style & ~wx.STAY_ON_TOP)

	# --- 表示 -------------------------------------------------------------

	def onClose(self, evt):
		# 閉じるボタンでは破棄せず隠す（ショートカットで再表示できる）
		if evt.CanVeto():
			evt.Veto()
			self.Hide()
		else:
			self.Destroy()

	def _wrapWidth(self, ctrl):
		"""ラベルを折り返す幅（パネル幅からラベル列と余白を引いた値）。"""
		width = self.panel.GetClientSize().width - 16
		if ctrl is not self.note:
			cols = self.grid.GetColWidths()
			width -= (cols[0] + self.grid.GetHGap()) if cols else 120
		return max(width, 80)

	def _rewrapAll(self):
		if not self:
			return
		for ctrl, text in self._raw.items():
			ctrl.SetLabel(text)
			ctrl.Wrap(self._wrapWidth(ctrl))
		# 幅が変わると注釈の折り返し行数も変わるので、確保する高さを計算し直す
		self._reserveNoteArea()
		self.panel.Layout()

	def _set(self, ctrl, text):
		"""テキストを設定し、右端で折り返す。変化がなければ何もしない。"""
		if self._raw.get(ctrl) == text:
			return
		self._raw[ctrl] = text
		ctrl.SetLabel(text)
		ctrl.Wrap(self._wrapWidth(ctrl))

	def _setNote(self, text):
		# 注釈の領域は常に確保してあるので、文言を入れ替えるだけ
		self._set(self.note, text)

	def _fitButton(self, button):
		"""ボタンの幅をラベルが収まるまで広げる。高さは文字の高さの2.5倍で固定する。"""
		button.InvalidateBestSize()
		button.SetMinSize(wx.DefaultSize)
		best = button.GetBestSize()
		button.SetMinSize((best.width + 24, int(button.GetCharHeight() * BUTTON_HEIGHT_RATIO)))

	def _setButton(self, button, text):
		if button.GetLabel() != text:
			button.SetLabel(text)
			self._fitButton(button)

	def _updateButtonLabels(self):
		# Translators: Button label shown in two lines. {key} is the actual key, e.g. NonConvert+Space.
		self._setButton(self.toggleButton, _("Toggle mode\n({key})").format(key=keyLabel("Space")))
		# Translators: Button label shown in two lines. {key} is the actual key, e.g. NonConvert+F5.
		self._setButton(self.refreshButton, _("Refresh virtual buffer\n({key})").format(key=keyLabel("F5")))

	def updateView(self, info, usingLast):
		"""状態表示を更新する。"""
		for key in ("mode", "buffer", "object", "app"):
			self._set(self.labels[key], info[key])
		self._set(self.labels["nvdaKey"], " / ".join(getNVDAKeyNames()))
		self._setNote(inUseNote() if usingLast else "")
		self._updateButtonLabels()
		# 折り返しで行数が変わる場合もあるので再配置
		self.panel.Layout()

	def showPaused(self):
		for key in ("mode", "buffer", "object", "app"):
			# Translators: Shown in each row while monitoring is paused.
			self._set(self.labels[key], _("(paused)"))
		self._setNote(pausedNote())
		self.panel.Layout()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# Translators: Category name in the Input Gestures dialog.
	scriptCategory = _("Developer Status Panel")

	def __init__(self):
		super().__init__()
		self._lastExternalFocus = None
		self.settings = loadSettings()
		self.timer = wx.Timer()
		self.timer.Bind(wx.EVT_TIMER, self._onTimer)
		self.panel = StatusPanel(self)
		self.menuItem = gui.mainFrame.sysTrayIcon.toolsMenu.Append(
			# Translators: Item in the NVDA Tools menu.
			wx.ID_ANY, _("&Developer Status Panel")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, lambda e: self.togglePanel(), self.menuItem)
		self.setMonitoring(self.settings["monitoring"])
		# 常時表示：起動時にフォーカスを奪わずに表示
		self.panel.ShowWithoutActivating()

	def terminate(self):
		try:
			self.timer.Stop()
			self.panel.saveGeometry()
			gui.mainFrame.sysTrayIcon.toolsMenu.Remove(self.menuItem)
			self.panel.Destroy()
		except Exception:
			log.debugWarning("devStatusPanel: terminate failed", exc_info=True)
		super().terminate()

	# --- 状態更新 ---------------------------------------------------------

	def _onTimer(self, evt):
		if not self.panel.IsShown():
			return
		try:
			focus = api.getFocusObject()
			usingLast = _isOwnProcess(focus)
			if usingLast:
				focus = self._lastExternalFocus
			else:
				self._lastExternalFocus = focus
			self.panel.updateView(describeState(focus), usingLast)
		except Exception:
			log.debugWarning("devStatusPanel: update failed", exc_info=True)

	def setMonitoring(self, enabled):
		"""監視のオン／オフ。オフの間はタイマーを止めるので負荷はほぼゼロ。"""
		if enabled:
			self.timer.Start(300)
			self._onTimer(None)
		else:
			self.timer.Stop()
			self.panel.showPaused()

	def togglePanel(self):
		if self.panel.IsShown():
			self.panel.Hide()
		else:
			self.panel.ShowWithoutActivating()

	# --- ボタン操作 -------------------------------------------------------

	def runOnTarget(self, action):
		"""直前のアプリにフォーカスを戻してから、NVDA本来のコマンドを実行する。"""
		target = self._lastExternalFocus
		if target is None:
			return
		try:
			hwnd = ctypes.windll.user32.GetAncestor(target.windowHandle, _GA_ROOT)
			ctypes.windll.user32.SetForegroundWindow(hwnd)
		except Exception:
			log.debugWarning("devStatusPanel: restore foreground failed", exc_info=True)
		self._waitThenRun(action, retries=10)

	def _waitThenRun(self, action, retries):
		if _isOwnProcess(api.getFocusObject()):
			if retries > 0:
				core.callLater(100, self._waitThenRun, action, retries - 1)
			return
		action()

	def doToggleMode(self):
		# 無変換+Space と同じ処理（仮想バッファの強制生成も含む）
		globalCommands.commands.script_toggleVirtualBufferPassThrough(None)

	def doRefreshBuffer(self):
		ti = api.getFocusObject().treeInterceptor
		refresh = getattr(ti, "script_refreshBuffer", None)
		if refresh:
			refresh(None)

	# --- ショートカット ---------------------------------------------------

	@script(
		# Translators: Description of the script shown in the Input Gestures dialog.
		description=_("Shows or hides the Developer Status Panel"),
		gesture="kb:NVDA+control+shift+d",
	)
	def script_togglePanel(self, gesture):
		self.togglePanel()
