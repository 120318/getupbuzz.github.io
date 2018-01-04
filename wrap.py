#coding=utf-8
# not support nested now.
import sys
import datetime
import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

output_dir = './_posts/'
input_dir = './src_post/'
prefix_content = '''---
layout: default
title: {}
---
'''

class CustomHandler(PatternMatchingEventHandler):
    def on_created(self, event):
        super(CustomHandler, self).on_created(event)
        if not event.is_directory:
            modify_file(event.src_path)
            logging.info("Created file: %s", event.src_path)

    def on_deleted(self, event):
        super(CustomHandler, self).on_deleted(event)
        if not event.is_directory:
            del_file(event.src_path)
            logging.info("Deleted file: %s", event.src_path)

    def on_modified(self, event):
        super(CustomHandler, self).on_modified(event)
        if not event.is_directory:
            modify_file(event.src_path)
            logging.info("Created file: %s", event.src_path)

def modify_file(path):
    time = datetime.datetime.now().strftime('%Y-%m-%d')
    name = path.split('/')[-1]
    file = open(path, 'r')
    content = file.read()
    file.close()
    t_file = open(output_dir +time + '-' +name, 'w')
    t_file.write(prefix_content.format(name.split('.')[0]))
    t_file.write(content)
    t_file.close()

def del_file(path):
    files = os.listdir(output_dir)
    for f in files:
        if f.endswith(path.split('/')[-1]):
            os.remove(output_dir + f)
            break

if __name__ == "__main__":
    print 'Start watch directory: ' + input_dir
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = CustomHandler()
    observer = Observer()
    observer.schedule(event_handler, input_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print 'Stop Watch!'
    observer.join()
