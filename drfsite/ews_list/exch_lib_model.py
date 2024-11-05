# -*- coding: utf-8 -*-
"""
Работаем с БД MySQL на удаленном сервере
Class pwp_model - здесь вся работа с базой данных и обработка запросов от pwp_view и pwp_exchangelib_conn

"""
# import pwp_settings as psettings  # Импортируем модуль с настройками всех параметров
from .pwp_settings import (
    exch_username,  # - это username для обращения к серверу
    exch_userkey,  # - пароль пользователя
    exch_usersmtpaddr,  # - адрес электронной почты пользователя (пресейла)
    exch_authtype,  # - тип аутентификации на exchange-сервере
    exch_serverurl,  # - адрес exchange-сервера
    inb_fold,  # - название папки, в которую будут складываться входящие сообщения из компании
    inb_fold_sales,  # - название папки, в которую будут складываться входящие сообщения от менеджеров
    inb_fold_supp,  # - название папки, в которую будут складываться входящие сообщения от поставщиков
    inb_fold_other,  # - название папки, в которую будут складываться неидентифицированная входящие сообщения
)

from typing import List, Any
import getpass
import re  # Модуль для работы с регулярными строковыми выражениями для фильтрации почты
import time
import calendar
# import os.path
from os.path import isfile, join
from os import listdir, path
import platform  # Определяем платформу
import glob
from datetime import date, datetime, timedelta
import logging
from functools import wraps
from timeit import default_timer

logger = logging.getLogger(__name__)

# from pwp_SplashScreen import *

"""
Из файла настроек для Базы Данных берем
userid      - имя пользователя для подключения к БД MySQL
dbpass      - пароль для подключения к БД MySQL
db_url      - ссылка на БД MySQL для подключения
dbname      - имя БД MySQL
dbhost      - адрес хоста БД MySQL
dbliten     - имя пользователя для подключения к БД SQLite
dblitepsw   - пароль для подключения к БД SQLite
"""

from exchangelib import (
    Account,
    Credentials,
    Build,
    Configuration,
    FaultTolerance,
    Version,
    Message,
    Mailbox,
    Folder,
    HTMLBody,
    FileAttachment,
    ItemAttachment,
    EWSDateTime,
    EWSTimeZone,
    EWSDate
)
from exchangelib.util import PrettyXmlHandler
from exchangelib.items import SEND_ONLY_TO_ALL, SEND_ONLY_TO_CHANGED
from exchangelib.properties import DistinguishedFolderId

# Список доменов компании
# company_domain = ['komus.net', 'region.komus.net', 'spb.komus.net', 'tl.komus.net', 'bony.komus.net', 'tu.komus.net']
company_domain = ['tsrv-it.ru', 'trlink.ru', 'aksinform.ru', 'tsv-llc.ru', 't-grp.ru']


# Совмещаем функцию логирования с временем выполнения
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(funcName)15s %(module)7s:%(lineno)d %(levelname)-6s - %(message)s",
        handlers=[PrettyXmlHandler()]
    )


def timer(func):
    @wraps(func)
    def wrapper(*a, **kw):
        start_time = default_timer()
        result = func(*a, **kw)
        total_time = default_timer() - start_time
        logger.info(
            "Func %s call total time %.3f",
            func.__name__,
            total_time,
        )
        return result

    return wrapper


"""
Класс для работы с Exchange-сервером
"""


