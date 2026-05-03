import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from comfyui_prompt_list import (  # noqa: E402
    NODE_CLASS_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS,
    ComfyUIPromptList,
)


def test_input_types_contains_only_text():
    input_types = ComfyUIPromptList.INPUT_TYPES()
    required = input_types["required"]

    assert list(required.keys()) == ["text"]


def test_split_basic_triple_star_separator():
    node = ComfyUIPromptList()
    (result,) = node.split("a***b***c")
    assert result == ["a", "b", "c"]


def test_split_preserves_multiline_chunks():
    node = ComfyUIPromptList()
    (result,) = node.split("first line\nsecond line***third line\nfourth line")
    assert result == ["first line\nsecond line", "third line\nfourth line"]


def test_split_normalizes_windows_newlines_and_trims():
    node = ComfyUIPromptList()
    (result,) = node.split("  one\r\nline  ***\r\n\r\n  two\rthree  ")
    assert result == ["one\nline", "two\nthree"]


def test_split_removes_empty_chunks():
    node = ComfyUIPromptList()
    (result,) = node.split("*** alpha ***   *** beta ***")
    assert result == ["alpha", "beta"]


def test_split_empty_input_falls_back_to_single_empty_string():
    node = ComfyUIPromptList()
    (result,) = node.split("   \r\n  ***   \n")
    assert result == [""]


def test_node_mappings_export_expected_values():
    assert NODE_CLASS_MAPPINGS["ComfyUI-Prompt-List"] is ComfyUIPromptList
    assert NODE_DISPLAY_NAME_MAPPINGS["ComfyUI-Prompt-List"] == "ComfyUI-Prompt-List"
