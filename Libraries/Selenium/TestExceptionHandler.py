import sys
import traceback


def driverhandler(func):
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            error_type = sys.exc_info()[0]
            error_obj = sys.exc_info()[1]
            # error_location = sys.exc_info()[2]
            print error_type
            print error_obj
            print traceback.print_exc()
            try:
                args[0].driver.close()
            except Exception:
                print 'Cannot Close driver'
            raise Exception('Test Execution Exception. Web driver is closed.')
    return inner
