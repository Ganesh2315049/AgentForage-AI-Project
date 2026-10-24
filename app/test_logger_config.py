
from logger_config import LOG_FILE, logger


def test_logger_writes_to_file():
    test_message = "SentinelAgent logging test"

    logger.info(test_message)

    for handler in logger.handlers:
        handler.flush()

    assert LOG_FILE.exists()
    assert test_message in LOG_FILE.read_text(encoding="utf-8")
