import os
import smtplib
import logging


def configure_log(path):
    logging.basicConfig(filename=path, level=logging.INFO,
                        format='%(levelname)s:%(message)s')
    logging.info('*****SCRIPT RUN*****')


# changes working directory to path
def change_working_dir(path):
    try:
        os.chdir(path)
        logging.info('Directory Changed To : '+path)
    except:
        logging.info('##Directory NOT Changed To : '+path+'##')
        return False


# gets all files at path
def get_files(path):
    count = 0
    latest_files = []
    for folders, subfolders, files in os.walk(path):
        continue
    try:
        logging.info(str(len(files))+' Files Fetched From '+str(path))
        return files
    except:
        logging.info('##0 Files Fetched##')
        return False


# gets two most recent files in files
def get_latest_files(files):
    if len(files) == 0:
        logging.info('##Latest Files Fetched : NONE##')
        return False
    elif len(files) == 1:
        file1 = files[0]
        logging.info('Latest Files Fetched : '+str(file1))
        return file1
    else:
        file1 = files[0]
        file2 = files[0]

    # finds most recent file
    for file in files:
        if os.path.getctime(file) > os.path.getctime(file1):
            file1 = file
    # finds second most recent file
    for file in files:
        if os.path.getctime(file) > os.path.getctime(file2) and os.path.getctime(file1) > os.path.getctime(file):
            file2 = file
    logging.info('Latest Files Fetched : '+str(file1)+' '+str(file2))
    return [file1, file2]


# def merge_file(files):
#     try:
#         with open(files[0], 'r') as file1, open(files[1], 'r') as file2:
#             txt = file1.read()+'\n'+file2.read()
#             logging.info('Files Text Merged')
#             return txt
#     except:
#         logging.info('##Files Text NOT Merged##')
#         return False


# def create_file(text, path, name):
#     try:
#         with open(path+'\\'+name+'.txt', 'a') as f:
#             f.write(text)
#             logging.info('Merged File Created With Merged Text')
#             return name
#     except:
#         logging.info('##Merged File NOT Created With Merged Text##')
#         return False

def create_file(files, s_path, d_path, name):
    try:
        with open(s_path+'\\'+files[0], 'r') as file1, open(s_path+'\\'+files[1], 'r') as file2, open(d_path+'\\'+name+'.txt', 'a') as f:
            for line in file1:
                f.write(line)
            logging.info('file 1 written')
            f.write('\n')
            for line in file2:
                f.write(line)
            logging.info('file 2 written')

            return name
    except:
        logging.info('##merging and creating file falied##')
        return False


def get_next_name(path):
    files = get_files(path)
    try:
        latest_file = get_latest_files(files)
        if type(latest_file) == list:
            latest_file = latest_file[0]
        else:
            pass
        name = 'merged_file'+str(int(latest_file[11:-4])+1)
    except:
        name = 'merged_file1'

    logging.info('File Name Created : '+name)
    return name


# send email about the outcome of the script
def send_email(name='', files='', log=''):
    '''
    for sending emails set the 'EMAIL_ADDRESS', 'EMAIL_PASSWORD','EMAIL_RECIEVER' 
    to your preferences and change the host name in 'smtplib.SMTP_SSL()'
    '''
    EMAIL_ADDRESS = ''
    EMAIL_PASSWORD = ''
    EMAIL_RECIEVER = ''

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        if name:
            subject = 'Files Merged'
            body = ''
            for index in range(0, len(files)):
                body += str(files[index])
                if index != len(files)-1:
                    body += ' and '
            body += ' are merged together as '+str(name)
        else:
            subject = 'Files Not Merged'
            body = log

        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_RECIEVER, msg)
        logging.info('Email Sent')


def get_last_script_log(path):
    with open(path, 'r') as log:
        last_log = log.read().split('*****SCRIPT RUN*****')[len(log.read())-1]
        return last_log


def main():

    source_path = r''
    destination_path = r''
    # log file will be created at log_path
    log_path = r''

    configure_log(log_path)

    change_working_dir(source_path)
    files = get_files(source_path)
    if not files:
        last_log = get_last_script_log(log_path)
        send_email(log=last_log)
        return
    latest_files = get_latest_files(files)
    change_working_dir(destination_path)
    name = create_file(latest_files, source_path, destination_path,
                       get_next_name(destination_path))

    last_log = get_last_script_log(log_path)
    send_email(name, latest_files, last_log)


main()
