import os
 
class NoSubjectError(Exception):
    pass
 
class NoRecipientError(Exception):
    pass
 
def send_email(to='', subject='', body=''):
    '''
    send_email(to='7185645054@txt.att.net', subject='subject with no body')
    send_email(to='7185645054@txt.att.net', subject='subject', body='this is the body of the email')
    '''
    if not subject:
        raise NoSubjectError
    if not to:
        raise NoRecipientError
    if not body:
        cmd = '''mailx -s '{s}' < /dev/null '{to}' 2>/dev/null'''.format(s=subject, to=to)
    else:
        cmd = '''echo '{b}' | mailx -s '{s}' '{to}' 2>/dev/null'''.format(b=body, s=subject, to=to)
    os.system(cmd)
