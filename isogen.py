__author__ = 'noxlesh'

import os
import datetime
import subprocess


class IsoGen(object):
    DVD_SIZE = 4700372992
    backup_list = []

    def __init__(self, bak_dir, iso_dir):
        self.bak_dir = bak_dir
        self.iso_dir = iso_dir

    # Generate backup file list
    def get_1c_archives_list(self):
        bak_1c_files = []
        os.chdir(self.bak_dir)
        all_bak_files = [archive for archive in os.listdir('.') if archive.endswith('.7z')]

        cur_date = datetime.date.today()
        past_monday = cur_date - datetime.timedelta(cur_date.weekday())
        past_friday = past_monday - datetime.timedelta(3)
        past_thursday = past_friday - datetime.timedelta(1)
        past_wednesday = past_thursday - datetime.timedelta(1)
        past_tuesday = past_wednesday - datetime.timedelta(1)
        past_saturday = past_tuesday - datetime.timedelta(3)

        for archive_name in all_bak_files:
            if archive_name.endswith(past_friday.strftime('%Y%m%d') + '.7z'):
                bak_1c_files.append(archive_name)
            elif archive_name.endswith(past_thursday.strftime('%Y%m%d') + '.7z'):
                bak_1c_files.append(archive_name)
            elif archive_name.endswith(past_wednesday.strftime('%Y%m%d') + '.7z'):
                bak_1c_files.append(archive_name)
            elif archive_name.endswith(past_tuesday.strftime('%Y%m%d') + '.7z'):
                bak_1c_files.append(archive_name)
            elif archive_name.endswith(past_saturday.strftime('%Y%m%d') + '.7z'):
                bak_1c_files.append(archive_name)
        self.backup_list = bak_1c_files
        # return all_bak_files

    # Make iso file(s)
    def mk_iso(self):
        os.chdir(self.bak_dir)
        available_space = self.DVD_SIZE
        vol_num = 0
        vols = []

        for archive in self.backup_list:
            if available_space > os.path.getsize(archive):
                if len(vols) == vol_num:
                    print 'Making vol %d' % vol_num
                    vols.append('')
                print 'Appending %s to vol %d Current space: %d' % (archive, vol_num, available_space)
                available_space -= os.path.getsize(archive)

                vols[vol_num] += '/%s=%s%s\n' % (archive, self.bak_dir, archive)
            else:
                vol_num += 1
                available_space = self.DVD_SIZE
                if len(vols) == vol_num:
                    print 'Making vol %d' % vol_num
                    vols.append('')
                print 'Appending %s to vol %d Current space: %d' % (archive, vol_num, available_space)
                vols[vol_num] += '/%s=%s%s\n' % (archive, self.bak_dir, archive)

        os.chdir(self.iso_dir)

        for l in range((vol_num+1)):
            with open("vol_%s.list" % l, "a") as myfile:
                myfile.write(vols[l])
        for i in range((vol_num+1)):
            mkiso_out = subprocess.Popen('mkisofs -D -r -input-charset utf-8 -graft-points -path-list vol_%s.list -o %s.iso' % (i, i), shell=True, stdout=subprocess.PIPE).communicate()
            print mkiso_out[0]
            os.remove('vol_%s.list' % i)
