#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import multiprocessing as mp
from datetime import datetime
from pathlib import Path
from functools import partial

# Catppuccin Mocha Colors
MAUVE = "\033[38;5;183m"  # #cba6f7
PEACH = "\033[38;5;223m"  # #fab387
YELLOW = "\033[38;5;228m"  # #f9e2af
GREEN = "\033[38;5;166m"  # #a6e3a1
BLUE = "\033[38;5;153m"  # #89b4fa
RED = "\033[38;5;211m"  # #f38ba8
SKY = "\033[38;5;117m"  # #89dceb
TEAL = "\033[38;5;72m"  # #94e2d5
RESET = "\033[0m"
BOLD = "\033[1m"
CLEAR_LINE = "\033[2K\r"

# Limiar para ativar multiprocessing (em linhas)
# Abaixo disso, busca linear é mais rápida que o overhead do Pool
LIMIAR_MULTIPROCESSING = 200_000

NUM_PROCESSOS = mp.cpu_count()

# Regex para captura de e-mails
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


class Progresso:
    def __init__(self, total):
        self.total = total
        self.processadas = 0
        self.encontradas = 0
        self.inicio = None
        self.rodando = False

    def iniciar(self):
        self.inicio = time.time()
        self.rodando = True
        self.processadas = 0
        self.encontradas = 0

    def atualizar(self, encontrada=False):
        self.processadas += 1
        if encontrada:
            self.encontradas += 1

    def formatar_tempo(self, segundos):
        if segundos < 60:
            return f"{int(segundos)}s"
        elif segundos < 3600:
            return f"{int(segundos // 60)}m {int(segundos % 60)}s"
        else:
            return f"{int(segundos // 3600)}h {int((segundos % 3600) // 60)}m"

    def exibir(self):
        if not self.rodando or not self.inicio:
            return
        elapsed = time.time() - self.inicio
        rate = self.processadas / elapsed if elapsed > 0 else 0
        eta = (self.total - self.processadas) / rate if rate > 0 else 0

        pct = (self.processadas / self.total * 100) if self.total > 0 else 0
        bar_len = 20
        filled = int(bar_len * self.processadas / self.total) if self.total > 0 else 0
        bar = GREEN + "=" * filled + YELLOW + "-" * (bar_len - filled) + RESET

        msg = (
            f"{CLEAR_LINE}{MAUVE}processando...{RESET} {bar} {pct:.1f}% | "
            f"{GREEN}{self.encontradas}{RESET} encontrados | "
            f"{self.processadas}/{self.total} linhas | "
            f"{self.formatar_tempo(elapsed)}"
        )
        sys.stdout.write(msg)
        sys.stdout.flush()


# ─── Funções de chunk para multiprocessing ────────────────────────────────────
# Precisam ser top-level para o pickle do mp.Pool funcionar corretamente.

def _buscar_dominio_chunk(args):
    """Busca termo no campo de domínio (primeiro campo antes de :login:senha)."""
    linhas, termo = args
    termo = termo.lower()
    resultados = []
    for linha in linhas:
        try:
            linha_strip = linha.strip()
            # Detecta se a linha tem URL (http/https) para extrair domínio corretamente
            if "http://" in linha_strip or "https://" in linha_strip:
                # formato: https://site.com:login:senha → domínio = site.com
                sem_proto = linha_strip.replace("https://", "").replace("http://", "")
                dominio = sem_proto.split(":")[0]
            else:
                # formato: login:senha → pega o campo antes do primeiro :
                dominio = linha_strip.split(":")[0]
            if termo in dominio.lower():
                resultados.append(linha_strip)
        except Exception:
            pass
    return resultados


def _buscar_email_chunk(args):
    """Busca termo dentro de endereços de e-mail na linha."""
    linhas, termo = args
    termo = termo.lower()
    resultados = []
    for linha in linhas:
        try:
            match = EMAIL_PATTERN.search(linha)
            if match and termo in match.group(0).lower():
                resultados.append(linha.strip())
        except Exception:
            pass
    return resultados


def _buscar_usuario_chunk(args):
    """
    Busca termo no campo de usuário/login.
    Pula o campo de URL quando o formato for url:login:senha.
    """
    linhas, termo = args
    termo = termo.lower()
    resultados = []
    for linha in linhas:
        try:
            linha_strip = linha.strip()
            if "http://" in linha_strip or "https://" in linha_strip:
                # formato: https://site.com:login:senha → usuario = partes[1] após remover proto
                sem_proto = linha_strip.replace("https://", "").replace("http://", "")
                partes = sem_proto.split(":")
                usuario = partes[1] if len(partes) >= 2 else ""
            else:
                # formato: login:senha
                partes = linha_strip.split(":")
                usuario = partes[0] if partes else ""
            if termo in usuario.lower():
                resultados.append(linha_strip)
        except Exception:
            pass
    return resultados


