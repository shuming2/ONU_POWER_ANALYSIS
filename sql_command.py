

SELECT_COUNT_IN_TIME_PERIOD = """SELECT MIN(STATIS_TIME), MAX(STATIS_TIME), COUNT(DISTINCT STATIS_TIME, GPON_REPORT_OLT, ONU_SN, FIBER_POWER_AVG)
                                 FROM ONUFIBERN
                                 WHERE STATIS_TIME >= '{}'
                                 AND STATIS_TIME <= '{}';"""

SELECT_DATA_BY_STATIS_TIME = """SELECT DISTINCT STATIS_TIME, GPON_REPORT_OLT, ONU_SN, FIBER_POWER_AVG
                                FROM ONUFIBERN
                                WHERE STATIS_TIME = '{}';"""

SELECT_DATA_BY_GPON_REPORT_OLT = """SELECT DISTINCT FIBER_POWER_AVG, STATIS_TIME
                                    FROM ONUFIBERN
                                    WHERE GPON_REPORT_OLT = '{}';"""

SELECT_DISTINCT_GPON_REPORT_OLT = """SELECT DISTINCT GPON_REPORT_OLT, ONU_SN
                                     FROM ONUFIBERN;"""

SELECT_DISTINCT_GPON_REPORT_OLT_WITH_SEARCH_INPUT = """SELECT DISTINCT GPON_REPORT_OLT, ONU_SN 
                                                       FROM ONUFIBERN
                                                       WHERE {} LIKE '%{}%';"""

SELECT_MAX_STATIS_TIME = "SELECT MAX(STATIS_TIME) FROM ONUFIBERN;"

INSERT_ONUFIBERN = """INSERT INTO ONUFIBERN(GPON_REPORT_OLT, VENDOR, ZH_LABEL, INT_ID, DEVICE_TYPE, OLT_PORT_NAME, 
                      OLT_PORT_ID, OLT_NAME, OLT_IP_ADDRESS, OLT_ID, CONUTY_NAME, CITY_NAME, CITY_ID, ID, 
                      FIBER_MODULE_TYPE, IS_LOVER_ZH, FIBER_POWER_MAX, FIBER_POWER_MIN, FIBER_POWER_AVG, 
                      LOWER_POWER_LIMIT, GATHER_NUM, ACHIEVE_NUM, UNACHIEVE_NUM, IS_OVERLOAD, ONU_ID, CELL_ID, 
                      CELL_NAME, CUSTOMER_ACCOUNT, ROOM_NO, FULL_ADDR, STATIS_CYCLE, OLT_PORT_ALIAS, ONU_NO, ONU_SN,
                      STATIS_TIME)
                      VALUES """

COLUMN_NAME_ONUFIBERN = ['GPON_REPORT_OLT', 'VENDOR', 'ZH_LABEL', 'INT_ID', 'DEVICE_TYPE', 'OLT_PORT_NAME',
                         'OLT_PORT_ID', 'OLT_NAME', 'OLT_IP_ADDRESS', 'OLT_ID', 'CONUTY_NAME', 'CITY_NAME', 'CITY_ID',
                         'ID', 'FIBER_MODULE_TYPE', 'IS_LOVER_ZH', 'FIBER_POWER_MAX', 'FIBER_POWER_MIN',
                         'FIBER_POWER_AVG', 'LOWER_POWER_LIMIT', 'GATHER_NUM', 'ACHIEVE_NUM', 'UNACHIEVE_NUM',
                         'IS_OVERLOAD', 'ONU_ID', 'CELL_ID', 'CELL_NAME', 'CUSTOMER_ACCOUNT', 'ROOM_NO', 'FULL_ADDR',
                         'STATIS_CYCLE', 'OLT_PORT_ALIAS', 'ONU_NO', 'ONU_SN', 'STATIS_TIME']


CREATE_ONUFIBERN_TABLE = """CREATE TABLE ONUFIBERN (
                            GPON_REPORT_OLT VARCHAR(255),
                            VENDOR VARCHAR(255),
                            ZH_LABEL VARCHAR(255),
                            INT_ID DOUBLE,
                            DEVICE_TYPE VARCHAR(60),
                            OLT_PORT_NAME VARCHAR(255),
                            OLT_PORT_ID DOUBLE,
                            OLT_NAME VARCHAR(255),
                            OLT_IP_ADDRESS VARCHAR(120),
                            OLT_ID DOUBLE,
                            CONUTY_NAME VARCHAR(120),
                            CITY_NAME VARCHAR(60),
                            CITY_ID DOUBLE,
                            ID DOUBLE,
                            FIBER_MODULE_TYPE VARCHAR(60),
                            IS_LOVER_ZH VARCHAR(2),
                            FIBER_POWER_MAX DOUBLE,
                            FIBER_POWER_MIN DOUBLE,
                            FIBER_POWER_AVG DOUBLE,
                            LOWER_POWER_LIMIT DOUBLE,
                            GATHER_NUM DOUBLE,
                            ACHIEVE_NUM DOUBLE,
                            UNACHIEVE_NUM DOUBLE,
                            IS_OVERLOAD DOUBLE,
                            ONU_ID DOUBLE,
                            CELL_ID DOUBLE,
                            CELL_NAME VARCHAR(255),
                            CUSTOMER_ACCOUNT VARCHAR(255),
                            ROOM_NO VARCHAR(255),
                            FULL_ADDR VARCHAR(255),
                            STATIS_CYCLE CHAR(2),
                            OLT_PORT_ALIAS VARCHAR(255),
                            ONU_NO DOUBLE,
                            ONU_SN VARCHAR(255),
                            STATIS_TIME DATETIME,
                            PRIMARY KEY(id));"""

