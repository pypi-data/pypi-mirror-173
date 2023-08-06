import string
import warnings
import random
import hashlib
from .error import *
from .letters import *
from .words import words
from .helpers import force_bytes
class Digest:
    def __init__(self,parent,hash_object):
        self.digest=None
        self.hexdigest=None
        self.parent=parent
        self.hash_object=hash_object
        if hasattr(hash_object,'digest'):
            self.digest=hash_object.digest()
        if hasattr(hash_object,'hexdigest'):
            self.hexdigest=hash_object.hexdigest()
    def __repr__(self):
        return f'<Digest for {self.parent} with hash object {self.hash_object}>'

class Hash:
    def __init__(self,hash_object):
        self.hash_object=hash_object
        self.digest=Digest(self,hash_object)
        self.hexdigest=self.digest.hexdigest
        self.bytesdigest=self.digest.digest
    def __repr__(self):
        return f'<Hash with hexdigest {self.digest.hexdigest}>'
class Password:
    def __init__(self,password=None,hashing_method=hashlib.md5,**kwargs):
        self.hashing_method = get_hashing_method(hashing_method)
        self.password=password
        if password is None:
            self.password=randpass(**kwargs).password
        try:
            self.bytes_password=force_bytes(self.password)
        except TypeError:
            raise TypeError("passwords can only be initialized from bytes or str")
    def hash(self,hashing_method=None):
        if hashing_method is None:
            hashing_method = self.hashing_method
        else:
            hashing_method = get_hashing_method(hashing_method)
        return Hash(hashing_method(self.bytes_password))
    def __repr__(self):
        return f'<Password {self.password!r}>'
class Method:
    def __init__(self,m):
        if callable(m):
            self.function=m
        else:
            self.function=METHODS[m]
    def __call__(self,*args,**kwargs):
        return self.function(*args,**kwargs)
def generating_method(fun):
    def decorator(*args,**kwargs):

        number_suffix=kwargs.get('number_suffix',0)
        if 'number_suffix' in kwargs:
            del kwargs['number_suffix']
        hm=kwargs.get('hashing_method',hashlib.md5)
        if 'hashing_method' in kwargs:
            del kwargs['hashing_method']
        number_suffix=Number(number_suffix)
        result=fun(*args,**kwargs)
       
        return Password(result+str(number_suffix),hm)
    return decorator

def _select(min,max=None,step=1):
        if max:
            range_object=range(min,max,step)
        else:
            range_object=range(0,min,step)
        range_object=tuple(range_object)
        return random.choice(range_object)
class Selector:
    def __init__(self,min,max=None,step=1):
        self.min=min
        self.max=max
        self.step=step
    def select(self):
        return _select(self.min,self.max,self.step)
    def __int__(self):
        return self.select()
    def __str__(self):
        return str(self.select())
    
class Number:
    def __init__(self,digitcount=Selector(1,3)):
        self.digitcount=digitcount
    def __repr__(self):
        return repr(self.number)
    @property
    def number(self,final_type=int):
        num=[]
        for q in range(int(self.digitcount)):
            num.append(str(Selector(10)))
        num_string=''.join(num)
        try:
            return final_type(num_string)
        except:
            return num_string
    def __int__(self):
        return self.number
    def __str__(self):
        return str(self.number)
class PasswordGenerator:
    def __init__(self,lowercase=False,uppercase=False,digits=False,symbols=False,all=False,**_):
        self.lowercase=lowercase | all |( not any((uppercase,digits,symbols)))
        self.uppercase=uppercase | all
        self.digits=digits | all
        self.symbols=symbols | all        
        self.choose_from=[]
        if any([self.lowercase,self.uppercase,self.digits,self.symbols]):
            if self.lowercase:
                self.choose_from.extend(string.ascii_lowercase)
            if self.uppercase:
                self.choose_from.extend(string.ascii_uppercase)
            if self.digits:
                self.choose_from.extend(string.digits)
            if self.symbols:
                self.choose_from.extend(string.punctuation)
        else:
            warnings.warn(CategoryWarning('no categories selected. All passwords will be ""'))
        self.passgen=self.generate

    @generating_method
    def generate(self,length=None,min=6,max=20):
        if length is None:
            length=Selector(min,max)
        length=int(length)
        passw=''.join(random.choices(self.choose_from,k=length))
        return passw

    @generating_method
    def pronounceable(self,length=None,min=6,max=20):
        if length is None:
            length=_select(min,max)
        passw=[]
        letters=[consonants,vowels]
        random.shuffle(letters)
        for q in range(length):
            passw.append(random.choice(letters[q%2]))
        return ''.join(passw)
    @generating_method
    def word(self):
        return random.choice(words)
def get_hashing_method(hashing_method):
    if isinstance(hashing_method,str):
        if hashing_method in hashlib.algorithms_guaranteed:
            return getattr(hashlib,hashing_method)
        raise KeyError("Unknown hashing method: {!r}".format(hashing_method))
    if not callable(hashing_method):
        raise TypeError("'hashing_method' must be string or callable")
    return hashing_method
def chars(length=None,min=6,max=20,number_suffix=0,pronounceable=False,**kwargs):
    if pronounceable:
        return _pronounceable(length,min,max,numbezr_suffix,**kwargs)
    return PasswordGenerator(**kwargs).passgen(length,min,max,number_suffix=number_suffix)
def word(number_suffix=0,**kwargs):
    return PasswordGenerator(**kwargs).word(number_suffix=number_suffix)
def _pronounceable(length=None,min=6,max=20,number_suffix=0,**kwargs):
    return PasswordGenerator(**kwargs).pronounceable(length,min,max,number_suffix=number_suffix)
def randpass(method=None,**kwargs):
    
    if method is None:
        method=random.choice([chars,word,_pronounceable])
        if method==word:
            try:
                del kwargs['min']
            except:pass
            try:
                del kwargs['max']
            except:pass
            try:
                del kwargs['length']
            except:pass
    else:
        method=Method(method)
    return method(**kwargs)
def passgen(method=chars,**kwargs):
    if isinstance(method,str):
        if method not in METHODS:
            raise KeyError("Invalid method. Available methods are listed in the docs.")
        method=METHODS[method]
    if not callable(method):
        raise TypeError("{!r} must be a string or callable".format('method'))
    return method(**kwargs)
METHODS={'chars':chars,'characters':chars,'c':chars,'word':word,'w':word,'pronounceable':_pronounceable,'p':_pronounceable}
