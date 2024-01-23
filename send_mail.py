O=False
N='plain'
M=tuple
I='text'
F=int
E=str
D=True
C='smtp_server'
B=None
from email.mime.nonmultipart import MIMENonMultipart as J
from email.mime.multipart import MIMEMultipart as P
import smtplib as K,click as A,socket as G
class L(J):
	def __init__(C,_text,_maintype=I,_subtype=N,_charset=B,*,policy=B):
		F='us-ascii';D=_text;A=_charset
		if A is B:
			try:D.encode(F);A=F
			except UnicodeEncodeError:A='utf-8'
		J.__init__(C,_maintype,_subtype,policy=policy,**{'charset':E(A)});C.set_payload(D,A)
class H(A.Option):
	def __init__(A,*E,**C):A.save_other_options=C.pop('save_other_options',D);F=C.pop('nargs',-1);super(H,A).__init__(*E,**C);A._previous_parser_process=B;A._eat_all_parser=B
	def add_to_parser(A,parser,ctx):
		F=parser
		def J(value,state):
			C=state;B=value;G=O;B=[B]
			if A.save_other_options:
				while C.rargs and not G:
					for K in A._eat_all_parser.prefixes:
						if C.rargs[0].startswith(K):G=D
						if not G:B.append(C.rargs.pop(0))
					else:B+=C.rargs;C.rargs[:]=[]
				B=M(B);A._previous_parser_process(B,C)
			L=super(H,A).add_to_parser(F,ctx)
			for I in A.opts:
				E=F._long_opt.get(I)or F._short_opt.get(I)
				if E:A._eat_all_parser=E;A._previous_parser_process=E.process;E.process=J;break
			return L
class Q(F):
	class PortOutOfRangeError(ValueError):0
	def __init__(B,port):
		A=port;A=F(A)
		if A<=0 or A>=65535:raise B.PortOutOfRangeError(f"Port {A} is not in range of 0-65535 (inclusive)")
@A.command(context_settings=dict(help_option_names=['-h','--help']))
@A.option('--smtp-server','-s',metavar='SERVER',help='SMTP Server to connect to. e.g. smtp.gmail.com, smtp-mail.outlook.com',callback=lambda ctx,param,value:A.prompt('Enter SMTP Server to connect to')if value is B else value)
@A.option('--ssl/--tls',is_flag=D,help='Establish SSL or TLS',default=O)
@A.option('--smtp-port','-p',type=Q,metavar='PORT',callback=lambda ctx,param,value:(465 if ctx.params['ssl']else 587)if value is B else value)
@A.option('--email','-e',type=E,metavar='EMAIL',callback=lambda ctx,param,value:A.prompt(f"Enter email for {ctx.params[C]} ({G.gethostbyname(ctx.params[C])})")if value is B else value)
@A.option('-p','--password',type=E,metavar='PASSWORD',help='Password for SMTP Server',callback=lambda ctx,param,value:A.prompt(f"Enter your password for {ctx.params[C]} ({G.gethostbyname(ctx.params[C])})",hide_input=D,confirmation_prompt=f"Confirm Your password for {ctx.params[C]} ({G.gethostbyname(ctx.params[C])})")if value is B else value)
@A.option('-r','--recievers',type=M,metavar='RECIEVERS',help='Who should recieve your email?',cls=H,multiple=D,callback=lambda ctx,param,value:A.prompt("Recievers (seperate with ', ')",type=E).split(', ')if value==()else value)
def R(smtp_server,smtp_port,ssl,email,password,recievers):
	G=email;E=smtp_port;D=smtp_server;B=recievers;B=B[0]if len(B)==1 else B;C=P('alternative');H='<i>italic</i>';J=L(H,I,N);M=L(H,I,'html');C.attach(J);C.attach(M)
	if ssl:A=K.SMTP_SSL(D,port=F(E));A.starttls()
	else:A=K.SMTP(D,port=F(E));A.starttls()
	A.login(G,password);A.sendmail(G,B,C.as_string());print('Note: If you did not recieve the email, check you spam folder.');A.quit()
if __name__=='__main__':R()
