# libraries to be imported
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import argparse, sys
from time import sleep


parser = argparse.ArgumentParser(description='Requests.')
parser.add_argument('--module', help='[1] send files\n[2] Configure Sender Profile')


args = parser.parse_args()

def configure():
    import json

    email = input("E-mail: ")
    password = input("Password: ")
    smtp_server = input("SMTP SERVER: ")
    smtp_port = input("SMTP PORT: ")

    dic = {
        'email': f'{email}',
        'password': f'{password}',
        'smtp_server': f'{smtp_server}',
        'smtp_port': f'{int(smtp_port)}'
    }

    # Serializing json
    json_object = json.dumps(dic, indent=4)

    # Writing to sample.json
    with open("conf/send_profile.json", "w") as outfile:
        outfile.write(json_object)



def sender(sender_toaddr,file_name, file_attach):
    sender_data = open("conf/send_profile.json", 'r')
    sender_profile = json.load(sender_data)

    fromaddr = sender_profile['email']
    try:
        # instance of MIMEMultipart
        msg = MIMEMultipart()

        # storing the senders email address
        msg['From'] = fromaddr

        # storing the receivers email address
        msg['To'] = sender_toaddr

        # storing the subject
        msg['Subject'] = f'attachment {file_attach}'

        # string to store the body of the mail
        body = f'attachment {file_name}'
        # attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        # open the file to be sent
        filename = file_name
        attachment = open(f"sample/{file_attach}", "rb")

        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form
        p.set_payload((attachment).read())

        # encode into base64
        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # attach the instance 'p' to instance 'msg'
        msg.attach(p)

        # creates SMTP session
        s = smtplib.SMTP(sender_profile['smtp_server'], sender_profile['smtp_port'])

        # start TLS for security
        s.starttls()

        # Authentication
        s.login(fromaddr, sender_profile['password'])

        # Converts the Multipart msg into a string
        text = msg.as_string()

        # sending the mail
        s.sendmail(fromaddr, sender_toaddr, text)

        # terminating the session
        s.quit()


    except Exception as e:
        print(e)


def main():
    if not len(sys.argv) > 1:
       print(''' 
       python3 MW_hard.py -h/--help

        --module
            [1] Send  (This Module Run Send Attached File)
            [2] Config  (This Module Config Sender Profile)
            
       ''')

    elif args.module == '1':
        print('[+] Send E-mail Test')
        email_from = input("Digite o Remetete: ")

        file_list = ['sample.vbs', 'sample.js', 'sample.txt', 'sample_macro.docm', 'sample_reverse_shell.pdf',
                     'sample_macro.xlsm', 'sample.rar', 'sample_password.rar', 'sample_password.zip','38bd5894a8e1c294b4ea9f3809a1bb7d987af8db390063603c2fca96df2a77bf.vbs','sample.docx.js']

        for file_attach in file_list:
            sender(f'{email_from}', f'{file_attach}', f'{file_attach}')
            print(f'Sender File {file_attach}')

        print('[+] Finish.......')

    elif args.module == '2':
        configure()
        print('[+] Finish.......')

main()