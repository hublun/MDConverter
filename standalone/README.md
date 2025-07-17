# MDConverter Standalone Package

This directory contains the standalone Python package for converting HTML webpage packages to Markdown.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the converter
python html_to_markdown_converter.py input.html

# Or install as package
pip install -e .
mdconverter input.html
```

## Contents

- `html_to_markdown_converter.py` - Main converter script
- `setup.py` - Package setup
- `requirements.txt` - Dependencies
- `src/mdconverter/` - Package source code
- `tests/` - Test suite
- `examples/` - Usage examples
- `docs/` - Documentation
- `assets/` - Images and templates
- `output/` - Default output directory