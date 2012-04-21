                        MultiMail
===========================================================
a primitive mail merge for email, using [Mutt][] and Python
-----------------------------------------------------------

### What is it? ###
This is a Python script that helps send batch emails with message bodies
customized for each recipient.


### Prerequisites ###
To run this script, you need:

- [Python](http://python.org/) (tested with 2.7, others may work as well)
- [Mutt][] mail client, configured and working


### How to configure ###
Sending an email requires the existence of three files:

- a configuration file
- a recipients file
- a message file

Examples of each type of file are located in the `example` directory.

#### Configuration file ####
The configuration file contains the subject and, optionally, the CC, BCC, and
attachments for the messages you want to send.

It follows the following format:

    [common]
    subject: your subject here
    cc: email@example.com
    bcc: email@example.com
    attachment: picture.jpg

#### Message file ####
The message file contains the body of your message as plain-text. For portions
of the text that you want to customize, insert a placeholder of the form <?>
where the ? is the number of the item to substitute in (starting at 1). e.g.,

    Hello, <1>. Are we still on for <2>?

If you want to include the recipient's email address, use the placeholder <0>.

#### Recipients file ####
The recipients file contains the addresses of the recipients and recipient-
specific information. Fields are separated by commas, and each line denotes
a new recipient. e.g.,

    Alice,"dinner on Monday"
    Bob,"lunch on Tuesday"

Note that strings containing spaces must be enclosed on quotes. (The quotes 
won't be part of the message sent.) There is currently no support for newlines.


### How to send ###
To send a batch of message, create the files described above and run the script.

    ./multimail.py

By default, the script will look for files with the following names
in the current directory:

- configuration file: batch.cfg
- recipients file: recipients.csv
- message file: message.txt

Any of these can be changed by running the script with the following flags: 

- configuration file: -c/--config
- recipients file: -r/--recipients
- message file: -m/--message

If you want to suppress any output from the script, you can run with the
`-s/--silent` flag.


### TODO ###

- Support for recipient-specific attachments
- You tell me

[Mutt]: http://www.mutt.org/
