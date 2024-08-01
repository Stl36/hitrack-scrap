import time

from db_service import TriggerManager
from parser import parser as scrap

while True:
    triggers = scrap.run()
    trigger_manager = TriggerManager(triggers)
    time.sleep(60)