class pwp_exch_model:
    # 0 - Total, 1 - Unread, 2 - Suppl, 3 - mtst, 4 - other, 5 - Komus
    msg_cnt_list = [0, 0, 0, 0, 0, 0]  # Обнуляем список счетчиков полученных сообщений в папке inbox
    current_message = None  # Текущее обрабатываемое сообщение
    configure_logging()
    # Most class definitions have a docstring containing
    # a URL to the MSDN page for the corresponding XML element.
    # Your code that uses Exchangelib Python, and needs debugging goes here:

    @timer
    def __init__(self):  # Подключаемся к Exchange-серверу и проверяем подключение
        try:
            self.credents_project = Credentials(username=exch_username, password=exch_userkey)
            logger.info("Запустили подключение Credentials")
        except AttributeError:
            logger.error("Потерялся файл с конфигурацией в директории проекта")
            exit()
        logger.info("Параметры Credentials из Docstring: %s", Credentials.__doc__)
        self.version = Version(build=Build(15, 0, 1497, 4012))
        logger.info("Параметры Version из Docstring: %s", Version.__doc__)
        # Обрабатываем ошибку в параметрах Exchange-сервера
        try:
            self.conf_exchange = Configuration(
                server=exch_serverurl, retry_policy=FaultTolerance(max_wait=3600), credentials=self.credents_project,
                version=self.version, auth_type=exch_authtype, max_connections=10)
        except NameError:
            print("Не заданы параметры Exchange-сервера")
            exit()
        logger.info("Параметры Configuration из Docstring: %s", Configuration.__doc__)
        # Подключаемся к Exchange-аккаунту на основе данных из конфигурационного файла
        self.my_acc_exch = Account(primary_smtp_address=exch_usersmtpaddr, config=self.conf_exchange,
                                   credentials=self.credents_project, autodiscover=False)
        logger.info("Параметры Account из Docstring: %s", Account.__doc__)
        # Определяемся с Тайм-зонами
        # logging.info(f'default_timezone : {self.my_acc_exch.default_timezone}')
        d = EWSDateTime(2024, 10, 28, tzinfo=EWSTimeZone.localzone())
        # current_tzinfo = EWSTimeZone.localzone()
        # logger.info('Текущая тайм-зона: %s ', current_tzinfo)
        logger.info('Текущая тайм-зона по datetime: %s ', datetime(*d.timetuple()[:6], tzinfo=d.tzinfo))
        # Инициируем папки для сортировки входящих сообщений
        # print("pwp_exch_model --> Подключились к аккаунту:", self.my_acc_exch)
        # print("pwp_exch_model --> exch_serverurl:", exch_serverurl)
        # print("pwp_exch_model --> self.credents_project:", self.credents_project)
        # print("pwp_exch_model --> exch_authtype:", exch_authtype)
        self.get_fold_supp = ''
        self.f_in = self.my_acc_exch.inbox // inb_fold
        self.f_in_sales = self.my_acc_exch.inbox // inb_fold_sales
        self.f_in_supp = self.my_acc_exch.inbox // inb_fold_supp
        self.f_in_other = self.my_acc_exch.inbox // inb_fold_other
        self.f_in_requests = self.my_acc_exch.inbox // 'ЗАПРОСЫ'
        self.f_in_projects = self.my_acc_exch.inbox // 'ПРОЕКТЫ'
        # self.f_supp_folder = None  # Начальный шаблон для добавления
        # self.f_supp_folder = self.my_acc_exch.inbox / 'DISTI'  # Начальный шаблон для добавления
        # self.f_vendor_folder = self.my_acc_exch.inbox / 'Vendors'  # Начальный шаблон для добавления

        # Отображаем количество сообщений в папке Входящие
        self.count_inbox_msg()
        # print("pwp_exch_model --> Определяем количество сообщений:")

    """
    Отправка сообщений адресату
    """

    def msg_send(self, m_body):  # Передаем только тело сообщения для отправки
        item = self.current_message
        acc = self.my_acc_exch
        # recipients: list[Any]
        recipients = [item.sender.email_address]
        print(f'pwp_exch_model -> msg_send -> item.subject: {item.subject}')
        print(f'pwp_exch_model -> msg_send -> recipients: {recipients}')
        print(f'pwp_exch_model -> msg_send -> item.cc_recipients: {item.cc_recipients}')
        m = Message(account=acc, folder=acc.sent, subject=item.subject, body=m_body,
                    to_recipients=recipients, cc_recipients=item.cc_recipients)
        m.send_and_save()

    @timer
    def count_inbox_msg(self):
        # 0 - Total, 1 - Unread, 2 - Suppl, 3 - mtst, 4 - other, 5 - Komus
        print("pwp_exch_model --> count_inbox_msg --> Обновляем папку Inbox")
        self.my_acc_exch.inbox.refresh()
        print("pwp_exch_model --> count_inbox_msg --> Считаем сообщения")
        self.msg_cnt_list[0] = self.my_acc_exch.inbox.total_count  # Всего сообщений в папке Входящие
        self.msg_cnt_list[1] = self.my_acc_exch.inbox.unread_count  # Непрочитанных сообщений в папке Входящие
        all_items = self.my_acc_exch.inbox // inb_fold_supp  # Всего сообщений в папке Поставщики
        self.msg_cnt_list[2] = all_items.total_count
        all_items = self.my_acc_exch.inbox // inb_fold_sales  # Всего сообщений в папке МТСТ
        self.msg_cnt_list[3] = all_items.total_count
        all_items = self.my_acc_exch.inbox // inb_fold_other  # Всего сообщений в папке Другие
        self.msg_cnt_list[4] = all_items.total_count
        all_items = self.my_acc_exch.inbox // inb_fold  # Всего сообщений в папке Комус
        self.msg_cnt_list[5] = all_items.total_count
        self.my_acc_exch.inbox.refresh()

    @staticmethod
    def create_attachement_list(item, files_attach):
        # Сначала вытаскиваем вложения из письма
        for attachment in item.attachments:
            if isinstance(attachment, FileAttachment):
                local_path = os.path.join(psettings.tmp_path, attachment.name)
                # print('create_attachement_list -> local_path: ', local_path)
                # local_path = os.path.join(tmp_path, attachment.name)
                # Добавили название файла в список combobox_attach
                files_attach.append(attachment.name)
                try:
                    with open(local_path, 'wb') as fopen:
                        fopen.write(attachment.content)
                except:
                    print(f'Файл {fopen} занят другим процессом!')
                    pass
                # print('create_attachement_list -> Saved attachment to', local_path)
            elif isinstance(attachment, ItemAttachment):
                if isinstance(attachment.item, Message):
                    try:
                        print('create_attachement_list -> Сообщение:', attachment.item.subject, attachment.item.body)
                    except:
                        pass
        return files_attach

    @staticmethod
    def clear_tmp_dir():
        # Проверяем наличие файлов в папке TMP и после этого удаляем
        # Добавляем файлы шаблонов в выпадающий список
        if platform.system() == 'Darwin':
            files = glob.glob(psettings.tmp_path + '/*')
        else:
            files = glob.glob(psettings.tmp_path + '/*')
        for f in files:
            try:
                os.remove(f)
            except:
                print('clear_tmp_dir -> файл - {f} открыт в другом приложении!')

    @staticmethod
    def msg_move2folder(msg2move, folder, mark_unread):  # Перемещаем сообщение msg2move в папку folder
        if mark_unread == 0:
            msg2move.is_read = True
        else:
            msg2move.is_read = False
        try:  # Запускаем исключение для Meeting requests, которые не перекладываются в папки
            msg2move.move(folder)
            msg2move.save()
        except:
            pass  # Пока так - нужен анализ типа сообщения во входящих

# Обнуляем счетчик в таблице project до единицы
# ALTER TABLE project AUTO_INCREMENT = 1
