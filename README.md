
<div style="text-align: center;">
  <img src="assets/port-scanner.png" alt="Logo" width="1200"/>
</div>


# 🔍 Port Scanner

Um simples **scanner de portas** desenvolvido em Python, útil para aprender sobre segurança de redes e como identificar portas abertas em um host.


## 🚀 Funcionalidades
- Escaneia portas de um intervalo definido (por padrão: 1–1024).  
- Permite definir alvo (IP ou domínio).  
- Salva resultados em um arquivo `.csv`.  
- Exibe as portas abertas no console em tempo real.  


## 📂 Estrutura do Projeto

PortScanner/
├── scanner.py
├── requirements.txt
├── results/
│   └── scan_results.csv
└── README.md

## ▶️ Como usar 
1. Clone este repositório:
  

2. Execute no terminal: 
 python scanner.py -t 127.0.0.1 -s 1 -e 1024 -o results.csv

 Parâmetros:

-t → Target (alvo, IP ou domínio)

-s → Porta inicial

-e → Porta final

-o → Arquivo de saída .csv

## 📊 Exemplo de saída
- No console:

[+] Escaneando host: scanme.nmap.org

[+] [OPEN] Porta 22 (SSH)

[+] [OPEN] Porta 80 (HTTP)

- No arquivo example_results.cvs

Porta,Status
22,OPEN
80,OPEN


## ⚙️ Pré-requisitos  
- Python 3.8 ou superior  
- Dependências listadas no `requirements.txt`  

Instalar dependências:

```bash
pip install -r requirements.txt
```






