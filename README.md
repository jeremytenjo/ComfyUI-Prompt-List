# ComfyUI Prompt List

Simple ComfyUI custom node that splits one text input into:
- `positive`
- `negative`

using a configurable divider string (default: `**`).

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
   - `positive`: text before the first divider
   - `negative`: text after the first divider (remaining parts are joined back with the same divider)

Example with default divider:

```text
cinematic portrait ** lowres, blurry
```

Outputs:
- `positive`: `cinematic portrait`
- `negative`: `lowres, blurry`

Example with custom divider `***`:

```text
cinematic portrait *** lowres *** blurry
```

Outputs:
- `positive`: `cinematic portrait`
- `negative`: `lowres***blurry`
