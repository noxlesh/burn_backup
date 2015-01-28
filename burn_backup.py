#!/usr/bin/python2
from isogen import IsoGen

BAK_DIR = '/media/backup-sql/'
ISO_DIR = '/media/store/backup/'

backup = IsoGen(BAK_DIR, ISO_DIR)
backup.get_1c_archives_list()
backup.mk_iso()