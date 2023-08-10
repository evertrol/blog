import logging
logging.basicConfig(
        format="%(asctime)s [%(levelname)-5s] - %(funcName)s():%(lineno)d: %(message)s",
        datefmt="%y-%m-%d %H:%M:%S",
        level=logging.DEBUG
    )


def main():
    myvar = 1.23
    logging.debug("myvar = %s", myvar)

if __name__ == '__main__':
    main()
