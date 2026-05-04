from typing import Dict, Tuple


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
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive", "negative")
    OUTPUT_IS_LIST = (True, True)
    FUNCTION = "split"
    CATEGORY = "utils/string"

    def _parse_block(self, block: str) -> Tuple[str, str]:
        lines = block.split("\n")
        section = None
        positive_lines = []
        negative_lines = []
        has_labels = False

        for raw_line in lines:
            line = raw_line.strip()
            lower = line.lower()

            if lower.startswith("positive:"):
                has_labels = True
                section = "positive"
                value = line[len("positive:") :].strip()
                if value:
                    positive_lines.append(value)
                continue

            if lower.startswith("negative:"):
                has_labels = True
                section = "negative"
                value = line[len("negative:") :].strip()
                if value:
                    negative_lines.append(value)
                continue

            if section == "positive":
                if raw_line.strip():
                    positive_lines.append(raw_line.strip())
                continue

            if section == "negative":
                if raw_line.strip():
                    negative_lines.append(raw_line.strip())
                continue

        if has_labels:
            return ("\n".join(positive_lines).strip(), "\n".join(negative_lines).strip())

        return (block.strip(), "")

    def split(self, text: str, divider: str = "**") -> Tuple[list[str], list[str]]:
        normalized = (text or "").replace("\r\n", "\n").replace("\r", "\n")
        active_divider = divider if divider else "**"
        items = [chunk.strip() for chunk in normalized.split(active_divider)]
        items = [item for item in items if item]

        if not items:
            return ([""], [""])

        parsed = [self._parse_block(item) for item in items]
        positive = [pair[0] for pair in parsed]
        negative = [pair[1] for pair in parsed]

        return (positive, negative)


NODE_CLASS_MAPPINGS = {
    "ComfyUI-Prompt-List": ComfyUIPromptList,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI-Prompt-List": "Prompts",
}
