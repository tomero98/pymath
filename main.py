import sys

from src.projectConf.app import Router
from src.projectConf.database import DatabaseAccessSingleton

if __name__ == '__main__':
    database_manager = DatabaseAccessSingleton()
    database_manager.setup_database()
    router = Router()
    sys.exit(router.run())
