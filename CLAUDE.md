# 2D Game Programming (2026-2)

Course project for "2D Game Programming". Python + pico2d, edited in VSCode with
Claude Code as the coding agent (the course slides suggest Opencode; Claude Code
is the approved alternative listed on the same slide).

## Environment

- Python: 3.14.7 (Windows per-user install; pick it via the VSCode interpreter selector)
- Library: `pico2d` 1.5.1 (pulls in PySDL2 + PySDL2-DLL, no manual SDL install needed)
- Editor: VSCode 1.135 with `ms-python.python` and `anthropic.claude-code`

## Layout

```
main.py             sample game: sprite animation, keyboard input, jump physics
tools/make_assets.py generates res/*.png using only the standard library
tools/smoke_test.py  non-interactive environment check, closes by itself
res/                generated PNG assets (safe to delete and regenerate)
.vscode/            interpreter, launch configs, tasks, extension recommendations
```

## Commands

```
python main.py               run the game
python tools/smoke_test.py   verify the environment without pressing any key
python tools/make_assets.py  regenerate res/*.png
```

## House rules (from the course slides, LEC00 p.4)

- No Korean characters in path names, file names, or source file names.
- No spaces in file or folder names.
- ASCII-only identifiers and file names; UTF-8 for file contents.

## pico2d notes for the agent

- The canvas origin is bottom-left; PNG rows run top-down, so sprite sheet rows
  are addressed with `bottom=0` for a single-row sheet.
- `clip_draw(left, bottom, w, h, x, y)` draws one frame; `clip_composite_draw`
  adds rotation and `'h'` / `'v'` flipping.
- Always drive movement with a delta time from `get_time()`, never per-frame
  constants, so behaviour does not change with the frame rate.
- `open_canvas()` must be called before any `load_image` / `load_font`.
