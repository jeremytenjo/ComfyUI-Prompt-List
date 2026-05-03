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

If a block does not include `positive:`/`negative:` labels, the full block is treated as positive and negative is empty:

```text
plain prompt A
**
plain prompt B
```

Outputs:
- `positive`: `["plain prompt A", "plain prompt B"]`
- `negative`: `["", ""]`

Custom divider example (`***`):

```text
positive: prompt A
negative: neg A
***
positive: prompt B
negative: neg B
```
