import click
import hashlib
from click_default_group import DefaultGroup
from . import password
from . import clipboard
from .helpers import get_loop
import sys
import builtins
@click.group(cls=DefaultGroup,default='generate',default_if_no_args=True)
def main():
    return 1

@main.command()
@click.option('--type','-t',default='chars',type=click.Choice(password.METHODS),help='generation method to use')
@click.option('--min',default=6,help='Minimal number of characters in password (has no effect if type is word)')
@click.option('--max',default=20,help='Maximal number of characters in password (has no effect if type is word)')
@click.option('--length','-l',default=None,type=int,help='Precise number of characters in password. Overrides --min and --max (has no effect if type is word)')
@click.option('--number-suffix','-s',default=0,help='Length of number suffix')
@click.option('--copy','-c',is_flag=True,help='Use this to copy the generated password to the clipboard')
@click.option('--hash','-h',is_flag=True,help='Print also the password hash')
@click.option('--algorithm','-a',default='md5',type=click.Choice(hashlib.algorithms_guaranteed),help='Hashing algorithm to use with -h. Default MD5. (If -h is not set, has no effect)')
@click.option('--lowercase','-L',is_flag=True,help='If type is chars, adds lowercase ASCII to the generation set. This flag is automatically set if none of -U,-D,-S,-A,-C is set.')
@click.option('--uppercase','-U',is_flag=True,help='If type is chars, adds uppercase ASCII to the generation set')
@click.option('--digits','-D',is_flag=True,help='If type is chars, adds decimal digits to the generation set')
@click.option('--symbols','-S',is_flag=True,help='If type is chars, adds ASCII symbols to the generation set')
@click.option('--all','-A',is_flag=True,help='If type is chars, adds all groups to the generation set')
@click.option('--copy-hash','-C',is_flag=True,help='Use this to copy the generated hash to clipboard. Has no effect if -h is not set.')
@click.option('--number','-n',default=1,help='Number of passwords to generate')
@click.option('--infinite','-i',is_flag=True,help='Constantly generates passwords. Overrides -n.')
def generate(type,min,max,length,number_suffix,copy,hash,algorithm,lowercase,uppercase,digits,symbols,all,copy_hash,number,infinite):
    kwargs={}
    if (copy or copy_hash) and not clipboard.CAN:
              click.secho("Can't use clipboard - no clipboard detected. Are you on a terminal?",err=True,fg='red')
              return 1
    for _ in get_loop(number,infinite):
        if password.METHODS[type] == password.chars:
            if not all|lowercase|uppercase|digits|symbols:
                lowercase=True
            kwargs.update({'lowercase':lowercase,'uppercase':uppercase,'digits':digits,'symbols':symbols,'all':all})
        passwd = password.passgen(type,min=min,max=max,length=length,number_suffix=number_suffix,**kwargs)
        click.echo(passwd.password)
        if hash:
            h =  passwd.hash(algorithm).hexdigest
            click.echo('[{0} HASH]: {1}'.format(algorithm, h))
            if copy:
                  clipboard.copy(h)
        if copy:
            clipboard.copy(passwd.password)
@main.command()
@click.option('--input','-i',default=sys.stdin,type=click.File('r'),help='Input to read from. Default is stdin')
@click.option('--output','-o',default=sys.stdout.buffer,type=click.File('wb'),help='Output to write to. Default is stdout')
@click.option('--algorithm','-a',default='md5',type=click.Choice(hashlib.algorithms_guaranteed),help='Hashing algorithm to use. Default MD5')
@click.option('--bytes-digest','-b',is_flag=True,help='Output normal digest instead of hexdigest.')
@click.option('--repr','-r',is_flag=True,help='If -b is set, outputs Python internal string representation of bytes output')
def hash(input,output,algorithm,bytes_digest,repr):
    for passwd in input:
        p = password.Password(passwd)
        if not bytes_digest:
            output.write(p.hash(algorithm).hexdigest.encode('ascii'))
            output.write(b'\n')
        else:
            if repr:
                output.write(builtins.repr(p.hash(algorithm).bytesdigest).encode())
                output.write(b'\n')
            else:
                output.write(p.hash(algorithm).bytesdigest)
        output.flush()

