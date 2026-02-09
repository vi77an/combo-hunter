#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coded by @vi77an -*-

import os
import re
from datetime import datetime
from pathlib import Path

RED = '\033[38;5;204m'
CYAN = '\033[38;5;180m'
YELLOW = '\033[38;5;180m'
GREEN = '\033[38;5;157m'
ORANGE = '\033[38;5;202m'
PURPLE = '\033[38;5;177m'
RESET = '\033[0m'
BOLD = '\033[1m'

class ComboHunter:
    def __init__(self):
        self.resultado_dir = Path('resultados')
        self.resultado_dir.mkdir(exist_ok=True)

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

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
        return [f for f in os.listdir('.') if f.endswith('.txt')]

    def selecionar_arquivo(self):
        arquivos = self.listar_arquivos_txt()
        
        if not arquivos:
            print(f"{RED}✗ adicione suas DBs ao diretório atual e retorne.\n{RESET}")
            return None
        
        print(f"arquivos disponíveis:{RESET}\n")
        for i, arquivo in enumerate(arquivos, 1):
            tamanho = os.path.getsize(arquivo) / (1024 * 1024)
            print(f"  {RED}[{i}]{RESET} {arquivo} {PURPLE}({tamanho:.2f} mb){RESET}")
        
        while True:
            try:
                print(f"\nescolha o número do arquivo:{RESET} ", end='')
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
            
            partes = linha.rsplit(':', 2)
            
            if len(partes) >= 1:
                dominio = partes[0]
                dominio = dominio.replace('https://', '').replace('http://', '')
                return dominio.lower()
            
            return linha.lower()
        
        except Exception:
            return linha.lower()

    def filtrar_linhas(self, arquivo, termo_busca):
        resultados = []
        termo_busca = termo_busca.lower()
        
        try:
            with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                for linha in f:
                    dominio = self.extrair_dominio(linha)
                    if termo_busca in dominio:
                        resultados.append(linha.strip())
            
            return resultados
        
        except FileNotFoundError:
            print(f"{RED}✗ arquivo não encontrado.{RESET}")
            return []
        except Exception as e:
            print(f"{RED}✗ erro ao ler arquivo: {e}{RESET}")
            return []

    def salvar_resultados(self, resultados, termo_busca):
        termo_arquivo = termo_busca.replace('.', '_')
        data_atual = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_arquivo = f"resultado_{termo_arquivo}_{data_atual}.txt"
        caminho_completo = self.resultado_dir / nome_arquivo
        
        try:
            with open(caminho_completo, 'w', encoding='utf-8') as f:
                for linha in resultados:
                    f.write(linha + '\n')
            
            print(f"\n{GREEN}{BOLD}✓ {len(resultados)} resultado(s) salvo(s) em:{RESET}")
            print(f"  {PURPLE}{BOLD}{caminho_completo}{RESET}\n")
            return True
        
        except Exception as e:
            print(f"{RED}✗ erro ao salvar arquivo: {e}{RESET}")
            return False

    def perguntar_sim_nao(self, mensagem):
        while True:
            print(f"{mensagem} (s/n):{RESET} ", end='')
            resposta = input().strip().lower()
            
            if resposta in ['s', 'sim', 'y', 'yes']:
                return True
            elif resposta in ['n', 'nao', 'não', 'no']:
                return False
            else:
                print(f"{RED}✗ resposta inválida. digite 's' ou 'n'.{RESET}")

    def run(self):
        self.limpar_tela()
        self.exibir_banner()
        
        arquivo_atual = None
        
        try:
            while True:
                if arquivo_atual is None:
                    arquivo_atual = self.selecionar_arquivo()
                    if arquivo_atual is None:
                        break
                
                print(f"\ndigite o termo para buscar (ex: netflix):{RESET} ", end='')
                termo_busca = input().strip()
                
                if not termo_busca:
                    print(f"{RED}✗ termo de busca não pode estar vazio.{RESET}")
                    continue
                
                print(f"\n🔍 buscando por '{termo_busca}'...{RESET}")
                resultados = self.filtrar_linhas(arquivo_atual, termo_busca)
                
                if resultados:
                    print(f"{GREEN}{BOLD}✓ {len(resultados)} linha(s) encontrada(s)!{RESET}")
                    self.salvar_resultados(resultados, termo_busca)
                    
                    if not self.perguntar_sim_nao("deseja continuar usando a ferramenta?"):
                        print(self.ate_logo())
                        break
                    
                    if self.perguntar_sim_nao("deseja selecionar um novo arquivo?"):
                        arquivo_atual = None
                        self.limpar_tela()
                        self.exibir_banner()
                
                else:
                    print(f"{RED}⚠  nenhum resultado encontrado para '{termo_busca}'.{RESET}")
                    
                    if not self.perguntar_sim_nao("deseja tentar outro termo?"):
                        print(self.ate_logo())
                        break
        
        except KeyboardInterrupt:
            print(f"\n\n{RED}✗ operação cancelada pelo usuário.{RESET}")
            print(self.ate_logo())
        
        except Exception as e:
            print(f"\n{RED}✗ erro inesperado: {e}{RESET}\n")

def main():
    hunter = ComboHunter()
    hunter.run()

if __name__ == "__main__":
    main()
