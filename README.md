# MDConverter - HTML to Markdown Converter

A comprehensive Python ecosystem for converting HTML webpage packages into clean, well-formatted Markdown files. This repository contains both a standalone Python package and an MCP (Model Context Protocol) server implementation.

## 🚀 Features

- **Clean Conversion**: Converts HTML to well-formatted Markdown with proper formatting
- **Image Processing**: Handles and preserves images from webpage packages  
- **Metadata Extraction**: Extracts and preserves article metadata (title, author, description, etc.)
- **Content Cleaning**: Removes ads, scripts, navigation, and other unwanted elements
- **Code Block Preservation**: Maintains syntax highlighting in code blocks
- **Configurable Output**: Extensive configuration options via files or CLI
- **Multiple Interfaces**: CLI, Python API, and MCP server
- **Package Structure**: Proper Python package with modular design

## 📁 Repository Structure

```
MDConverter/
├── README.md                           # This file
├── LICENSE                            # License file
├── 
├── standalone/                        # 📦 STANDALONE PACKAGE
│   ├── setup.py                      # Package setup
│   ├── requirements.txt              # Dependencies
│   ├── html_to_markdown_converter.py # Main converter script
│   ├── src/mdconverter/              # Package source
│   ├── tests/                        # Test suite
│   ├── examples/                     # Usage examples
│   ├── docs/                         # Documentation
│   ├── assets/                       # Processed images and templates
│   └── output/                       # Default output directory
│
└── mcp-server/                       # 🔌 MCP SERVER
    ├── pyproject.toml                # Modern Python project config
    ├── src/                          # MCP server source
    ├── tests/                        # MCP server tests
    ├── converted_articles/           # Example conversions
    ├── test_output/                  # Test outputs
    └── config/                       # MCP configuration files
```

## 🔧 Installation

### Standalone Package

```bash
# Clone the repository
git clone https://github.com/hublun/MDConverter.git
cd MDConverter/standalone

# Install the package
pip install -e .

# Or install dependencies directly
pip install -r requirements.txt
```

### MCP Server

```bash
# Navigate to MCP server directory
cd MDConverter/mcp-server

# Install the MCP server
pip install -e .
```

## 📖 Usage

### Command Line Interface (Standalone)

```bash
# Basic usage
python html_to_markdown_converter.py input.html

# With custom output file
python html_to_markdown_converter.py input.html output.md

# Using the package CLI
mdconverter input.html -o output.md

# With configuration file
mdconverter input.html --config config.json
```

### Python API (Standalone)

```python
from mdconverter import HTMLToMarkdownConverter, Config

# Basic conversion
converter = HTMLToMarkdownConverter("input.html")
success = converter.convert()

# With custom configuration
config = Config({
    'output_dir': 'custom_output',
    'add_metadata': True,
    'log_level': 'DEBUG'
})

converter = HTMLToMarkdownConverter(
    "input.html", 
    output_file="custom.md",
    config=config
)
success = converter.convert()
```

### MCP Server Usage

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "mdconverter": {
      "command": "mdconverter-mcp",
      "args": []
    }
  }
}
```

#### Available MCP Tools

1. **convert_html_to_markdown**: Full HTML to Markdown conversion
2. **validate_html_file**: Validate HTML files before conversion
3. **get_html_metadata**: Extract metadata without full conversion
4. **list_supported_formats**: Show supported formats and features
5. **convert_html_content**: Convert HTML content strings directly

## 🛠️ Configuration

### Standalone Package

Create a `config.json` file:

```json
{
  "output_dir": "output",
  "images_dir": "assets/images",
  "preserve_images": true,
  "clean_html": true,
  "add_metadata": true,
  "log_level": "INFO"
}
```

### MCP Server

The MCP server supports the same configuration options via tool parameters:

```python
{
  "tool": "convert_html_to_markdown",
  "arguments": {
    "html_file_path": "/path/to/webpage.html",
    "output_dir": "converted_articles",
    "preserve_images": true,
    "add_metadata": true
  }
}
```

## 🧪 Testing

### Standalone Package
```bash
cd standalone
python -m pytest tests/
```

### MCP Server
```bash
cd mcp-server
python test_conversion.py
```

## 📚 Documentation

- [Standalone Package Documentation](standalone/docs/)
- [MCP Server Setup Guide](mcp-server/SETUP_GUIDE.md)
- [Configuration Guide](standalone/docs/configuration.md)
- [API Reference](standalone/docs/README_html_converter.md)

## 🔄 Migration Guide

### From Legacy Script

If you were using the old `html_to_markdown_converter.py` script:

```bash
# Old way
python html_to_markdown_converter.py input.html

# New way (still supported)
cd standalone
python html_to_markdown_converter.py input.html

# Or use the package
mdconverter input.html
```

### From Standalone to MCP

The MCP server provides the same functionality with additional features:

```python
# Standalone
converter = HTMLToMarkdownConverter("file.html")
converter.convert()

# MCP
{
  "tool": "convert_html_to_markdown",
  "arguments": {"html_file_path": "file.html"}
}
```

## 🎯 Key Features

### Content Processing
- **Smart Content Extraction**: Identifies and extracts main article content
- **Metadata Preservation**: YAML frontmatter with article information
- **Image Organization**: Copies and organizes image files
- **Code Syntax Preservation**: Maintains syntax highlighting
- **Clean Output**: Removes unwanted elements (ads, navigation, etc.)

### Multiple Interfaces
- **CLI Tool**: Command-line interface for batch processing
- **Python API**: Programmatic access for integration
- **MCP Server**: Model Context Protocol for AI assistant integration

### Advanced Features
- **Configurable Processing**: Extensive customization options
- **Error Handling**: Comprehensive validation and error reporting
- **Multiple Formats**: Support for various HTML structures
- **Template System**: Customizable output templates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Update documentation
6. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Documentation**: Check the `docs/` directories for detailed guides
- **Examples**: See the `examples/` directories for usage examples

---

**Note**: This repository was extracted from the [Leet_Vibe](https://github.com/DRCEDU/Leet_Vibe) repository to create a focused, standalone HTML to Markdown conversion tool.