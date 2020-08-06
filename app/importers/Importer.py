import shutil
import os
import stat
import tempfile

from django.conf import settings


class Importer:

    def __init__(self, data, file_id):
        self.data = data
        self.columns = None
        self.temp_dir = None
        self.file_id = file_id
        self.table = "importers_dumpfiledata"

    def run(self):
        self.set_columns()
        file_path = self.get_file_path()
        self.save_data(file_path)
        self.import_data(file_path)
        self.remove_temp_dir()

    def set_columns(self):
        self.columns = list(self.data[0].keys())
        self.columns.extend(["file_id"])

    def set_temp_dir(self):
        self.temp_dir = tempfile.mkdtemp()

    def get_file_path(self):
        self.set_temp_dir()
        file_name = "dump_file.csv"
        file_path = os.path.join(self.temp_dir, file_name)
        return file_path

    def save_data(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            tmp_data = [','.join(self.columns) + '\n']
            for row in self.data:
                tmp_record = []
                for col in self.columns:
                    if col == 'file_id':
                        tmp_record.append(str(self.file_id))
                    else:
                        tmp_record.append(str(row.get(col, '')))
                tmp_data.append(','.join(tmp_record) + '\n')
            file.writelines(tmp_data)

    def remove_temp_dir(self):
        if self.temp_dir:
            try:
                shutil.rmtree(self.temp_dir)  # delete directory
            except Exception as exc:
                print(exc)

    def import_data(self, file_path):
        os.chmod(file_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        os.system("mysql --host={host} --port={port} --user={user} --password={password} --database={database} " \
                  "--execute=\"LOAD DATA LOCAL INFILE '{file_path}' INTO TABLE {table} FIELDS TERMINATED BY '{sep}' " \
                  "OPTIONALLY ENCLOSED BY '\\\"' IGNORE 1 LINES ({columns}); SHOW WARNINGS\""
                  .format(host=settings.DATABASES["default"]['HOST'],
                          port=settings.DATABASES["default"]['PORT'],
                          user=settings.DATABASES["default"]['USER'],
                          password=settings.DATABASES["default"]['PASSWORD'],
                          database=settings.DATABASES["default"]['NAME'],
                          file_path=file_path, sep=',', columns=','.join(self.columns),
                          table=self.table))
