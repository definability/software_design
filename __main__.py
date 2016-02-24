import psycopg2
from random import randint
from os import linesep
from datetime import datetime, timedelta

from src import TransactionManager
from src.utils import get_fly_book, get_hotel_book


USER = 'test_user'
PASSWORD = '123'
HOST = 'localhost'
CONNECTION_PREFIX = "host='{host}' user='{user}' password='{password}'".format(
                     host=HOST, user=USER, password=PASSWORD)


def get_fly_connection():
    connection_string = "{connection} dbname='{db}'".format(
                          connection=CONNECTION_PREFIX, db='test_db_fly')
    return psycopg2.connect(connection_string)


def get_hotel_connection():
    connection_string = "{connection} dbname='{db}'".format(
                          connection=CONNECTION_PREFIX, db='test_db_hotel')
    return psycopg2.connect(connection_string)


def fly(tm, values):

    query_string = "insert into fly_booking (client_name, fly_number, fly_from, fly_to, book_date) values ('{client}', '{number}', '{fly_from}', '{fly_to}', '{book_date}');"
    queries = [query_string.format(**value) for value in values]
    #print linesep.join(queries)

    connection = get_fly_connection()
    cursor = connection.cursor()

    success = tm.add_transaction(cursor, queries)

    if not success:
        return connection

    print 'Commands fly ready'.upper()
    print linesep.join(queries)

    return connection


def hotel(tm, values):

    query_string = "insert into hotel_booking (client_name, hotel_name, arrival_date, departure_date) values ('{client}', '{hotel}', '{arrival}', '{departure}');"
    queries = [query_string.format(**value) for value in values]
    #print linesep.join(queries)

    connection = get_hotel_connection()
    cursor = connection.cursor()

    success = tm.add_transaction(cursor, queries)

    if not success:
        print 'Commands for hotel failed'.upper()
        return connection

    print 'Commands for hotel ready'.upper()
    print linesep.join(queries)

    return connection


if __name__ == '__main__':

    tm = TransactionManager()

    fly_book = get_fly_book()
    hotel_book = get_hotel_book()
    fly_connection = fly(tm, [fly_book])
    hotel_connection = hotel(tm, [hotel_book])

    tm.commit_transactions()

    fly_connection.close()
    hotel_connection.close()

