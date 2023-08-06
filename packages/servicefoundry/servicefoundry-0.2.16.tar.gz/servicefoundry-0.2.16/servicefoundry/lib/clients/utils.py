from servicefoundry.lib.exceptions import BadRequestException


def request_handling(res):
    try:
        status_code = res.status_code
    except Exception as ex:
        raise Exception("Unknown error occurred. Couldn't get status code.") from ex
    if 200 <= status_code <= 299:
        if res.content == b"":
            return None
        return res.json()
    if 400 <= status_code <= 499:
        try:
            message = res.json()["message"]
        except Exception:
            message = res
        raise BadRequestException(res.status_code, message)
    if 500 <= status_code <= 599:
        raise Exception(res.content)
