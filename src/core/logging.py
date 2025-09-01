import logging
import logging.handlers
import sys

import structlog
from structlog.processors import CallsiteParameter, JSONRenderer

from configs.settings import settings

# structlog 공통 설정
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.contextvars.merge_contextvars,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
        structlog.processors.CallsiteParameterAdder(
            parameters=[
                CallsiteParameter.FILENAME,
                CallsiteParameter.LINENO,
                CallsiteParameter.FUNC_NAME,
            ],
        ),
        # 이 프로세서는 항상 마지막에 두는 것이 좋습니다.
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


# 콘솔 핸들러 설정
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(
    structlog.stdlib.ProcessorFormatter(
        # 렌더링만 담당하도록 단순화
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(colors=True),
        ],
        foreign_pre_chain=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(
                fmt="%Y-%m-%d %H:%M:%S", utc=False
            ),
        ],
    )
)

# 파일 핸들러 설정
file_handler = logging.handlers.RotatingFileHandler(
    settings.log_path, maxBytes=10_000_000, backupCount=5, encoding="utf-8"
)
file_handler.setFormatter(
    structlog.stdlib.ProcessorFormatter(
        # JSON 렌더링만 담당
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.dict_tracebacks,
            JSONRenderer(ensure_ascii=False),
        ],
        foreign_pre_chain=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(
                fmt="%Y-%m-%d %H:%M:%S", utc=False
            ),
        ],
    )
)

# 루트 로거에 핸들러 추가
root_logger = logging.getLogger()
root_logger.handlers.clear()
root_logger.addHandler(console_handler)
root_logger.addHandler(file_handler)
root_logger.setLevel(logging.INFO)


def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    """
    처리되지 않은 예외를 로깅하기 위한 함수.
    sys.excepthook의 표준 인자를 그대로 받음.
    """
    # 사용자가 Ctrl+C로 종료한 경우는 무시
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger = structlog.get_logger("uncaught_exception")

    # exc_info에 예외 튜플을 전달하면 structlog가 처리
    logger.error(
        "처리되지 않은 예외가 발생했습니다.",
        exc_info=(exc_type, exc_value, exc_traceback),
    )
