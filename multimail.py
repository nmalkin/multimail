#!/usr/bin/env python

import csv
import getopt
import os
import sys
from ConfigParser import ConfigParser
from tempfile import NamedTemporaryFile

# Defaults
VERBOSE = True
CONFIG_SECTION = 'common'
DEFAULT_CONFIG_FILE = 'batch.cfg'
DEFAULT_RECIPIENTS_FILE = 'recipients.csv'
DEFAULT_MESSAGE_FILE = 'message.txt'

# Commands
CMD = 'mutt -s "%(subject)s" %(extras)s -- "%(recipient)s" < "%(message-file)s"'
CC = '-c "%(cc)s" '
BCC = '-b "%(bcc)s" '
ATTACH = '-a %(attachment)s '

def log(message):
    """ Prints given message if VERBOSE is set to True.
    """
    if VERBOSE:
        print(message)

def get_message(filename):
    """ Reads the given filename and returns its contents as a string.
    """

    f = open(filename, 'r')
    message = ''.join(f.readlines())
    f.close()
    return message

def personalize_message(message, personalizations):
    """ Returns a copy of the message with placholders replaced with personalizations.
        Placeholders take the form <0>, <1>, <2>, ...
        Personalizations are given as a list of strings.
    """

    for i in range(len(personalizations)):
        placeholder = '<' + str(i) + '>' # e.g., <1>
        message = message.replace(placeholder, personalizations[i])
    return message

def get_options(filename):
    """ Parses config file for subject, cc, bcc, attachment,
        returns these as a 4-tuple, in that order.
    """

    config = ConfigParser()
    config.read(filename)

    # Get the options. They're all in the 'common' section.
    subject = config.get(CONFIG_SECTION, 'subject')
    cc = config.get(CONFIG_SECTION, 'cc')
    bcc = config.get(CONFIG_SECTION, 'bcc')
    attachment = config.get(CONFIG_SECTION, 'attachment')

    return (subject, cc, bcc, attachment)

def get_personalizations(filename):
    """ Reads a CSV file with addresses and personalizations.
        The first column is the recipient's address;
        the remaining columns are the personalizations.
        This function returns a list of tuples (recipient, [personalizations]).
    """
    
    personalizations = []
    reader = csv.reader(open(filename, 'r'))
    for row in reader:
        personalizations.append(row)
    return personalizations

def send_message(message, subject, recipient, cc='', bcc='', attachment=''):
    """ Sends message with given options.
    """

    log('Sending message to: %s' % recipient)

    tmp = NamedTemporaryFile('w')
    tmp.write(message)
    tmp.flush()

    extras = ''
    if cc != '':
        extras += CC % {'cc': cc}
    if bcc != '':
        extras += BCC % {'bcc': bcc}
    if attachment != '':
        extras += ATTACH % {'attachment': attachment}

    run = CMD % \
            {'subject'      : subject, \
             'extras'       : extras, \
             'recipient'    : recipient, \
             'message-file' : tmp.name}
    os.system(run)

    tmp.close()

def multimail(config_filename, personalization_filename, message_filename):
    message = get_message(message_filename)
    personalizations = get_personalizations(personalization_filename)
    (subject, cc, bcc, attachment) = get_options(config_filename)

    for recipient in personalizations:
        # The first column for each recipient is the email address.
        address = recipient[0]

        # Personalize message
        personalized_message = personalize_message(message, recipient)

        # The same pattern matching is applied to the attachment.
        if attachment != '':
            attachment = personalize_message(attachment, personalizations)

        # Send the message!
        send_message(personalized_message, subject, address, cc, bcc, attachment)
        
def main():
    config_file = DEFAULT_CONFIG_FILE
    recipients_file = DEFAULT_RECIPIENTS_FILE
    message_file = DEFAULT_MESSAGE_FILE

    # Read command-line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:r:m:s', ['config=', 'recipients=', 'message=', 'silent'])
    except getopt.GetoptError, err:
        print(str(err))
    for opt, val in opts:
        if opt in ('-c', '--config'):
            config_file = val
        elif opt in ('-r', '--recipients'):
            recipients_file = val
        elif opt in ('-m', '--message'):
            message_file = val
        elif opt in ('-s', '--silent'):
            VERBOSE = False
            
    multimail(config_file, recipients_file, message_file)

if __name__=="__main__":
    main()
