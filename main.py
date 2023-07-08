import sys

from src.projectConf.app import Controller
from src.projectConf.database import DatabaseAccessSingleton

if __name__ == '__main__':
    database_manager = DatabaseAccessSingleton()
    database_manager.setup_database()
    controller = Controller()
    sys.exit(controller.run())
