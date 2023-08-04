#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Send mail from python
"""
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import click
import requests
name=__name__
del __name__
# dummy class
class Server(str): pass
class Port(int):
  class PortOutOfRangeError(ValueError): pass
  def __init__(self, port: int):
    if port <= 0 or port >= 65535:
      raise self.PortOutOfRangeError(f"Port {port} is not in range of 0-65535 (inclusive)")

@click.command()
@click.option('--argument', callback=get_default_value)
@click.option('--arg2', is_flag=True)
def my_command(argument, arg2):
    click.echo(f"Argument: {argument}")

if __name__ == '__main__':
    my_command()

@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option('--smtp-server', '-s', type=Server, required=True, help="SMTP Server to connenvt to. e.g. smtp.gmail.com, smtp-mail.outlook.com")
@click.option('--ssl/--tls', is_flag=True, help='Establish SSL or TLS', default=False)
@click.option('--smtp-port', '-p', type=Port, callback=(lambda ctx, param, value: 465 if ctx.params['ssl'] else 587 if value is None else value))

#@click.option('--sender', '', )
def main(smtp_server: str, smtp_port: int, ssl):
  """
  Send mail via SMTP Servers, from python!
  """
  sender = "ekanav@hotmail.com"
  password = "Kanav@123"
  reciever = "email.kanavg@gmail.com"
  message = MIMEMultipart("alternative")
  msg_text = requests.get("https://report3.live.fxinside.net/birt/jsp/reportApi.jsp?type=Volume&groupBy1=OrgLongName&format=html").text

  m1=MIMEText(msg_text, "plain")
  m2=MIMEText(msg_text, "html")

  message.attach(m1)
  message.attach(m2)
  if ssl:
    server = smtplib.SMTP_SSL(smtp_server, port=int(smtp_port))
  else:
    server = smtplib.SMTP(smtp_server, port=int(smtp_port))
    server.starttls()
  server.login(sender, password)
  server.sendmail(sender, reciever, message.as_string())
  server.quit()

if name == "__main__":
  main()