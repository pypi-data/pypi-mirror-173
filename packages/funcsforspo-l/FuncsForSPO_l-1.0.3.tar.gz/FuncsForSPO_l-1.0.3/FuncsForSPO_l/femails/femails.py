from pathlib import Path
from FuncsForSPO_l.fregex.functions_re import *
from FuncsForSPO_l.fpython.functions_for_py import *
from pretty_html_table import build_table

from email import encoders
from email.mime.base import MIMEBase
import os
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from FuncsForSPO_l.fpython.functions_for_py import *
from FuncsForSPO_l.fregex.functions_re import extrair_email
import smtplib

    
    
def envia_email_gmail(
    email_app_google: str,
    passwd_app_gmail: str,
    emails_to: str|tuple|list,
    assunto: str,
    body_msg,
    anexos: tuple|list|bool = False,
    prints: bool = False
    ):
    """Função para enviar um e-mail completo no Google Gmail
    
    ### Primeiramente, verifique se o email que enviará está configurado.
    
    Se não, siga o passo-a-passo abaixo para configurar o e-mail.
    ### Passo-a-passo para ativar envio de e-mails no Gmail
    1- Ative a verificação por duas etapas no Gmail: https://myaccount.google.com/signinoptions/two-step-verification
    
    2- Vá para esse link para criar uma senha de app: https://myaccount.google.com/apppasswords
        2a - Selecione App, E-mail
        2b - Selecione dispositivo, Outro (nome personalizado)
        2c - Capture a senha para adicionar na função.
        
    ### Dica para utilização de um body:
        Utilize template:
            file: template.html:
                <!DOCTYPE html>
                <html>
                <body>
                    <p>Olá <strong>$nome_placeholder</strong>, hoje é <strong>$data_placeholder</strong>.</p>
                </body>
                </html>
        >>> from string import Template
        >>> with open('template.html', 'r', encoding='utf-8') as html:
        >>>     template = Template(html.read())
        >>>     nome = 'Nome'
        >>>     data_atual = datetime.now().strftime('%d/%m/%Y')
        >>>     body_msg = template.substitute(nome_placeholder=nome, data_placeholder=data_atual)


    Args:
        email_app_google (str): E-mail que enviará para os destinatários, (emails_to)
        passwd_app_gmail (str): Passwd do E-mail que enviará para os destinatários, (emails_to)
        emails_to (str|tuple|list): Destinatário(s)
        assunto (str): Assunto do E-mail
        body_msg (str): Corpo do E-mail
        anexos (tuple | list | bool): Anexos, optional, default = False
        prints (bool): Mostra as eventuais saídas, como por exemplo a recuperação dos anexos e falando que o e-mail foi enviado
    """

    msg = MIMEMultipart()

    # para quem está indo a msg
    # 'gabriel.souza.paycon@gmail.com;gablop6543@gmail.com'
    if isinstance(emails_to, str):
        emails_to = extrair_email(emails_to)
        if len(emails_to) == 0:
            print(f'Não foi possível compreender o e-mail enviado: {emails_to}')
            return
    emails_to = ';'.join(emails_to)
    msg['to'] = emails_to

    # assunto
    msg['subject'] = assunto

    # corpo
    body = MIMEText(body_msg, 'html')
    msg.attach(body)

    # insere_os_anexos
    if isinstance(anexos, (tuple, list)):
        for anexo in anexos:
            anexo_abspath = os.path.abspath(anexo)
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(anexo_abspath, "rb").read())
            encoders.encode_base64(part)
            try:
                file_name = anexo_abspath.split("\\")[-1]
            except Exception:
                file_name = anexo_abspath.split("/")[-1]
                
            print(f'Recuperando anexo: {file_name}')
            part.add_header(f'Content-Disposition', f'attachment; filename={file_name}')
            msg.attach(part)
    elif isinstance(anexos, str):
        anexo_abspath = os.path.abspath(anexos)
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(anexo_abspath, "rb").read())
        encoders.encode_base64(part)
        try:
            file_name = anexo_abspath.split("\\")[-1]
        except Exception:
            file_name = anexo_abspath.split("/")[-1]
        print(f'Recuperando anexo: {file_name}')
        part.add_header('Content-Disposition', f'attachment; filename={file_name}')
        msg.attach(part)

    # abre conexao com smtp
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        try:
            smtp.login(email_app_google, passwd_app_gmail)
        except smtplib.SMTPAuthenticationError as e:
            print(f'E-mail não enviado:\n\tUsuário ou senha inválido!\n\n{e.smtp_error}')
            return
        smtp.send_message(msg)
        print('E-mail enviado com sucesso!')
        
        
def enviar_email_outlook_redmail(usname, passwd, to: list|str, assunto: str='Assunto do E-mail', body: str='<p>Olá!</p>', anexos :dict[str, str]=False, enviar_dataframe_no_corpo: list|tuple|bool=False) -> None:
    """Função para enviar um e-mail no Outlook
    
    Args:
        usname (str): E-mail do seu Outlook
        passwd (str): Passwd do seu Outlook
        to (str|tuple|list): Destinatário(s)
        assunto (str): Assunto do E-mail
        body (str): Corpo do E-mail (DEVE SER HTML)
        anexos (dict): Anexos, se não enviado, será sem anexos
        enviar_dataframe_no_corpo (tuple|list): Mostra as eventuais saídas, como por exemplo a recuperação dos anexos e falando que o e-mail foi enviado, se não enviado, não será adicionado, -> (df, 'yellow_light')

    Use:
        >>> df = pd.DataFrame(
        >>>     {
        >>>         'c1': ['data1', 'data2', 'data3', 'data4'],
        >>>         'c2': ['data1', 'data2', 'data3', 'data4'],
        >>>         'c3': ['data1', 'data2', 'data3', 'data4'],
        >>>         'c4': ['data1', 'data2', 'data3', 'data4'],
        >>>     }
        >>> )
        >>> 
        >>> body = "<html><body><h1>TESTE</h1></body></html>"
        >>> 
        >>> anexos = {
        >>>     # file_name_email:      path_file -> Path from pathlib    
        >>>    'minha_tabela.xlsx': Path(r'my_dirtabela.xlsx'),
        >>>    'meu_relatorio.docx': Path(r'relatório.docx'),
        >>>}
        >>>
        >>> enviar_email_outlook_redmail(
        >>>     'myoutlook@outlook.com',
        >>>     'mypasswdoutlook',
        >>>     ['target1@outlook.com', 'target2@gmail.co'],
        >>>     'Assunto do E-mail',
        >>>     body,
        >>>     anexos,
        >>>     (df, 'yellow_light')
        >>>     )
    """
    
    from redmail import outlook
    from pretty_html_table import build_table

    try:
        outlook.username = usname
        outlook.password = passwd
    except:
        print('Erro no login...')
        
    if isinstance(enviar_dataframe_no_corpo, list) or isinstance(enviar_dataframe_no_corpo, tuple):
        html_table = build_table(*enviar_dataframe_no_corpo)
        body = f"""{body}
        {html_table}"""
    
    if isinstance(anexos, dict):
        outlook.send(
        receivers=to,
        subject=assunto,
        html=body,
        attachments=anexos
        )
    else:
        outlook.send(
            receivers=to,
            subject=assunto,
            html=body,
        )

    
    print('E-mail enviado com sucesso!')