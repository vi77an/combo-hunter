# 🕸️ Combo Hunter

Combo Hunter is a powerful CLI tool designed for efficiently filtering and extracting specific domains from massive combo lists. Whether you're dealing with 10 million lines or more, this tool helps you find exactly what you need in seconds! 🔍

## ⚠️ Legal Warning

**Disclaimer:** This tool is strictly for educational and authorized security testing purposes. Misuse of combo lists or unauthorized access to accounts is illegal and unethical. The user assumes full responsibility for any actions taken with this tool.

## ✨ Features

- 🚀 Lightning-fast domain filtering
- 🎨 Interactive and colorful CLI interface
- 📂 Flexible `.txt` file selection
- 🔍 Intelligent domain search
- 💾 Automatic results export
- 🌐 Supports URLs with `https://`
- 🔒 Robust error handling

## 🛠️ Requirements

- Python 3.6+
- No external dependencies

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/vi77an/combo-hunter.git
   cd combo-hunter
   ```

2. Ensure you have Python 3.6+ installed:
   ```bash
   python3 --version
   ```

## 💻 Usage

1. Place your `.txt` combo list files in the same directory as the script.

2. Run the tool:

   ```bash
   python3 combo_hunter.py
   ```

3. Follow the interactive prompts:
   - Select your combo list file
   - Enter the domain or term to search
   - View and export results automatically

### Example Workflow

```
✓ arquivo selecionado: combos_netflix.txt

digite o termo para buscar (ex: netflix): gmail
🔍 buscando por 'gmail'...
✓ 250 linha(s) encontrada(s)!
✓ resultados salvos em: resultados/resultado_gmail_20260208_123456.txt
```

## 📦 Project Structure

```
combo-hunter/
├── combo_hunter.py    # Main script
├── README.md          # Documentation
├── .gitignore         # Git ignore file
└── resultados/        # Exported results directory
```

## 🔍 Search Capabilities

- Case-insensitive search
- Extracts domains from various input formats
- Handles URLs and plain text combo lists
- Supports partial and full domain matches

## 📝 Input Format

Supported combo list formats:

```
dominio.com:login:senha
https://dominio.com:login:senha
login:senha@dominio.com
```

## 🛡️ Privacy & Security

- No external dependencies
- Local file processing
- No internet connection required
- Results saved locally in `resultados/` directory

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Coded with 🩷 by [@vi77an](https://t.me/vi77an)**
