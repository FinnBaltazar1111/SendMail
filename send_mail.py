#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import click
import socket

# https://stackoverflow.com/a/48394004/
class OptionEatAll(click.Option):
  def __init__(self, *args, **kwargs):
      self.save_other_options = kwargs.pop('save_other_options', True)
      nargs = kwargs.pop('nargs', -1)
      assert nargs == -1, 'nargs, if set, must be -1 not {}'.format(nargs)
      super(OptionEatAll, self).__init__(*args, **kwargs)
      self._previous_parser_process = None
      self._eat_all_parser = None

  def add_to_parser(self, parser, ctx):
    def parser_process(value, state):
      # method to hook to the parser.process
      done = False
      print(value)
      value = [value]
      print(value)
      if self.save_other_options:
          # grab everything up to the next option
          while state.rargs and not done:
            for prefix in self._eat_all_parser.prefixes:
              if state.rargs[0].startswith(prefix):
                done = True
              if not done:
                value.append(state.rargs.pop(0))
            else:
              # grab everything remaining
              value += state.rargs
              state.rargs[:] = []
          print(value)
          value = tuple(value)

          # call the actual process
          self._previous_parser_process(value, state)

      retval = super(OptionEatAll, self).add_to_parser(parser, ctx)
      for name in self.opts:
        our_parser = parser._long_opt.get(name) or parser._short_opt.get(name)
        if our_parser:
          self._eat_all_parser = our_parser
          self._previous_parser_process = our_parser.process
          our_parser.process = parser_process
          break
      print('dict', retval)
      return retval
class Port(int):
  class PortOutOfRangeError(ValueError): pass
  def __init__(self, port: int):
    port=int(port)
    if port <= 0 or port >= 65535:
      raise self.PortOutOfRangeError(f'Port {port} is not in range of 0-65535 (inclusive)')

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--smtp-server', '-s', metavar="SERVER", help='SMTP Server to connect to. e.g. smtp.gmail.com, smtp-mail.outlook.com', callback = lambda ctx, param, value: click.prompt("Enter SMTP Server to connect to") if value is None else value)
@click.option('--ssl/--tls', is_flag=True, help='Establish SSL or TLS', default=False)
@click.option('--smtp-port', '-p', type=Port, metavar="PORT", callback=lambda ctx, param, value: (465 if ctx.params['ssl'] else 587) if value is None else value)
@click.option('--email', '-e', type=str, metavar="EMAIL", callback=lambda ctx, param, value: click.prompt(f'Enter email for {ctx.params["smtp_server"]} ({socket.gethostbyname(ctx.params["smtp_server"])})') if value is None else value)
@click.option('-p', '--password', type=str, metavar="PASSWORD", help='Password for SMTP Server', callback=lambda ctx, param, value: click.prompt(f'Enter your password for {ctx.params["smtp_server"]} ({socket.gethostbyname(ctx.params["smtp_server"])})', hide_input=True, confirmation_prompt=f'Confirm Your password for {ctx.params["smtp_server"]} ({socket.gethostbyname(ctx.params["smtp_server"])})',) if value is None else value)
@click.option('-r', '--reciever', type=tuple, metavar="RECIEVERS", help="Who should recieve your email?", cls=OptionEatAll, multiple=True, callback=lambda ctx, param, value: click.prompt("Recievers (seperate with ', ')", type=str).split(', ') if value == () else value)

def main(smtp_server: str, smtp_port: int, ssl: bool, email: str, password: str, reciever):
  '''
  Send mail via SMTP Servers, from python!
  '''
  print(reciever[0])
  print(type(reciever[0]))
  reciever=reciever[0][2:-3] if len(reciever)==1 else reciever
  message = MIMEMultipart('alternative')
  msg_text = "<i>italic</i>"

  m1=MIMEText(msg_text, 'plain')
  m2=MIMEText(msg_text, 'html')

  message.attach(m1)
  message.attach(m2)
  if ssl:
    server = smtplib.SMTP_SSL(smtp_server, port=int(smtp_port))
    server.starttls()
  else:
    server = smtplib.SMTP(smtp_server, port=int(smtp_port))
    server.starttls()
  server.login(email, password)
  server.sendmail(email, reciever, message.as_string())
  print("Note: If you did not recieve the email, check you spam folder.")
  server.quit()

if __name__ == '__main__':
  main()