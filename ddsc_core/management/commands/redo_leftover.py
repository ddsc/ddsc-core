from os import listdir
from os.path import isfile
from django.core.management.base import BaseCommand
from ddsc_worker.celery import celery
from ddsc_core.models.system import Folder


class Command(BaseCommand):
    help = 'Scan a file directory to reschedule the tasks'
    args = '<path for incoming csv files and socket>'

    def handle(self, *args, **options):
        filePath_socket = '/mnt/ftp/socket/'
        filePath_file_obj = Folder.objects.all()
        for folder in filePath_file_obj:
            path = folder.path
            for file in listdir(path):
                if isfile(path + file):
                    celery.send_task(
                        "ddsc_worker.tasks.new_file_detected", kwargs={
                        "pathDir": path,
                        "fileName": file,
                        }
                    )

        for file in listdir(filePath_socket):
            if isfile(filePath_socket + file):
                celery.send_task(
                    "ddsc_worker.tasks.new_socket_detected", kwargs={
                    "pathDir": filePath_socket,
                    "fileName": file,
                    }
                )
        print 'complete!'
