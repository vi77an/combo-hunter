# 🕸️ Combo Hunter

[English](README_en.md)

Combo Hunter é uma poderosa ferramenta CLI projetada para filtrar e extrair domínios específicos de listas de combos massivas. Seja lidando com 10 milhões de linhas ou mais, esta ferramenta ajuda você a encontrar exatamente o que precisa em segundos! 🔍

## ⚠️ Aviso Legal

**Disclaimer:** Esta ferramenta é estritamente para fins educacionais e testes de segurança autorizados. O uso indevido de combo lists ou acesso não autorizado a contas é ilegal e antiético. O usuário assume total responsabilidade por quaisquer ações tomadas com esta ferramenta.

## ✨ Funcionalidades

- 🚀 Filtragem de domínios ultra-rápida
- 🎨 Interface CLI interativa e colorida
- 📂 Seleção flexível de arquivos `.txt`
- 🔍 Busca inteligente de domínios
- 💾 Exportação automática de resultados
- 🌐 Suporte a URLs com `https://`
- 🔒 Tratamento robusto de erros

## 🛠️ Requisitos

- Python 3.6+
- Nenhuma dependência externa

## 🚀 Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/vi77an/combo-hunter.git
   cd combo-hunter
   ```

2. Verifique se você tem Python 3.6+ instalado:
   ```bash
   python3 --version
   ```

## 💻 Uso

1. Coloque seus arquivos de combo list `.txt` no mesmo diretório do script.

2. Execute a ferramenta:

   ```bash
   python3 combo_hunter.py
   ```

3. Siga os prompts interativos:
   - Selecione seu arquivo de combo list
   - Digite o domínio ou termo para buscar
   - Visualize e exporte resultados automaticamente

### Exemplo de Fluxo de Trabalho

```
✓ arquivo selecionado: combos_netflix.txt

digite o termo para buscar (ex: netflix): gmail
🔍 buscando por 'gmail'...
✓ 250 linha(s) encontrada(s)!
✓ resultados salvos em: resultados/resultado_gmail_20260208_123456.txt
```

## 📦 Estrutura do Projeto

```
combo-hunter/
├── combo_hunter.py    # Script principal
├── README.md          # Documentação
├── README_en.md       # Documentação em Inglês
├── .gitignore         # Arquivo de ignorados do Git
└── resultados/        # Diretório de resultados exportados
```

## 🔍 Capacidades de Busca

- Busca sem distinção entre maiúsculas e minúsculas
- Extração de domínios de diversos formatos de entrada
- Manipula URLs e combo lists em texto simples
- Suporta correspondências parciais e completas de domínios

## 📝 Formato de Entrada

Formatos de combo list suportados:

```
dominio.com:login:senha
https://dominio.com:login:senha
login:senha@dominio.com
```

## 🛡️ Privacidade & Segurança

- Nenhuma dependência externa
- Processamento de arquivos local
- Nenhuma conexão com a internet necessária
- Resultados salvos localmente no diretório `resultados/`

## 🤝 Contribuindo

1. Faça um fork do repositório
2. Crie sua branch de funcionalidade (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona NovaFuncionalidade'`)
4. Envie para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📄 Licença

Distribuído sob a Licença MIT. Veja `LICENSE` para mais informações.

---

**Coded with 🩷 by [@vi77an](https://t.me/vi77an)**
