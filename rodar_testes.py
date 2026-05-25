import subprocess
import time
import os

# Já cria a pasta "results" exigida no trabalho
os.makedirs("results", exist_ok=True)

print("Iniciando automação das 5 rodadas do Locust...")
print("Cada rodada dura 5 minutos (1m warm-up descartado + 4m reais).")

# Loop para rodar 5 vezes
for i in range(1, 6):
    print(f"\n--- Iniciando Rodada {i} de 5 ---")
    
    # Montando o comando de terminal do Locust
    # --headless: Não abre o navegador
    # -u 50: 50 usuários
    # -r 10: Adiciona 10 usuários por segundo
    # -t 5m: Tempo total cravado de 5 minutos
    # --host http://localhost:8000: URL da API que estamos testando
    # --csv: Nome base para os arquivos que serão salvos
    comando = [
        "locust", 
        "-f", "locustfile.py", 
        "--headless", 
        "-u", "50", 
        "-r", "10", 
        "-t", "5m",
        "--host", "http://localhost:8000",
        "--csv", f"results/otimizado_run_{i}" 
    ]
    
    # Executa o comando e trava a tela esperando terminar
    subprocess.run(comando)
    
    print(f"Rodada {i} finalizada! CSVs salvos na pasta 'results/'.")
    
    if i < 5:
        print("Aguardando 10 segundos para o sistema respirar antes da próxima rodada...")
        time.sleep(10)

print("\nTODAS AS 5 RODADAS FORAM CONCLUÍDAS COM SUCESSO!")