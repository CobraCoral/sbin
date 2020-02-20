#!/usr/bin/env python3.6

###################################################################################################
# Imports
# --=-- Standard library imports
from sys import argv, path
from os.path import abspath, dirname, join, realpath, split, isfile
import urllib
from multiprocessing import Process, Manager
import time
import datetime
import pickle

# --=-- Third party imports
from flask import Flask, json, Blueprint, render_template, abort, url_for, request, Response
from jinja2 import TemplateNotFound

# --=-- Package and Local imports
# --=-- Ugly hack import for sibling modules to allow absolute import from the root ('modules')
# folder. Please forgive the heresy.
#if __name__ == '__main__' and __package__ is None:
actual_path = realpath(argv[0])
relative_path = actual_path[actual_path.find('modules'):]
directory_depth = relative_path.count('/')-1
to_append = abspath(join(split(argv[0])[0], '../'*directory_depth))
if __debug__:
    print('Appending to path: [%s]'%(to_append))
path.append(to_append)

# --=-- Local application imports
from cronmonitor.api import common as common
if __debug__:
    print(common.get_users())
from mail import sendmail as mailx
if __debug__:
    print(dir())

###################################################################################################
# Data file
data_dump = 'registered_cron_scripts.p'

# Timeout in seconds.  If a registered script does not update greater than timeout x misses (60x2)
# in seconds, we will issue a warning
timeout = 60
timeout_misses = 2
max_timeout = timeout * timeout_misses

# Sharing data over Process.Manager
global_dict = Manager().dict()
global_dict['updatemyip'] = [datetime.datetime.now(), datetime.datetime.now()]

#script name, datetime registered, datetime updated
if isfile(data_dump):
    loaded_dict = pickle.load(open(data_dump, 'rb'))
    for k, v in loaded_dict.items():
        global_dict[k] = v
else:
    if __debug__:
        print('registered_cron_scripts.p file not found, initializing it')
    pickle.dump(dict(global_dict), open(data_dump, 'wb'))

if __name__ == '__main__':
    api = Flask(__name__)
else:
    api = Blueprint('api', __name__, template_folder='templates')

@api.route('/')
def show_info():
    app = Flask(__name__) 
    app.register_blueprint(api)

    api_dict = {}
    for rule in app.url_map.iter_rules():
        if 'static' in rule.endpoint: continue
        options = {}
        for arg in rule.arguments:
            options[arg] = '[{0}]'.format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        api_dict[rule.endpoint.replace('api.','')] = (url, methods)

    try:
        return render_template('pages/v1_api.html', api_dict=api_dict)
    except TemplateNotFound:
        abort(404)

##
# This method just exists to show how to use common methods to all versions
@api.route('/users')
def get_users():
    return 'Example of calling a module common to all versions: %s'%common.get_users()

@api.route('/list', methods=['GET'])
def get_list():
    try:
        return render_template('pages/v1_cron_scripts.html', cron_scripts=global_dict)
    except TemplateNotFound:
        abort(404)


@api.route('/update', methods=['POST'])
def post_update():
    # bad request
    if not request.json or not 'script' in request.json:
        abort(400)

    # not found
    script = request.json['script']
    if not script in global_dict.keys():
        abort(404)

    registered_time, last_updated_time = global_dict[script]
    now = datetime.datetime.now()
    # need to explicitly update the list so Process.Manager() synchronizes it across Processes
    global_dict['updatemyip'] = [registered_time, now]
    pickle.dump(dict(global_dict), open(data_dump, 'wb'))

    delta = (now - last_updated_time).total_seconds()
    rtSz = registered_time.strftime('%Y-%m-%d %H:%M:%S.%s')
    lutSz = last_updated_time.strftime('%Y-%m-%d %H:%M:%S.%s')
    return_value = {'success': True, 'result': 'GoodCron: Registered [%s] Last Time [%s], Delta [%s]'%(rtSz, lutSz, delta)}

    # OK
    return json.dumps(return_value), 200

def validate_cron_entries_updates(local_dict):
    '''
    Go through each registered script, and see if we need to alert in case the last update time
    is less than timeout X misses. It will then send an email to alert about the issue
    mailx(to='7185645054@txt.att.net', subject='subject with no body')
    mailx(to='7185645054@txt.att.net', subject='subject', body='this is the body of the email')
    :return:
    '''
    index = 1
    while True:
        # now loop throught the synchronized dictionary
        for script in local_dict.keys():
            registered_time, last_time_update = local_dict[script]
            now = datetime.datetime.now()
            delta = (now - last_time_update).total_seconds()
            if __debug__:
                print('script [%s] last update[%s] Delta since last update [%s] seconds'%(script, last_time_update, delta))
            if delta > max_timeout:
                # Data file
                error_email_sent_time_data_dump = 'registered_cron_scripts.error_email_sent_time.%s.p'%(script)
                now = datetime.datetime.now()
                error_email_sent_time = now
                if isfile(error_email_sent_time_data_dump):
                    error_email_sent_time = pickle.load(open(error_email_sent_time_data_dump, 'rb'))
                if (now - error_email_sent_time).total_seconds() > 60*60:
                    pickle.dump(datetime.datetime.now(), open(error_email_sent_time_data_dump, 'wb'))
                    mail_to = '7185645054@txt.att.net'
                    mail_subject = 'script [%s] last update[%s] late by [%s] seconds'%(script, last_time_update, delta)
                    if __debug__:
                        print('Sending email to [%s] : [%s]'%(mail_to, mail_subject))
                    mailx.send_email(to='7185645054@txt.att.net', subject='Script [%s] has not run'%(script))

        # forcing Manager to update and synchronize across proxies
        time.sleep(10)

########################################################################
# Create the process that will keep monitoring scripts and updates
action_process = Process(target=validate_cron_entries_updates, args=(global_dict,))
if __debug__:
    print('Starting monitoring thread')
if action_process.is_alive()==False:
    try:
        action_process.start()
    except:
        print('ERROR: Could not start cron_entries_updater action_process thread')

if __name__ == '__main__':
    api.run()

