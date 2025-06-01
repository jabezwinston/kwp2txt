# KWP to UTF-8 Tamil Text Converter

Converts legacy KWP-encoded Tamil files into modern UTF-8 format, making them compatible with modern systems and editors.

## 💾 Installation

```
pip install kwp2txt
```

## 🔧 Usage

```bash
kwp2txt <input_file> <output_file>
```

```bash
kwp2txt Tamil_doc.kwp Tamil_doc.txt
```

## 🐞 Know issues
- Document with mixture of English and Tamil will not be handled properly. All text will be treated as Tamil.
- Notepad and Wordpad might have some trouble detecting text files as UTF-8. Use Notepad++ or VSCode

## ℹ️ Note
- This tool is extremely experimental.
- Use [KWP Converter](https://kamban.com.au/en/downloads/product/127-kwp-convertor) for better results.