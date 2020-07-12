import datetime


def verify_response_time(response, expected_time):
    return response.elapsed < datetime.timedelta(seconds=expected_time)
