#!/usr/bin/env python3.12
# -*- encoding: utf-8 -*-
'''
***REQUIRES***
Python==3.12
'''
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import click
import validators
import socket

# dummy class
class Server(str): pass
class Port(int):
  class PortOutOfRangeError(ValueError): pass
  def __init__(self, port: int):
    port=int(port)
    if port <= 0 or port >= 65535:
      raise self.PortOutOfRangeError(f'Port {port} is not in range of 0-65535 (inclusive)')

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--smtp-server', '-s', type=Server, required=True, help='SMTP Server to connect to. e.g. smtp.gmail.com, smtp-mail.outlook.com')
@click.option('--ssl/--tls', is_flag=True, help='Establish SSL or TLS', default=False)
@click.option('--smtp-port', '-p', type=Port, callback=lambda ctx, param, value: (465 if ctx.params['ssl'] else 587) if value is None else value)
@click.option('--email', '-e', type=str, callback=lambda ctx, param, value: click.prompt(f'Enter email for {ctx.params["smtp_server"]} ({socket.gethostbyname(ctx.params["smtp_server"])})'))
@click.option('-p', '--password', help='Password for SMTP Server', callback=lambda ctx, param, value: click.prompt(f'Enter your password for {ctx.params["smtp_server"]} ({socket.gethostbyname(ctx.params["smtp_server"])})', hide_input=True, confirmation_prompt=f'Confirm Your password for {ctx.params["smtp_server"]} ({socket.gethostbyname(ctx.params["smtp_server"])})',) if value is None else value)

def main(smtp_server: str, smtp_port: int, ssl: bool, email: str, password: str):
  '''
  Send mail via SMTP Servers, from python!
  '''
  reciever = 'email.kanavg@gmail.com'
  message = MIMEMultipart('alternative')
  msg_text = "<i>italic</i>"

  m1=MIMEText(msg_text, 'plain')
  m2=MIMEText(msg_text, 'html')

  message.attach(m1)
  message.attach(m2)
  if ssl:
    server = smtplib.SMTP_SSL(smtp_server, port=int(smtp_port))
  else:
    server = smtplib.SMTP(smtp_server, port=int(smtp_port))
    server.starttls()
  server.login(email, password)
  server.sendmail(email, reciever, message.as_string())
  server.quit()

if __name__ == '__main__':
  main()