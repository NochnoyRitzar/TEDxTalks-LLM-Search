import os
import re
import logging
import pandas as pd


def load_csv_data(df_path):
    """
    Load csv file from specified path and return pandas DataFrame

    :param df_path: path to csv file
    :type df_path: str
    :return: pandas DataFrame
    :rtype: pandas.DataFrame
    """
    df = pd.read_csv(df_path)
    return df


def create_logger(logger_name, log_filename):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    log_format = logging.Formatter('%(levelname)s: %(asctime)s - %(message)s')
    handler = logging.FileHandler(filename=os.path.join('logs', log_filename), encoding='utf-8', mode='w')
    handler.setFormatter(log_format)
    logger.addHandler(handler)

    return logger
