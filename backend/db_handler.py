from typing import final
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text, func
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, DateTime
import pymysql
import pymysql.cursors

import datetime
import pandas as pd

import utils
import config

DB_ADDRESS = config.DB_ADDRESS
DB_USER = config.DB_USER
DB_PASSWORD = config.DB_PASSWORD


def get_db_connection():
    conn = pymysql.connect(host=DB_ADDRESS, port=3306, user=DB_USER, password=DB_PASSWORD,
                           db='psat_capstone', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    return conn


def create_database():
    # TODO : 데이터베이스를 생성합니다.
    conn = pymysql.connect(host=DB_ADDRESS, port=3306,
                           user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    sql = "CREATE DATABASE psat_capstone;"
    cursor.execute(sql)
    cursor.execute("USE model_info;")
    conn.commit()
    conn.close()


def _create_history_table(conn):
    with conn.cursor() as cursor:
        sql = '''
            CREATE TABLE `history` (
                `HISTORY_ID` int() NOT NULL AUTO_INCREMENT,
                `DATE` datetime NOT NULL,
                `WORKER_ID` int() NOT NULL,
                `COIL_ID` int() NOT NULL,
                `CRM_ID` int() NOT NULL,
                `THICKNESS_PRED` decimal(11,8) NOT NULL,
                PRIMARY KEY (`HISTORY_ID`)
            ) 
        '''
        cursor.execute(sql)
        conn.commit()


def _create_feature_history_table(conn):
    with conn.cursor() as cursor:
        sql = '''
            CREATE TABLE `history_features` (
                `HISTORY_ID` int(11) NOT NULL,
                `FEATURE_1` decimal(11,8) NOT NULL,
                `FEATURE_2` decimal(11,8) NOT NULL,
                `FEATURE_3` decimal(11,8) NOT NULL,
                `FEATURE_4` decimal(11,8) NOT NULL,
                `FEATURE_5` decimal(11,8) NOT NULL,
                `FEATURE_6` decimal(11,8) NOT NULL,
                `FEATURE_7` decimal(11,8) NOT NULL,
                `FEATURE_8` decimal(11,8) NOT NULL,
                `FEATURE_9` decimal(11,8) NOT NULL,
                `FEATURE_10` decimal(11,8) NOT NULL,
                `FEATURE_11` decimal(11,8) NOT NULL,
                `FEATURE_12` decimal(11,8) NOT NULL,
                PRIMARY KEY (`HISTORY_ID`),
            CONSTRAINT `FeaturesToHistory` FOREIGN KEY (`HISTORY_ID`) REFERENCES `history` (`HISTORY_ID`) ON DELETE CASCADE ON UPDATE CASCADE
            ) 
        '''
        cursor.execute(sql)
        conn.commit()


def create_tables(conn):
    _create_history_table(conn)
    _create_feature_history_table(conn)
    conn.commit()


def insert_history(conn, value_dict):
    with conn.cursor() as cursor:
        sql = "INSERT INTO history (`DATE`, `WORKER_NAME`, `COIL_ID`, `CRM_ID`, `THICKNESS_PRED`) VALUES (%(DATE)s, %(WORKER_NAME)s, %(COIL_ID)s, %(CRM_ID)s, %(THICKNESS_PRED)s)"
        cursor.execute(sql, value_dict)
        conn.commit()


def insert_feature_history(conn, value_dict):
    with conn.cursor() as cursor:
        sql = "INSERT INTO history_features (`FEATURE_1`, `FEATURE_2`, `FEATURE_3`, `FEATURE_4`, `FEATURE_5`, `FEATURE_6`,`FEATURE_7`, `FEATURE_8`, `FEATURE_9`, `FEATURE_10`, `FEATURE_11`, `FEATURE_12`) VALUES ('%(FEATURE_1)s', '%(FEATURE_2)s', %(FEATURE_3)s, %(FEATURE_4)s, %(FEATURE_5)s, %(FEATURE_6)s, %(FEATURE_7)s, %(FEATURE_8)s, %(FEATURE_9)s, %(FEATURE_10)s,  %(FEATURE_11)s, %(FEATURE_12)s)"

        cursor.execute(sql, value_dict)
        conn.commit()


def get_history(conn):
    with conn.cursor() as cursor:
        sql = '''
               SELECT * 
               FROM history, history_features
               WHERE history.HISTORY_ID = history_features.HISTORY_ID
      '''

        cursor.execute(sql)
        history_info = cursor.fetchall()
    return history_info


def split_data(params):
    hitory_input_dict = {}
    feature_history_input_dict = {}
    for key, value in params.items():
        if key in utils.hitory_columns:
            if key == 'DATE':
                hitory_input_dict[key] = datetime.datetime.strptime(
                    value, '%d/%m/%Y, %H:%M:%S')
            elif key == 'WORKER_NAME':
                hitory_input_dict[key] = value
            elif key == 'COIL_ID':
                hitory_input_dict[key] = value
            elif key == 'CRM_ID':
                hitory_input_dict[key] = value
            else:
                hitory_input_dict[key] = round(float(value), 4)
        else:
            feature_history_input_dict[key] = round(float(value), 4)

    return hitory_input_dict, feature_history_input_dict
