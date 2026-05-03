from typing import Any, Dict, Tuple


class ComfyUIPromptList:
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "text": (
                    "STRING",
                    {"multiline": True, "dynamicPrompts": True},
                ),
                "divider": (
                    "STRING",
                    {"default": "**"},
                ),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive", "negative")
    FUNCTION = "split"
    CATEGORY = "utils/string"

    def split(self, text: str, divider: str = "**") -> Tuple[str, str]:
        normalized = (text or "").replace("\r\n", "\n").replace("\r", "\n")
        active_divider = divider if divider else "**"
        items = [chunk.strip() for chunk in normalized.split(active_divider)]
        items = [item for item in items if item]

        positive = items[0] if len(items) > 0 else ""
        negative = active_divider.join(items[1:]) if len(items) > 1 else ""

        return (positive, negative)


NODE_CLASS_MAPPINGS = {
    "ComfyUI-Prompt-List": ComfyUIPromptList,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI-Prompt-List": "PromptList",
}
