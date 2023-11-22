from celery import shared_task

from core.containers import VisitorContainer


@shared_task
def debug_task():
    print("DEBUG")
    return


@shared_task
def sample_task():
    print('aaa')


@shared_task
def get_statistic_for_the_last_week():
    visitor_interactor = VisitorContainer.interactor()

    visitor_interactor.change_total_reading_time_for_the_last_week()


@shared_task
def get_statistic_for_the_last_month():
    visitor_interactor = VisitorContainer.interactor()

    visitor_interactor.change_total_reading_time_for_the_last_month()
