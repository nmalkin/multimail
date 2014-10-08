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

- a message file
- a recipients file
- a configuration file

Examples of each type of file are located in the `example` directory.

#### Message file ####
The message file contains the body of your message as plain-text. For portions
of the text that you want to customize, insert a placeholder of the form <?>
where the ? is the number of the item to substitute in (start the numbering at 1).

For example:

    Hello, <1>. Are we still on for <2>?

If you want to include the recipient's email address, use the placeholder `<0>`.

#### Recipients file ####
The recipients file contains the addresses of the recipients and
recipient-specific information. Fields are separated by commas, and each line
denotes a new recipient. The first column must contain the recipient's email
address.

For example:

    alice@example.com,Alice,"dinner on Monday"
    bob@example.com,Bob,"lunch on Tuesday"

Note that strings containing spaces must be enclosed in quotes. (The quotes 
won't be part of the message sent.) There is currently no support for newlines.

#### Configuration file ####
The configuration file contains the subject and, optionally, the CC, BCC, and
attachment filename for the messages you want to send.

It follows the following format:

    [common]
    subject: your subject here
    cc: email@example.com
    bcc: email@example.com
    attachment: picture.jpg

A field need not be filled out, but its label must appear.
(e.g., you can have the attachment field be empty,
but you still need the `attachment:` label)

Speaking of attachments,
__the attachment field supports the same placeholders as the message__.
So if you want user-specific attachments, just use a placeholder in the
configuration file and put the filename (or portion of it) in the respective
column of the recipients file.


### How to send ###
To send a batch of message, create the files described above and run the script.

    ./multimail.py

By default, the script will look for files with the following names
in the current directory:

- configuration file: batch.cfg
- recipients file: recipients.csv
- message file: message.txt

Any of these can be changed by running the script with the following flags: 

- configuration file: `-c/--config`
- recipients file: `-r/--recipients`
- message file: `-m/--message`

If you want to suppress any output from the script, you can run with the
`-s/--silent` flag.


[Mutt]: http://www.mutt.org/
