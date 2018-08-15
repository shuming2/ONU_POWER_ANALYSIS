import datetime

# Database
USERNAME = 'amber'
PWD = '19950613'
DB_NAME = 'cm_gpon_report'
TABLE_NAME = 'onufibern'

# Update Database
MAX_EMPTY_DAYS = 3
INITIAL_TIME = datetime.datetime(2018, 5, 31, 0, 0)

# API
API_URL = 'http://10.213.54.148:8080/ServiceOpenFrame/data/GPON_REPORT_ONUFIBERN_VIEW'
CONTENT_TYPE = 'application/x-www-form-urlencoded'
APP_KEY = 'df994502-f4a5-4f44-90d8-2168e71ccc22'
APP_SECRET = 'z1mVTgq7wpReR9dUL9dy'

# Alert
ALERT_THRESHOLD = 1
