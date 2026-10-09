"""Build script for the Developer Status Panel NVDA add-on.

Compiles every addon/locale/*/LC_MESSAGES/*.po into .mo, then packages the
contents of addon/ into dist/<name>-<version>.nvda-addon.

Uses only the Python standard library, so GNU gettext (msgfmt) is not required.

Usage:
	python build.py
"""

import argparse
import ast
import configparser
import struct
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ADDON_DIR = ROOT / "addon"
DIST_DIR = ROOT / "dist"
# Directories and file suffixes that are never packaged.
EXCLUDED_DIRS = {"__pycache__"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def read_manifest():
	"""Return (name, version) from addon/manifest.ini."""
	text = (ADDON_DIR / "manifest.ini").read_text(encoding="utf-8")
	parser = configparser.ConfigParser(interpolation=None)
	# manifest.ini has no section header.
	parser.read_string("[manifest]\n" + text)
	section = parser["manifest"]
	return section["name"].strip().strip('"'), section["version"].strip().strip('"')


def unquote(line, path, lineno):
	"""Decode a quoted PO string such as "Hello\\n"."""
	if not (len(line) >= 2 and line.startswith('"') and line.endswith('"')):
		raise SyntaxError(f"{path}:{lineno}: expected a quoted string")
	return ast.literal_eval(line)


def parse_po(path):
	"""Parse a .po file into {msgid: msgstr} (keys and values as str).

	Fuzzy and untranslated entries are skipped, as msgfmt does by default.
	msgctxt and plural forms are encoded the same way as GNU msgfmt.
	"""
	messages = {}
	entry = {}
	fuzzy = False
	key = None

	def flush():
		nonlocal entry, fuzzy
		if "msgid" in entry:
			msgid = entry["msgid"]
			if "msgid_plural" in entry:
				msgid += "\0" + entry["msgid_plural"]
				count = len([k for k in entry if k.startswith("msgstr[")])
				msgstr = "\0".join(entry[f"msgstr[{i}]"] for i in range(count))
			else:
				msgstr = entry.get("msgstr", "")
			if "msgctxt" in entry:
				msgid = entry["msgctxt"] + "\x04" + msgid
			# The header (empty msgid) is always kept.
			if msgid == "" or (msgstr.replace("\0", "") and not fuzzy):
				messages[msgid] = msgstr
		entry = {}
		fuzzy = False

	lines = path.read_text(encoding="utf-8").splitlines()
	for lineno, raw in enumerate(lines, 1):
		line = raw.strip()
		if not line:
			continue
		if line.startswith("#"):
			# A comment starts a new entry when the previous one is complete.
			if "msgstr" in entry or any(k.startswith("msgstr[") for k in entry):
				flush()
			if line.startswith("#,") and "fuzzy" in line:
				fuzzy = True
			continue
		if line.startswith('"'):
			if key is None:
				raise SyntaxError(f"{path}:{lineno}: string without a keyword")
			entry[key] += unquote(line, path, lineno)
			continue
		keyword, _, rest = line.partition(" ")
		if keyword in ("msgctxt", "msgid") and (
			"msgstr" in entry or any(k.startswith("msgstr[") for k in entry)
		):
			flush()
		if keyword not in ("msgctxt", "msgid", "msgid_plural", "msgstr") and not (
			keyword.startswith("msgstr[") and keyword.endswith("]")
		):
			raise SyntaxError(f"{path}:{lineno}: unknown keyword {keyword!r}")
		key = keyword
		entry[key] = unquote(rest.strip(), path, lineno)
	flush()
	return messages


def write_mo(messages, path):
	"""Write messages to a GNU .mo file (little endian, no hash table)."""
	ids = sorted(messages)
	encoded_ids = [m.encode("utf-8") for m in ids]
	encoded_strs = [messages[m].encode("utf-8") for m in ids]
	count = len(ids)
	header_size = 7 * 4
	ids_table = header_size
	strs_table = ids_table + count * 8
	data_start = strs_table + count * 8

	offsets = []
	data = b""
	for blob in encoded_ids + encoded_strs:
		offsets.append((len(blob), data_start + len(data)))
		data += blob + b"\0"

	output = struct.pack(
		"<7I",
		0x950412DE,  # magic
		0,  # revision
		count,
		ids_table,
		strs_table,
		0,  # hash table size
		data_start,  # hash table offset (unused)
	)
	for length, offset in offsets:
		output += struct.pack("<2I", length, offset)
	output += data
	path.write_bytes(output)


def compile_translations():
	"""Compile every .po under addon/locale into a .mo next to it."""
	po_files = sorted((ADDON_DIR / "locale").glob("*/LC_MESSAGES/*.po"))
	for po in po_files:
		mo = po.with_suffix(".mo")
		messages = parse_po(po)
		write_mo(messages, mo)
		# The header entry is not a translation.
		translated = len([m for m in messages if m])
		print(f"Compiled {po.relative_to(ROOT).as_posix()} ({translated} messages)")
	return po_files


def is_excluded(path):
	relative = path.relative_to(ADDON_DIR)
	if any(part in EXCLUDED_DIRS for part in relative.parts):
		return True
	return path.suffix in EXCLUDED_SUFFIXES


def package(name, version):
	"""Zip the contents of addon/ (not the folder itself) into dist/."""
	DIST_DIR.mkdir(exist_ok=True)
	target = DIST_DIR / f"{name}-{version}.nvda-addon"
	files = sorted(
		p for p in ADDON_DIR.rglob("*") if p.is_file() and not is_excluded(p)
	)
	with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
		for file in files:
			archive.write(file, file.relative_to(ADDON_DIR).as_posix())
	print(f"Created {target.relative_to(ROOT).as_posix()} ({len(files)} files)")
	return target


def main():
	parser = argparse.ArgumentParser(description="Build the NVDA add-on package.")
	parser.add_argument(
		"--list",
		action="store_true",
		help="list the contents of the package after building",
	)
	args = parser.parse_args()

	name, version = read_manifest()
	compile_translations()
	target = package(name, version)
	if args.list:
		with zipfile.ZipFile(target) as archive:
			for info in archive.infolist():
				print(f"  {info.file_size:>8}  {info.filename}")
	return 0


if __name__ == "__main__":
	sys.exit(main())
