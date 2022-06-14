import sys

from src.function.data_mappers.function_exercise_data_mapper import FunctionExerciseDataMapper
from src.projectConf.app import Controller
from src.projectConf.database.database_manager import DatabaseManager

if __name__ == '__main__':
    database_manager = DatabaseManager()
    database_manager.setup_database()
    controller = Controller()
    sys.exit(controller.run())
