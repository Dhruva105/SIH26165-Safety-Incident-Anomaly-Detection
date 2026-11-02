"""Create a ZIP archive of the project, including the local dataset by default."""
from __future__ import annotations
import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".venv", "venv", "__pycache__", ".git", ".pytest_cache", ".ruff_cache", ".ipynb_checkpoints"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def create_archive(output: Path, include_dataset: bool = True) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output = output.resolve()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.resolve() == output:
                continue
            relative = path.relative_to(ROOT)
            if any(part in EXCLUDED_PARTS for part in relative.parts):
                continue
            if path.suffix in EXCLUDED_SUFFIXES:
                continue
            if not include_dataset and relative.as_posix().startswith("data/raw/"):
                continue
            # Never package private analysis artifacts or reviewer sheets.
            if relative.as_posix().startswith("artifacts/private/"):
                continue
            archive.write(path, Path(ROOT.name) / relative)
    return output


def main():
    parser = argparse.ArgumentParser(description="Package the project as a ZIP archive.")
    parser.add_argument("--output", default="../Safety-Incident-Anomaly-Detection.zip")
    parser.add_argument("--without-dataset", action="store_true", help="Do not include data/raw CSV.")
    args = parser.parse_args()
    output = (ROOT / args.output).resolve() if not Path(args.output).is_absolute() else Path(args.output)
    result = create_archive(output, include_dataset=not args.without_dataset)
    print(f"Created: {result}")
    print(f"Size: {result.stat().st_size / (1024**2):.2f} MB")

if __name__ == "__main__":
    main()
