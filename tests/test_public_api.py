import os
import subprocess
import sys
from pathlib import Path

import pynvl


def test_all_public_names_are_available_at_package_level():
    assert set(pynvl.__all__) <= set(dir(pynvl))


def test_pd_coalesce_is_exported_at_package_level():
    from pynvl import pd_coalesce

    assert pd_coalesce is pynvl.pd_coalesce


def test_core_package_imports_without_pandas():
    src_dir = Path(__file__).parents[1] / "src"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(src_dir)
    command = """
import pynvl

assert pynvl.nvl(None, 5) == 5
for name in (
    "pd_sign",
    "pd_nvl",
    "pd_nvl2",
    "pd_noneif",
    "pd_decode",
    "pd_coalesce",
):
    helper = getattr(pynvl, name)
    assert callable(helper)
    try:
        helper()
    except ImportError as exc:
        assert "pandas is required" in str(exc)
    else:
        raise AssertionError(f"{name} did not raise ImportError")
"""

    subprocess.run(
        [sys.executable, "-S", "-c", command],
        check=True,
        env=env,
        cwd=src_dir.parent,
    )


def test_package_imports_without_optional_document_dependencies():
    src_dir = Path(__file__).parents[1] / "src"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(src_dir)
    command = """
import pynvl

assert pynvl.utl_to_text("plain text") == "plain text"
assert "utl_to_text" in pynvl.__all__
"""

    subprocess.run(
        [sys.executable, "-S", "-c", command],
        check=True,
        env=env,
        cwd=src_dir.parent,
    )