def _buscar_url_chunk(args):
    """Busca termo em qualquer posição da linha (busca genérica por URL)."""
    linhas, termo = args
    termo = termo.lower()
    resultados = []
    for linha in linhas:
        try:
            if termo in linha.strip().lower():
                resultados.append(linha.strip())
        except Exception:
            pass
    return resultados


# ─── Classe principal ─────────────────────────────────────────────────────────

class ComboHunter:
    def __init__(self):
        self.base_dir = Path("resultados")
        self.pastas = {
            "dominios": self.base_dir / "dominios",
            "emails": self.base_dir / "emails",
            "usuarios": self.base_dir / "usuarios",
            "urls": self.base_dir / "urls",
            "limpos": self.base_dir / "limpos",
        }
        self.limpar_dir = Path("limpar")
        self.limpar_dir.mkdir(exist_ok=True)
        for pasta in self.pastas.values():
            pasta.mkdir(parents=True, exist_ok=True)

    def limpar_tela(self):
        os.system("cls" if os.name == "nt" else "clear")

    def exibir_banner(self):
        banner = f"""{RED}{BOLD}
⠀⠀⠀⠀⠀⠀⠀⠠⡧⠀⠀⠄⠀⣆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⡄⠀⠀⠀⢺⠂⠀⠀⠀⢀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣧
⠀⠐⠗⠀⠀⠀⠀⠁⠀⠀⣼⣿⡏⣿⣷⡀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠐⠺⠂⠀⠀⠀⠀⠀⠀⠄
⠤⣤⣤⣤⣤⣤⣤⣤⣤⣿⣿⠇⠀⢿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒
⠀⠀⠘⢿⣿⣿⣟⠛⠛⠛⠛⠀⠀⠀⠛⠛⠛⠛⠋⠉⠉⠉
⠀⠀⠁⠀⠈⠛⣿⣿⣦  {RESET}✧ combo hunter | a filter tool ✧{RED}{BOLD}
⠀⠀⠀⠀⠀⠀⠀⢹⣿⡿       {RESET}coded by t.me/vi77an{RED}{BOLD}
⠀⠀⠀⠠⡧⠀⠀⣾⣿⠁⢀⣤⣾⣦⡀
⠀⠠⠀⠀⠀⠀⣸⣿⢇⣶⣿⠟⠙⠻⣿⣄
⠀⠀⠀⠀⠀⢠⣿⣿⠿⠋⠁⠀⠀⠀⠀⠉⠳⡄
⠀⠀⠀⠀⠀⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈
    {RESET}"""
        print(banner)

    def ate_logo(self):
        art = f"""
⠀⠀⠀⠀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡼⠙⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠃⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢰⠃⠀⠘⣿⡄⠀⠀⠀⠀⠀⠀⢀⣿⡇⠀⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡎⠀⠀⠀⢹⣿⣆⠀⠀⠀⠀⠀⣼⣿⠁⠀⠀⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡇⠀⠀⢀⠞⢻⣿⡆⠀⠀⠀⢰⣿⣿⡀⠀⠀⢹⡄⠀⠀⠀⠀{RED}⢀⣤⣤⡄⠀⣀⣤⣤⣀{RESET}
⠀⠀⠀⠀⠀⠀⡇⠀⢰⠋⠀⠈⣿⣿⡄⠀⠀⣾⣿⡇⠹⡄⠀⢨⡇⠀⠀⠀{RED}⢸⣿⣿⣿⣿⣾⣿⣿⣿⣿⡇{RESET}
⠀⠀⠀⠀⠀⠀⡇⢀⡏⠀⢀⣴⣿⣿⣿⣿⣾⣿⣿⣧⡀⢳⠀⢸⡁⠀⠀⠀{RED}⠻⣿⣿⣿⣿⣿⣿⣿⣿⠟{RESET}
⠀⠀⠀⠀⠀⠀⢣⠸⣅⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⡀⣸⠀⠀⠀⠀⠀⠀{RED}⠙⠻⣿⣿⡿⠋{RESET}
⠀⠀⠀⠀⠀⠀⠘⣦⣿⣿⡿⠛⠻⢿⣿⣿⣿⣿⡟⠉⠙⢿⣿⣇⠀⠀⠀⣀⣠⡄⠀⠀⠀{RED}⠉{RESET}
⠀⠀⠀⠀⠀⠀⠀⣿⣿⡿⠀⠀⣿⡟⣿⣿⣿⣿⢸⣷⠀⠈⣿⣿⣤⠶⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠚⠉⠉⠉⠙⠒⠲⣿⣿⣷⠀⠀⠙⢡⣿⣿⣽⣿⣌⠁⠀⣰⣿⣿⣀⣀⣀⠀⠀{BOLD}..até logo..{RESET}
⠀⠀⠀⠀⠀⢀⣠⠽⢿⣿⣿⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠉⠑⠒⠠⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣀⠴⠚⠉⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⡍⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            """
        return art + RESET

    def listar_arquivos_txt(self):
        combos_dir = Path("combos")
        if not combos_dir.exists():
            return []
        return [str(f) for f in combos_dir.glob("*.txt")]

    def selecionar_arquivo(self):
        arquivos = self.listar_arquivos_txt()

        if not arquivos:
            print(f"{RED}✗ adicione suas DBs na pasta 'combos' e retorne.\n{RESET}")
            return None

        print(f"arquivos disponíveis:{RESET}\n")
        for i, arquivo in enumerate(arquivos, 1):
            tamanho = os.path.getsize(arquivo) / (1024 * 1024)
            print(f"  {RED}[{i}]{RESET} {arquivo} {MAUVE}({tamanho:.2f} mb){RESET}")

        while True:
            try:
                print(f"\nescolha o número do arquivo:{RESET} ", end="")
                escolha = input().strip()

                if not escolha.isdigit():
                    print(f"{RED}✗ por favor, digite um número válido.{RESET}")
                    continue

                indice = int(escolha) - 1

                if 0 <= indice < len(arquivos):
                    arquivo_selecionado = arquivos[indice]
                    print(f"✓ arquivo selecionado: {GREEN}{BOLD}{arquivo_selecionado}{RESET}")
                    return arquivo_selecionado
                else:
                    print(f"{RED}✗ número fora do intervalo. escolha entre 1 e {len(arquivos)}.{RESET}")

            except KeyboardInterrupt:
                print(f"\n{RED}✗ operação cancelada pelo usuário.{RESET}")
                return None

    def extrair_dominio(self, linha):
        try:
            linha = linha.strip()
            if "http://" in linha or "https://" in linha:
                sem_proto = linha.replace("https://", "").replace("http://", "")
                return sem_proto.split(":")[0].lower()
            return linha.split(":")[0].lower()
        except Exception:
            return linha.lower()

    def extrair_usuario(self, linha):
        try:
            linha = linha.strip()
            if "http://" in linha or "https://" in linha:
                sem_proto = linha.replace("https://", "").replace("http://", "")
                partes = sem_proto.split(":")
                return partes[1].lower() if len(partes) >= 2 else linha.lower()
            partes = linha.split(":")
            return partes[0].lower() if partes else linha.lower()
        except Exception:
            return linha.lower()

    def extrair_email_completo(self, linha):
        try:
            linha = linha.strip()
            match = EMAIL_PATTERN.search(linha)
            if match:
                return match.group(0).lower()
            return None
        except Exception:
            return None

    def _contar_linhas(self, arquivo):
        """Conta linhas sem carregar tudo na memória."""
        count = 0
        with open(arquivo, "r", encoding="utf-8", errors="ignore") as f:
            for _ in f:
                count += 1
        return count

    def buscar_paralelo(self, arquivo, termo_busca, tipo_busca):
        """
        Busca paralela com multiprocessing para arquivos grandes.
        Para arquivos pequenos usa busca linear (evita overhead do Pool).
        Exibe barra de progresso durante a busca.
        """
        # Seleciona função de busca correta usando partial (evita lambda + closure)
        func_map = {
            "dominios": _buscar_dominio_chunk,
            "emails": _buscar_email_chunk,
            "usuarios": _buscar_usuario_chunk,
            "urls": _buscar_url_chunk,
        }
        func = func_map.get(tipo_busca, _buscar_url_chunk)

        try:
            print(f"{MAUVE}lendo arquivo...{RESET}", end="\r")
            sys.stdout.flush()

            with open(arquivo, "r", encoding="utf-8", errors="ignore") as f:
                linhas = f.readlines()

            total = len(linhas)

            if total == 0:
                print(f"{RED}✗ arquivo vazio.{RESET}")
                return []

            # Para arquivos pequenos, não vale o custo do multiprocessing
            if total < LIMIAR_MULTIPROCESSING:
                print(
                    f"{MAUVE}iniciando busca linear ({total:,} linhas)...{RESET}"
                )
                progresso = Progresso(total)
                progresso.iniciar()
                resultados = []
                for linha in linhas:
                    resultado_linha = func(([linha], termo_busca))
                    if resultado_linha:
                        resultados.extend(resultado_linha)
                        progresso.atualizar(True)
                    else:
                        progresso.atualizar()
                    # Atualiza display a cada 1000 linhas para não travar o terminal
                    if progresso.processadas % 1000 == 0:
                        progresso.exibir()
                progresso.exibir()
                sys.stdout.write(CLEAR_LINE)
                sys.stdout.flush()
            else:
                print(
                    f"{MAUVE}iniciando busca paralela com {NUM_PROCESSOS} núcleos "
                    f"({total:,} linhas)...{RESET}"
                )

                chunk_size = max(1, total // NUM_PROCESSOS)
                chunks = [
                    (linhas[i: i + chunk_size], termo_busca)
                    for i in range(0, total, chunk_size)
                ]

                progresso = Progresso(len(chunks))
                progresso.iniciar()

                resultados = []
                with mp.Pool(NUM_PROCESSOS) as pool:
                    for chunk_result in pool.imap_unordered(func, chunks):
                        resultados.extend(chunk_result)
                        progresso.atualizar(bool(chunk_result))
                        progresso.exibir()

                sys.stdout.write(CLEAR_LINE)
                sys.stdout.flush()

            print(
                f"{GREEN}✓ busca concluída!{RESET} "
                f"{GREEN}{BOLD}{len(resultados)}{RESET} resultado(s) encontrado(s) "
                f"em {total:,} linhas."
            )
            return resultados

        except Exception as e:
            print(f"{RED}✗ erro na busca: {e}{RESET}")
            return []

    def buscar_emails(self, arquivo, termo_busca):
        return self.buscar_paralelo(arquivo, termo_busca, "emails")

    def buscar_usuarios(self, arquivo, termo_busca):
        return self.buscar_paralelo(arquivo, termo_busca, "usuarios")

    def buscar_urls(self, arquivo, termo_busca):
        return self.buscar_paralelo(arquivo, termo_busca, "urls")

    def filtrar_linhas(self, arquivo, termo_busca):
        return self.buscar_paralelo(arquivo, termo_busca, "dominios")

    def salvar_resultados(self, resultados, termo_busca, tipo_busca):
        data_atual = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"{termo_busca}@{len(resultados)}_{data_atual}.csv"

        pasta = self.pastas.get(tipo_busca, self.pastas["urls"])
        caminho_completo = pasta / nome_arquivo

        creditos = "来源: t.me/vi77an"

        try:
            with open(caminho_completo, "w", encoding="utf-8") as f:
                f.write(f"# {creditos}\n")
                for linha in resultados:
                    f.write(linha + "\n")

            print(f"\n{GREEN}{BOLD}✓ {len(resultados)} resultado(s) salvo(s) em:{RESET}")
            print(f"  {MAUVE}{BOLD}{caminho_completo}{RESET}\n")
            return True

        except Exception as e:
            print(f"{RED}✗ erro ao salvar arquivo: {e}{RESET}")
            return False

    def perguntar_sim_nao(self, mensagem):
        while True:
            print(f"{mensagem} (s/n):{RESET} ", end="")
            resposta = input().strip().lower()

            if resposta in ["s", "sim", "y", "yes"]:
                return True
            elif resposta in ["n", "nao", "não", "no"]:
                return False
            else:
                print(f"{RED}✗ resposta inválida. digite 's' ou 'n'.{RESET}")

    def selecionar_tipo_busca(self):
        print(f"""
{RESET}tipos de busca disponiveis:
  {RED}[1]{RESET} dominio     - buscar por dominio de email
  {RED}[2]{RESET} email       - buscar por email completo
  {RED}[3]{RESET} usuario     - buscar por usuario
  {RED}[4]{RESET} url         - buscar por palavra em URL
""")

        while True:
            print(f"escolha o tipo de busca:{RESET} ", end="")
            escolha = input().strip()

            if escolha == "1":
                return "dominios"
            elif escolha == "2":
                return "emails"
            elif escolha == "3":
                return "usuarios"
            elif escolha == "4":
                return "urls"
            else:
                print(f"{RED}✗ opção inválida. escolha 1, 2, 3 ou 4.{RESET}")

    def listar_arquivos_limpar(self):
        return [str(f) for f in self.limpar_dir.glob("*.txt")]

    def selecionar_arquivo_limpar(self):
        arquivos = self.listar_arquivos_limpar()

        if not arquivos:
            print(f"{RED}✗ adicione arquivos na pasta 'limpar' e retorne.\n{RESET}")
            return None

        print(f"arquivos disponiveis:{RESET}\n")
        for i, arquivo in enumerate(arquivos, 1):
            nome = Path(arquivo).name
            tamanho = os.path.getsize(arquivo) / (1024 * 1024)
            print(f"  {RED}[{i}]{RESET} {nome} {MAUVE}({tamanho:.2f} mb){RESET}")

        while True:
            try:
                print(f"\nescolha o numero:{RESET} ", end="")
                escolha = input().strip()

                if not escolha.isdigit():
                    print(f"{RED}✗ digite um numero valido.{RESET}")
                    continue

                indice = int(escolha) - 1

                if 0 <= indice < len(arquivos):
                    arquivo_selecionado = arquivos[indice]
                    print(f"✓ arquivo selecionado: {GREEN}{BOLD}{Path(arquivo_selecionado).name}{RESET}")
                    return arquivo_selecionado
                else:
                    print(f"{RED}✗ numero fora do intervalo.{RESET}")

            except KeyboardInterrupt:
                print(f"\n{RED}✗ operacao cancelada.{RESET}")
                return None

    def detectar_formato(self, linha):
        linha = linha.strip()

        if "http://" in linha or "https://" in linha:
            return "url"

        partes = linha.count(":")

        if partes >= 2:
            return "logpass"
        elif partes == 1:
            return "login"
        return "desconhecido"

    def limpar_dados(self, arquivo):
        # FIX: adicionada chave "desconhecido" para evitar KeyError
        formatos_encontrados = {"url": 0, "logpass": 0, "login": 0, "desconhecido": 0}

        try:
            with open(arquivo, "r", encoding="utf-8", errors="ignore") as f:
                linhas = [linha.strip() for linha in f if linha.strip()]

            for linha in linhas:
                formato = self.detectar_formato(linha)
                formatos_encontrados[formato] += 1

            print(f"\n{MAUVE}formatos detectados:{RESET}")
            print(f"  url:log:pass  -> {formatos_encontrados['url']}")
            print(f"  log:pass       -> {formatos_encontrados['logpass']}")
            print(f"  log:           -> {formatos_encontrados['login']}")
            if formatos_encontrados["desconhecido"] > 0:
                print(f"  desconhecido   -> {formatos_encontrados['desconhecido']}")

            print(f"""
{RESET}opcoes de formatacao:
  {RED}[1]{RESET} url:log:pass -> log:pass
  {RED}[2]{RESET} url:log:pass -> url:log:pass (extrair url)
  {RED}[3]{RESET} manter original
""")

            while True:
                print(f"escolha:{RESET} ", end="")
                escolha = input().strip()

                if escolha == "1":
                    return self.formatar_para_logpass(linhas)
                elif escolha == "2":
                    return self.formatar_url_logpass(linhas)
                elif escolha == "3":
                    return linhas
                else:
                    print(f"{RED}✗ opcao invalida.{RESET}")

        except Exception as e:
            print(f"{RED}✗ erro ao limpar dados: {e}{RESET}")
            return []

    def formatar_para_logpass(self, linhas):
        """
        Converte url:login:senha → login:senha.
        FIX: extrai corretamente login:senha (partes[2] + ':' + partes[3]),
        não apenas partes[3] (que seria só a senha).
        """
        resultados = []
        for linha in linhas:
            if "http://" in linha or "https://" in linha:
                # formato esperado: https://site.com:login:senha
                # split(maxsplit=3) → ['https', '//site.com', 'login', 'senha']
                partes = linha.split(":", 3)
                if len(partes) >= 4:
                    # partes[0] = 'https', partes[1] = '//site.com'
                    # partes[2] = login, partes[3] = senha
                    logpass = f"{partes[2]}:{partes[3]}"
                    resultados.append(logpass)
                else:
                    resultados.append(linha)
            else:
                resultados.append(linha)
        return resultados

    def formatar_url_logpass(self, linhas):
        """
        Mantém linhas que já têm URL; linhas sem URL são mantidas como estão
        (não faz sentido inventar uma URL para login:senha).
        """
        resultados = []
        for linha in linhas:
            if "http://" in linha or "https://" in linha:
                resultados.append(linha)
            else:
                # FIX: não prefixar https:// em login:senha — isso geraria
                # 'https://user@email.com:senha', que é inválido semanticamente.
                # Mantém a linha original.
                resultados.append(linha)
        return resultados

    def run(self):
        self.limpar_tela()
        self.exibir_banner()

        try:
            while True:
                print(f"""
{RESET}selecione o modo:
  {MAUVE}[1]{RESET} buscar     - filtrar dados por termo
  {MAUVE}[2]{RESET} limpar     - formatar arquivos (url:log:pass -> log:pass)
""")
                while True:
                    print(f"escolha o modo:{RESET} ", end="")
                    modo = input().strip()

                    if modo == "1":
                        modo_busca = True
                        break
                    elif modo == "2":
                        modo_busca = False
                        break
                    else:
                        print(f"{RED}✗ opcao invalida. escolha 1 ou 2.{RESET}")

                tipo_busca = ""

                if modo_busca:
                    arquivo_atual = self.selecionar_arquivo()
                    if arquivo_atual is None:
                        continue

                    tipo_busca = self.selecionar_tipo_busca()

                    while True:
                        print(
                            f"\ndigite o termo para buscar (ex: netflix):{RESET} ",
                            end="",
                        )
                        termo_busca = input().strip()

                        if not termo_busca:
                            print(f"{RED}✗ termo de busca não pode estar vazio.{RESET}")
                            continue

                        print(f"\n🔍 buscando por '{termo_busca}'...{RESET}")

                        if tipo_busca == "dominios":
                            resultados = self.filtrar_linhas(arquivo_atual, termo_busca)
                        elif tipo_busca == "emails":
                            resultados = self.buscar_emails(arquivo_atual, termo_busca)
                        elif tipo_busca == "usuarios":
                            resultados = self.buscar_usuarios(arquivo_atual, termo_busca)
                        else:
                            resultados = self.buscar_urls(arquivo_atual, termo_busca)

                        if resultados:
                            self.salvar_resultados(resultados, termo_busca, tipo_busca)
                            break
                        else:
                            print(f"{RED}⚠  nenhum resultado encontrado para '{termo_busca}'.{RESET}")
                            if not self.perguntar_sim_nao("deseja tentar outro termo?"):
                                break

                    if self.perguntar_sim_nao("deseja buscar em outro arquivo?"):
                        continue
                    break
                else:
                    while True:
                        arquivo_limpar = self.selecionar_arquivo_limpar()
                        if arquivo_limpar is None:
                            break

                        resultados = self.limpar_dados(arquivo_limpar)
                        termo_busca = Path(arquivo_limpar).stem
                        tipo_busca = "limpos"

                        if resultados:
                            self.salvar_resultados(resultados, termo_busca, tipo_busca)

                        if not self.perguntar_sim_nao("deseja limpar outro arquivo?"):
                            break

                    if self.perguntar_sim_nao("deseja mudar de modo?"):
                        continue
                    break

        except KeyboardInterrupt:
            print(f"\n\n{RED}✗ operação cancelada pelo usuário.{RESET}")
            print(self.ate_logo())

        except Exception as e:
            print(f"\n{RED}✗ erro inesperado: {e}{RESET}\n")


def verificar_python():
    if sys.version_info[0] >= 3 and sys.version_info[1] >= 8:
        return True

    print(f"{RED}✗ Python 3.8+ é necessário.{RESET}\n")
    print("Instale o Python 3 para continuar:\n")
    print(f"  {SKY}Linux (Debian/Ubuntu):{RESET} sudo apt install python3")
    print(f"  {SKY}Linux (RHEL/CentOS):{RESET}   sudo yum install python3")
    print(f"  {SKY}Linux (Arch):{RESET}           sudo pacman -S python")
    print(f"  {SKY}Windows:{RESET}                 python.org ou Microsoft Store")
    print(f"  {SKY}macOS:{RESET}                   brew install python3\n")
    sys.exit(1)


def main():
    verificar_python()
    hunter = ComboHunter()
    hunter.run()


if __name__ == "__main__":
    main()
