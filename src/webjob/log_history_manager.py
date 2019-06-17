"""
LogHistoryManager
=====
Prover
    1. Gerenciamento da quantidade de log mantidos no historico
    2. Remoção dos log mais antigos

Como usar
    Adicione este script como um WebJob Triggered no Azure App Service "siga-api" com a seguinte expressão CRON:
        0 0 0 * * *
"""

import os
import sys

sys.path.append(os.getenv("APP_ROOT"))
sys.path.append(os.getenv("APP_SITEPACKAGES"))

days_ago = int(os.getenv("PERIOD_LOG_IN_DAYS"))
log_directory = os.getenv("APP_LOG")

if os.path.exists(log_directory):
    files = os.listdir(log_directory)
    files.sort()

    number_of_files = len(files)

    if number_of_files > days_ago:
        excess = number_of_files - days_ago

        to_remove = files[:excess]

        for file in to_remove:
            os.remove(log_directory + file)

    print(files)
