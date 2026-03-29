# Combo Hunter

[English](README_en.md)

Ferramenta CLI para filtrar e extrair dados de listas de combos.

## ⚠️ Aviso Legal

Esta ferramenta e para fins educacionais e testes de seguranca autorizados. O uso indevido de combo lists ou acesso nao autorizado a contas e ilegal. **O usuario assume total responsabilidade**.

## Funcionalidades

- Modo Busca: filtrar dados por termo
- Modo Limpar: formatar arquivos (url:log:pass -> log:pass)
- 4 tipos de busca: dominios, emails completos, usuarios e URLs
- Organização automatica por categoria
- Verificação automatica de Python

## Requisitos

- Python 3.6+
- Nenhuma dependencia externa

## Instalação

```bash
git clone git@github.com:vi77an/combo-hunter.git
cd combo-hunter
python3 --version
```

## Estrutura

```
combos/          # seus arquivos de db.txt aqui
limpar/          # arquivos para formatar aqui
resultados/      # resultados gerados
  ├── dominios/
  ├── emails/
  ├── usuarios/
  ├── urls/
  └── limpar/
```

## Uso

```bash
python3 combo_hunter.py
ou
python combo_hunter.py
ou
py combo_hunter.py
```

Escolha o modo (1 = buscar, 2 = limpar) e siga as instruções.

## Preview

<img width="1026" height="725" alt="preview" src="https://github.com/user-attachments/assets/9d0c9d27-732e-4406-9582-26ec7f99d04c" />

---

## Licença

Distribuído sob a Licença MIT. Veja `LICENSE` para mais informações.

---

**Coded with 🩷 by [@vi77an](https://t.me/vi77an)**
