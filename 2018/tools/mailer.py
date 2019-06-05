#! /usr/bin/env python
#
# Usage:
#     mailer.py template_file subject_line email_file EMAIL,NAME,TITLE
#
#     email_file needs to have the email in 1st column, optional other directives
#     that can be used in ${NAME} type macro expansions
#
#
# alternative ideas:
#     http://naelshiab.com/tutorial-send-email-python/
#     https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/
#     https://medium.freecodecamp.org/send-emails-using-code-4fcea9df63f?gi=61be8b3ff3dd
#     https://arjunkrishnababu96.github.io/Send-Emails-Using-Code/
#


# This needs to be in python3


import os
import sys
from string import Template
import smtplib
import shlex

def get_file(filename):
    """
    read file, return list of lines, but skip comment and blank lines
    """
    out = []
    f = open(filename)
    lines = f.readlines()
    f.close()
    for line in lines:
        if line[0] == '#': continue
        line = line.strip()
        if len(line) == 0: continue
        out.append(line)
    return out

# Function to read the contacts from a given contact file and return a
# list of names and email addresses
def get_contacts(filename):
    ncol = 0
    #with open(filename, mode='r', encoding='utf-8') as contacts_file:
    with open(filename, mode='r') as contacts_file:
        for a_contact in contacts_file:
            if a_contact[0] == '#': continue
            w = shlex.split(a_contact)
            if ncol == 0:
                ncol = len(w)
                print("Found %d columns" % ncol)
                col = []
                for i in range(ncol):
                    col.append([])
            for i in range(ncol):
                col[i].append(w[i])
    return col


def read_template(filename):
    # with open(filename, 'r', encoding='utf-8') as template_file:
    with open(filename, 'r') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)



if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: %s message subject contacts col1,col2,..." % sys.argv[0])
        sys.exit(1)
    T_message = read_template(sys.argv[1])
    T_subject = Template(sys.argv[2])
    cols = get_contacts(sys.argv[3])
    dirs = sys.argv[4].split(',')
    print('cols: ',dirs)

    kwargs={}
    for i in range(len(cols[0])):
        for j in range(len(dirs)):
            kwargs[dirs[j]] = cols[j][i]
            if dirs[j] == 'EMAIL' :
                e1 = cols[j][i]
        s1 = T_subject.substitute(**kwargs)
        # print("s1: ",s1)

        m1 = T_message.substitute(**kwargs)
        # print("m1: ",m1)

        f1 = 'tmp.msg'
        fd1 = open(f1,'w')
        fd1.write(m1)
        fd1.close()

        return_adress = "adass2018@astro.umd.edu"

        cmd = 'mailx -r %s -s "%s" %s < %s' % (return_adress,s1,e1,f1)
        print(cmd)
        os.system(cmd)
