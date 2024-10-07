"""
Hiding passwords
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

load_dotenv('./drfsite/.env')
userid = os.environ.get('USERID')
dbpass = os.environ.get('SECRET_KEY')
db_url = os.environ.get('DATABASE_URL')
dbname = os.environ.get('DATABASENAME')
dbhost = os.environ.get('DBHOST')
dbport = os.environ.get('DBPORT')
dbliten = os.environ.get('DBSQLITENAME')
dblitepsw = os.environ.get('DBSQLITEPSW')
percentile = os.environ.get('PERCENTILE')
exch_username = os.environ.get('EXCH_USERID')
exch_userkey = os.environ.get('EXCH_USERKEY')
exch_serverurl = os.environ.get('EXCH_SERVER_URL')
exch_usersmtpaddr = os.environ.get('EXCH_SMTP_USERADDR')
exch_authtype = os.environ.get('EXCH_AUTH_TYPE')
inb_fold = os.environ.get('INBOX_FOLDER')
inb_fold_sales = os.environ.get('INBOX_FOLDER_SALES')
inb_fold_supp = os.environ.get('INBOX_FOLDER_SUPP')
inb_fold_other = os.environ.get('INBOX_FOLDER_OTHER')
email_templ_path = os.environ.get('EMAIL_TEMPL_PATH')
draft_email_templ_path = os.environ.get('DRAFT_EMAIL_TEMPL')
tmp_path = os.environ.get('TMP_PATH')
email_templ_path_mac = os.environ.get('EMAIL_TEMPL_PATHMAC')
