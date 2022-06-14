from .py_math_app import PyMathApp
from ..models import Topic
from ..views import WelcomePage, TopicPage
from ...function.views import FunctionExercisePage


class Controller:
    def __init__(self):
        self._app = None
        self._current_view = None
        self._previous_view = None

    def run(self):
        self._init_app()
        self._start_app_flow()
        self._execute_app()

    def _init_app(self):
        self._app = PyMathApp(sys_argv=[])

    def _start_app_flow(self):
        FunctionExercisePage(subtopic=Topic(identifier=2, title='Tópicos', description='', topic_parent_id=None)).draw()
        # self._setup_front_page()

    def _setup_front_page(self):
        front_page = WelcomePage()
        front_page.draw()
        self._current_view = front_page
        self._current_view.continue_signal.connect(self._setup_topic_page)
        self._current_view.close_signal.connect(self._close_page)

    def _setup_topic_page(self):
        topic_page = TopicPage()
        topic_page.draw()
        self._current_view, self._previous_view = topic_page, self._current_view
        self._current_view.close_signal.connect(self._close_page)
        self._current_view.continue_signal.connect(self._setup_subtopic_page)

    def _setup_subtopic_page(self, topic: Topic):
        topic_page = TopicPage(topic=topic)
        topic_page.draw()
        self._current_view, self._previous_view = topic_page, None
        self._current_view.close_signal.connect(self._close_page)
        self._current_view.continue_signal.connect(self._setup_exercise_page)

    def _setup_exercise_page(self, subtopic: Topic):
        exercise_page = self._get_exercise_page(subtopic=subtopic)
        exercise_page.draw()
        self._current_view, self._previous_view = exercise_page, None

    def _close_page(self):
        if self._previous_view:
            self._previous_view.show()
        self._current_view.close()
        self._current_view = self._previous_view

    def _execute_app(self):
        self._app.exec()

    @staticmethod
    def _get_exercise_page(subtopic: Topic):
        return FunctionExercisePage(subtopic=subtopic)
