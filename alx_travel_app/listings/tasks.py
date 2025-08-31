from celery import shared_task

@shared_task
def example_listing_task():
    print('This is a background task for listings app.')
    return 'Task completed.'
