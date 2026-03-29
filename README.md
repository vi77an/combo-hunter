<div align="center">

```
⠀⠀⠀⠀⠀⠀⠀⠠⡧⠀⠀⠄⠀⣆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⡄⠀⠀⠀⢺⠂⠀⠀⠀⢀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣧
⠤⣤⣤⣤⣤⣤⣤⣤⣤⣿⣿⠇⠀⢿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⠶⠶⠶
⠀⠀⠘⢿⣿⣿⣟⠛⠛⠛⠛
⠀⠀⠁⠀⠈⠛⣿⣿⣦     ✧ combo hunter | a filter tool ✧
⠀⠀⠀⠀⠀⠀⠀⢹⣿⡿            coded by t.me/vi77an
```

**combo hunter** · ferramenta de filtragem e limpeza de combo lists

![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-lightgrey?style=flat-square)

</div>

---

## sobre

**combo hunter** é um script Python de linha de comando para filtrar e formatar grandes arquivos de combo lists (`.txt`). Suporta busca por domínio, e-mail, usuário ou URL, com barra de progresso em tempo real e processamento paralelo automático para arquivos grandes.

---

## estrutura de pastas

```
projeto/
├── combo_hunter.py       ← script principal
├── combos/               ← coloque aqui seus arquivos .txt para busca
├── limpar/               ← coloque aqui arquivos .txt para formatação
└── resultados/
    ├── dominios/         ← resultados de buscas por domínio
    ├── emails/           ← resultados de buscas por e-mail
    ├── usuarios/         ← resultados de buscas por usuário
    ├── urls/             ← resultados de buscas por URL
    └── limpos/           ← arquivos formatados pelo modo limpar
```

> As pastas são criadas automaticamente ao iniciar o script.

---

## requisitos

- Python 3.8 ou superior
- sem dependências externas — apenas biblioteca padrão

```bash
python --version   # deve retornar 3.8+
```

---

## uso

```bash
python combo_hunter.py
```

O script abre um menu interativo com dois modos:

### modo 1 — buscar

Filtra linhas de um arquivo `.txt` por um termo de busca. Quatro tipos disponíveis:

| tipo | descrição | exemplo de match |
|------|-----------|-----------------|
| **domínio** | campo de domínio/site antes do login | `netflix.com:user:pass` |
| **e-mail** | endereço de e-mail completo na linha | `user@gmail.com:pass` |
| **usuário** | campo de login/usuário | `joao123:senha` |
| **url** | qualquer ocorrência do termo na linha | `https://netflix.com/...` |

Os resultados são salvos em `resultados/<tipo>/<termo>@<quantidade>_<data>.csv`.

### modo 2 — limpar

Reformata arquivos no padrão `url:login:senha`. Três opções de saída:

| opção | entrada | saída |
|-------|---------|-------|
| `1` | `https://site.com:user:pass` | `user:pass` |
| `2` | qualquer | mantém linhas com URL, preserva demais |
| `3` | qualquer | mantém original sem alteração |

---

## formatos suportados

O script reconhece automaticamente os seguintes formatos de linha:

```
https://site.com:login:senha      ← url:login:senha
http://site.com:login:senha       ← url:login:senha (http)
login:senha                       ← log:pass
login@dominio.com:senha           ← email:pass
```

---

## performance

O script adapta a estratégia de busca ao tamanho do arquivo:

- **arquivos pequenos** (< 200.000 linhas): busca linear com barra de progresso
- **arquivos grandes** (≥ 200.000 linhas): busca paralela usando todos os núcleos disponíveis (`multiprocessing.Pool`)

Em ambos os casos a barra de progresso é exibida em tempo real com contagem de encontrados, percentual e tempo decorrido.

---

## saída

Os arquivos de resultado são salvos em formato `.csv` com o seguinte padrão de nome:

```
<termo>@<quantidade>_<YYYYMMDD_HHMMSS>.csv
```

Exemplo: `netflix@1523_20240315_142301.csv`

A primeira linha do arquivo contém um comentário de créditos. As demais contêm as linhas encontradas, uma por linha.

---

## créditos

desenvolvido com 🩷 por [vilanele](https://t.me/vi77an)
