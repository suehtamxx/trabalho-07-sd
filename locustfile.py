from locust import HttpUser, task, between, events
import random
import string
import gevent

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    def reset_stats_after_warmup():
        gevent.sleep(60) 
        print("\n" + "="*50)
        print("WARM-UP DE 1 MINUTO CONCLUÍDO. ZERANDO ESTATÍSTICAS AUTOMATICAMENTE!")
        print("="*50 + "\n")
        environment.runner.stats.reset_all()

    gevent.spawn(reset_stats_after_warmup)
    
class APIUser(HttpUser):
    # 40% dos acessos
    @task(4)
    def recurso_lento(self):
        self.client.get("/api/recurso-lento")

    # 30% dos acessos
    @task(3)
    def recurso_detalhe(self):
        cliente_id = random.randint(1, 50)
        self.client.get(f"/api/recurso-detalhe/{cliente_id}", name="/api/recurso-detalhe/[id]")

    # 20% dos acessos
    @task(2)
    def status(self):
        self.client.get("/api/status")

    # 10% dos acessos 
    @task(1)
    def criar_recurso(self):
        nome_aleatorio = ''.join(random.choices(string.ascii_letters, k=6))
        self.client.post("/api/recurso", json={"nome": f"Usuario {nome_aleatorio}"})