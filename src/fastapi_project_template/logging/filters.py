import logging


def filter_maker(level):
    level = getattr(logging, level)

    def record_filter(record):
        return record.levelno <= level

    return record_filter
