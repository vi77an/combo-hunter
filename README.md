# 🕸️ combo list hunter

cli tool para caçar domínios específicos em combo lists massivas.
sua db tem 10 milhões de linhas? sem problemas.
filtre, extraia e encontre o que precisa em segundos! 🔥

## ✨ features

- interface colorida e interativa
- seleção de arquivos `.txt` do diretório
- busca inteligente por domínios
- exportação automática dos resultados
- suporte a urls com `https://`

## 🚀 instalação

```bash
git clone https://github.com/vi77an/combo-hunter.git
cd combo-hunter
```

nenhuma dependência externa necessária - apenas python 3.6+

## 💻 uso

1. coloque seus arquivos `.txt` na mesma pasta do script
2. execute o script:

```bash
python combo_hunter.py
```

3. selecione o arquivo desejado
4. digite o termo para buscar (ex: `netflix`, `globo`)
5. os resultados serão salvos em `resultados/`

## 📝 formato esperado

as linhas devem seguir o padrão:
```
dominio.com:login:senha
https://dominio.com:login:senha
```

## 🎨 preview

```
 ██▒   █▓ ██▓ ██▓     ██▓    ▄▄▄       ███▄    █ 
▓██░   █▒▓██▒▓██▒    ▓██▒   ▒████▄     ██ ▀█   █ 
 ▓██  █▒░▒██▒▒██░    ▒██░   ▒██  ▀█▄  ▓██  ▀█ ██▒
  ▒██ █░░░██░▒██░    ▒██░   ░██▄▄▄▄██ ▓██▒  ▐▌██▒
   ▒▀█░  ░██░░██████▒░██████▒▓█   ▓██▒▒██░   ▓██░

          ✧ combo list filter tool ✧ 
              ⸸ bloody coded by vi77an ⸸
    
arquivos disponíveis:

  [1] comboteste.txt (0.00 mb)
  [2] dbteste.txt (0.00 mb)

escolha o número do arquivo: 1
✓ arquivo selecionado: comboteste.txt

digite o termo para buscar (ex: netflix): oie

🔍 buscando por 'oie'...
⚠  nenhum resultado encontrado para 'oie'.
deseja tentar outro termo? (s/n): n

👋 até logo!
```

## 📦 estrutura

```
combo-hunter/
├── combo_hunter.py    # script principal
├── README.md          # documentação
├── .gitignore         # arquivos ignorados
└── resultados/        # outputs (auto-criada)
```

## ⚠️ aviso legal

esta ferramenta é destinada apenas para fins educacionais e testes de segurança autorizados. o uso inadequado é de responsabilidade do usuário.

## 📄 licença

mit license - sinta-se livre para usar e modificar.

---

coded with 🩸 by [vi77an](t.me/vi77an)
