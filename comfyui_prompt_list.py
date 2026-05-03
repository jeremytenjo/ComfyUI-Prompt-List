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
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompts",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "split"
    CATEGORY = "utils/string"

    def split(self, text: str) -> Tuple[list[str]]:
        normalized = (text or "").replace("\r\n", "\n").replace("\r", "\n")
        items = [chunk.strip() for chunk in normalized.split("***")]
        items = [item for item in items if item]

        if not items:
            items = [""]

        return (items,)


NODE_CLASS_MAPPINGS = {
    "ComfyUI-Prompt-List": ComfyUIPromptList,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI-Prompt-List": "ComfyUI-Prompt-List",
}
