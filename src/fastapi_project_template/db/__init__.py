from python3_commons.conf import db_settings
from python3_commons.db import AsyncSessionManager

from fastapi_project_template.conf import ro_db_settings

db_configs = {
    'main': db_settings,
    'ro': ro_db_settings if ro_db_settings.dsn else db_settings,
}

async_session_manager = AsyncSessionManager(db_configs)
get_main_db_session = async_session_manager.get_async_session('main')
get_ro_db_session = async_session_manager.get_async_session('ro')
