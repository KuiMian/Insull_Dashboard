import os


def update_and_summary():
    print('data has update.')

    os.system('python update_yesterday.py')
    print('history data has updated.')

    os.system('python update_future.py')
    print('future data has updated.')

    os.system('python summary.py')
    print('summary has updated.')
