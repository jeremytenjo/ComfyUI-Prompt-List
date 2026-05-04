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
    assert required["text"][1]["forceInput"] is True
    assert required["divider"][1]["default"] == "**"


def test_split_basic_default_separator():
    node = ComfyUIPromptList()
    positive, negative = node.split("a**b")
    assert positive == ["a", "b"]
    assert negative == ["", ""]


def test_split_preserves_multiline_chunks():
    node = ComfyUIPromptList()
    positive, negative = node.split("first line\nsecond line**third line\nfourth line")
    assert positive == ["first line\nsecond line", "third line\nfourth line"]
    assert negative == ["", ""]


def test_split_normalizes_windows_newlines_and_trims():
    node = ComfyUIPromptList()
    positive, negative = node.split("  one\r\nline  **\r\n\r\n  two\rthree  ")
    assert positive == ["one\nline", "two\nthree"]
    assert negative == ["", ""]


def test_split_extra_chunks_are_kept_as_additional_items():
    node = ComfyUIPromptList()
    positive, negative = node.split("alpha**beta**gamma")
    assert positive == ["alpha", "beta", "gamma"]
    assert negative == ["", "", ""]


def test_split_empty_input_falls_back_to_empty_strings():
    node = ComfyUIPromptList()
    positive, negative = node.split("   \r\n  **   \n")
    assert positive == [""]
    assert negative == [""]


def test_split_supports_custom_divider():
    node = ComfyUIPromptList()
    positive, negative = node.split("a***b***c", divider="***")
    assert positive == ["a", "b", "c"]
    assert negative == ["", "", ""]


def test_split_parses_labeled_positive_negative():
    node = ComfyUIPromptList()
    text = "positive: cat photo\nnegative: blurry, lowres"
    positive, negative = node.split(text)
    assert positive == ["cat photo"]
    assert negative == ["blurry, lowres"]


def test_split_parses_labeled_multiline_sections():
    node = ComfyUIPromptList()
    text = (
        "positive: cinematic portrait\n"
        "red dress\n"
        "negative: lowres\n"
        "bad hands"
    )
    positive, negative = node.split(text)
    assert positive == ["cinematic portrait\nred dress"]
    assert negative == ["lowres\nbad hands"]


def test_split_labeled_blocks_work_across_multiple_items():
    node = ComfyUIPromptList()
    text = (
        "positive: prompt a\nnegative: neg a\n"
        "**\n"
        "positive: prompt b\nnegative: neg b"
    )
    positive, negative = node.split(text)
    assert positive == ["prompt a", "prompt b"]
    assert negative == ["neg a", "neg b"]


def test_split_without_labels_defaults_to_positive_only():
    node = ComfyUIPromptList()
    positive, negative = node.split("plain prompt text")
    assert positive == ["plain prompt text"]
    assert negative == [""]


def test_outputs_are_marked_as_lists():
    assert ComfyUIPromptList.OUTPUT_IS_LIST == (True, True)


def test_node_mappings_export_expected_values():
    assert NODE_CLASS_MAPPINGS["ComfyUI-Prompt-List"] is ComfyUIPromptList
    assert NODE_DISPLAY_NAME_MAPPINGS["ComfyUI-Prompt-List"] == "Prompts"
