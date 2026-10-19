from pathlib import Path


def test_project_structure_exists():
    root = Path(__file__).resolve().parents[1]

    assert (root / "src" / "trace_agent").is_dir()
    assert (root / "README.md").is_file()