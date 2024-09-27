import time
from datetime import datetime

import schedule

from configs.tools.queue import HTMLSQSListener


# Função a ser executada a cada 2 minutos
def task_every_2_minutes():
    print(f"Tarefa a cada 2 minutos executada em {datetime.now()}")
    HTMLSQSListener().check_messages()


# Função para agendar a tarefa a cada 2 minutos
def schedule_2_min_task():
    schedule.every(10).seconds.do(task_every_2_minutes)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    schedule_2_min_task()
