import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from comfyui_prompt_list import (  # noqa: E402
    NODE_CLASS_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS,
    ComfyUIPromptList,
)


def test_input_types_contains_text_and_divider():
    input_types = ComfyUIPromptList.INPUT_TYPES()
    required = input_types["required"]

    assert list(required.keys()) == ["text", "divider"]
    assert required["divider"][1]["default"] == "**"


def test_split_basic_default_separator():
    node = ComfyUIPromptList()
    positive, negative = node.split("a**b")
    assert positive == "a"
    assert negative == "b"


def test_split_preserves_multiline_chunks():
    node = ComfyUIPromptList()
    positive, negative = node.split("first line\nsecond line**third line\nfourth line")
    assert positive == "first line\nsecond line"
    assert negative == "third line\nfourth line"


def test_split_normalizes_windows_newlines_and_trims():
    node = ComfyUIPromptList()
    positive, negative = node.split("  one\r\nline  **\r\n\r\n  two\rthree  ")
    assert positive == "one\nline"
    assert negative == "two\nthree"


def test_split_extra_chunks_are_kept_in_negative():
    node = ComfyUIPromptList()
    positive, negative = node.split("alpha**beta**gamma")
    assert positive == "alpha"
    assert negative == "beta**gamma"


def test_split_empty_input_falls_back_to_empty_strings():
    node = ComfyUIPromptList()
    positive, negative = node.split("   \r\n  **   \n")
    assert positive == ""
    assert negative == ""


def test_split_supports_custom_divider():
    node = ComfyUIPromptList()
    positive, negative = node.split("a***b***c", divider="***")
    assert positive == "a"
    assert negative == "b***c"


def test_node_mappings_export_expected_values():
    assert NODE_CLASS_MAPPINGS["ComfyUI-Prompt-List"] is ComfyUIPromptList
    assert NODE_DISPLAY_NAME_MAPPINGS["ComfyUI-Prompt-List"] == "PromptList"
