from ProxyPool.getter import Getter
from ProxyPool.validator import Validator
from ProxyPool.conf import CRAWL_CYCLE_TIME, VALIDATE_CYCLE_TIME, VALIDATE_URL_NUMBER

def main():
    Validator(VALIDATE_CYCLE_TIME, VALIDATE_URL_NUMBER).start()
    Getter(CRAWL_CYCLE_TIME).start()


if __name__ == '__main__':
    main()
