import os


def update_and_summary():

    print('data is updating.\n')

    try:
        os.system('python get_yesterday.py')
        print('history data has overridden.\n')
    except:
        print('get_yesterday raise error. ')
    else:
        os.system('python update_yesterday.py')
        print('yesterday data has updated.\n')

        try:
            os.system('python get_future.py')
            print('future data has updated.\n')
        except:
            print('get_future raise error. ')
        else:
            os.system('python summary.py')
            print('summary has generated.\n')

    print('\n\n\n')


update_and_summary()