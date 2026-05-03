# ComfyUI Prompt List

Simple ComfyUI custom node that splits text into multiple prompt blocks using a configurable divider (default: `**`).

It outputs prompt lists so downstream nodes run once per block (multi-image generation in one queue run).

## Install

1. Go to your ComfyUI custom nodes folder:
   - `ComfyUI/custom_nodes/`
2. Clone this repo:
   - `git clone https://github.com/your-user/ComfyUI-Prompt-List.git`
3. Restart ComfyUI.

## Usage

1. Add the node: `PromptList` (category: `utils/string`)
2. Set inputs:
   - `text`: your full prompt text
   - `divider`: separator string (default `**`)
3. Connect outputs:
   - `positive` (`STRING` list): one entry per split block
   - `negative` (`STRING` list): parsed per block (or empty when omitted)

Single plain string example:

```text
cinematic portrait of a woman, warm sunlight, high detail
```

Outputs:
- `positive`: `["cinematic portrait of a woman, warm sunlight, high detail"]`
- `negative`: `[""]`

Multiple plain strings example:

```text
plain prompt A
**
plain prompt B
```

Outputs:
- `positive`: `["plain prompt A", "plain prompt B"]`
- `negative`: `["", ""]`

Per-block format:

```text
positive: <prompt>
negative: <prompt>
```

Split multiple blocks using the divider (default `**`):

```text
positive: prompt A
negative: neg A
**
positive: prompt B
negative: neg B
```

Outputs:
- `positive`: `["prompt A", "prompt B"]`
- `negative`: `["neg A", "neg B"]`

If a block does not include `positive:`/`negative:` labels, the full block is treated as positive and negative is empty.

Custom divider example (`***`):

```text
positive: prompt A
negative: neg A
***
positive: prompt B
negative: neg B
```

## Multiple Image Generation

`PromptList` outputs `STRING` lists (`positive` and `negative`) and marks them as list outputs, so ComfyUI iterates downstream nodes once per list item.

That means one queue run can generate multiple images:

1. Put multiple prompt blocks in `text`
2. Separate blocks with the divider (`**` by default)
3. Connect `positive` and `negative` to your `CLIP Text Encode` nodes
4. Queue once

ComfyUI will process each block as its own prompt pair, producing one image result per block (with your normal batch/sampler settings applied per run).
