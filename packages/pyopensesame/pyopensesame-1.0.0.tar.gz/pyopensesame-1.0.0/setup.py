import setuptools
setuptools.setup(name="pyopensesame",
                 version="1.0.0",
                 description="Advanced password generator and hasher",
                 long_description="""
# opensesame
Advanced password generator and hasher made in Python.
# Installation
## From PyPI(any OS)
```bash
python3 -m pip install opensesame
```
## Directly from GitHub(Linux only)
```bash
git clone "https://github.com/jenca-adam/opensesame/" opensesame_build
cd opensesame_build
./setup.sh
cd ..
rm -rf opensesame_build
```
You can also use `sudo python3 setup.py install`, but `setup.sh` allows local installation.
# CLI
`opensesame` CLI supports two commands:<br>
1.`generate` for generating passwords(default)

```bash
Usage: python -m opensesame generate [OPTIONS]

Options:
  -t, --type [chars|characters|c|word|w|pronounceable|p]
                                  generation method to use
  --min INTEGER                   Minimal number of characters in password
                                  (has no effect if type is word)
  --max INTEGER                   Maximal number of characters in password
                                  (has no effect if type is word)
  -l, --length INTEGER            Precise number of characters in password.
                                  Overrides --min and --max (has no effect if
                                  type is word)
  -s, --number-suffix INTEGER     Length of number suffix
  -c, --copy                      Use this to copy the generated password to
                                  the clipboard
  -h, --hash                      Print also the password hash
  -a, --algorithm [sha3_384|sha512|blake2b|sha1|sha224|sha3_512|sha256|shake_256|md5|sha384|shake_128|sha3_256|sha3_224|blake2s]
                                  Hashing algorithm to use with -h. Default
                                  MD5. (If -h is not set, has no effect)
  -L, --lowercase                 If type is chars, adds lowercase ASCII to
                                  the generation set. This flag is
                                  automatically set if none of -U,-D,-S,-A,-C
                                  is set.
  -U, --uppercase                 If type is chars, adds uppercase ASCII to
                                  the generation set
  -D, --digits                    If type is chars, adds decimal digits to the
                                  generation set
  -S, --symbols                   If type is chars, adds ASCII symbols to the
                                  generation set
  -A, --all                       If type is chars, adds all groups to the
                                  generation set
  -C, --copy-hash                 Use this to copy the generated hash to
                                  clipboard. Has no effect if -h is not set.
  -n, --number INTEGER            Number of passwords to generate
  -i, --infinite                  Constantly generates passwords. Overrides
                                  -n.
  --help                          Show this message and exit.
```

2.`hash` for hashing passwords.<br>
```bash
Usage: python -m opensesame hash [OPTIONS]

Options:
  -i, --input FILENAME            Input to read from. Default is stdin
  -o, --output FILENAME           Output to write to. Default is stdout
  -a, --algorithm [sha224|blake2b|sha3_384|sha384|blake2s|sha1|shake_128|sha3_224|sha512|sha3_256|sha3_512|sha256|md5|shake_256]
                                  Hashing algorithm to use. Default MD5
  -b, --bytes-digest              Output normal digest instead of hexdigest.
  -r, --repr                      If -b is set, outputs Python internal string
                                  representation of bytes output
  --help                          Show this message and exit.
```
# Python lib
## Generation methods
# opensesame
Advanced password generator and hasher made in Python.
# Installation
## From PyPI(any OS)
```bash
python3 -m pip install opensesame
```
## Directly from GitHub(Linux only)
```bash
git clone "https://github.com/jenca-adam/opensesame/" opensesame_build
cd opensesame_build
./setup.sh
cd ..
rm -rf opensesame_build
```
You can also use `sudo python3 setup.py install`, but `setup.sh` allows local installation.
# CLI
`opensesame` CLI supports two commands:<br>
1.`generate` for generating passwords(default)

```bash
Usage: python -m opensesame generate [OPTIONS]

Options:
  -t, --type [chars|characters|c|word|w|pronounceable|p]
                                  generation method to use
  --min INTEGER                   Minimal number of characters in password
                                  (has no effect if type is word)
  --max INTEGER                   Maximal number of characters in password
                                  (has no effect if type is word)
  -l, --length INTEGER            Precise number of characters in password.
                                  Overrides --min and --max (has no effect if
                                  type is word)
  -s, --number-suffix INTEGER     Length of number suffix
  -c, --copy                      Use this to copy the generated password to
                                  the clipboard
  -h, --hash                      Print also the password hash
  -a, --algorithm [sha3_384|sha512|blake2b|sha1|sha224|sha3_512|sha256|shake_256|md5|sha384|shake_128|sha3_256|sha3_224|blake2s]
                                  Hashing algorithm to use with -h. Default
                                  MD5. (If -h is not set, has no effect)
  -L, --lowercase                 If type is chars, adds lowercase ASCII to
                                  the generation set. This flag is
                                  automatically set if none of -U,-D,-S,-A,-C
                                  is set.
  -U, --uppercase                 If type is chars, adds uppercase ASCII to
                                  the generation set
  -D, --digits                    If type is chars, adds decimal digits to the
                                  generation set
  -S, --symbols                   If type is chars, adds ASCII symbols to the
                                  generation set
  -A, --all                       If type is chars, adds all groups to the
                                  generation set
  -C, --copy-hash                 Use this to copy the generated hash to
                                  clipboard. Has no effect if -h is not set.
  -n, --number INTEGER            Number of passwords to generate
  -i, --infinite                  Constantly generates passwords. Overrides
                                  -n.
  --help                          Show this message and exit.
```

2.`hash` for hashing passwords.<br>
```bash
Usage: python -m opensesame hash [OPTIONS]

Options:
  -i, --input FILENAME            Input to read from. Default is stdin
  -o, --output FILENAME           Output to write to. Default is stdout
  -a, --algorithm [sha224|blake2b|sha3_384|sha384|blake2s|sha1|shake_128|sha3_224|sha512|sha3_256|sha3_512|sha256|md5|shake_256]
                                  Hashing algorithm to use. Default MD5
  -b, --bytes-digest              Output normal digest instead of hexdigest.
  -r, --repr                      If -b is set, outputs Python internal string
                                  representation of bytes output
  --help                          Show this message and exit.
```
# Python lib
## Generation methods
### chars
This generates a password of a given length randomly selecting from the given character sets. Character sets are: 

* `lowercase` -> lower case ascii chars
* `uppercase` -> UPPER CASE ASCII CHARS
* `digits` -> 0123456789
* `symbols` -> *!"#$%&\'()+,\*-./:;<=>?@[\\]^_`{|}~*
* `all` -> everything above
Character sets are added by setting kwarg `<CHARSET_NAME>` to `True`.
If no character sets are specified, only lowercase is used.

You can specify length using `length`,`min` and `max` atributtes, where `length` overrides the boundaries(`min` and `max`).
Default length is picked between 6 and 20.
> :warning: Be careful! Don't select only one boundary, as it might cause `IndexError`.

You can also generate a pronounciable password by setting `pronounciable` to `True`.
Character sets don't apply to pronounciable passwords.
### word
This just selects a random word from the wordlist.
No attributes from `chars` apply to this.
### passgen
With `passgen`,you can select a method and call the method with given `**kwargs`. <br>
It's just a wrapper. <br>
The methods are selected by setting the first arg of `passgen` to `chars`,`word` or `pronounciable`. You can also set it to the first char of their name. 
## `number_suffix`
`chars`,`word` and `passgen` all have the argument `number_suffix`. It specifies how many digits are supposed to be added to the end of the password.
## `Password` object
Generation methods return this.<br>
It's a string wrapped in hashing.
Hashing is done with  `Password.hash(algorithm)`.
`Password.hash` returns `Hash` object with attributes `hexdigest`(hexadecimal representation of the digest) and `bytesdigest`(actual digest)


### chars
This generates a password of a given length randomly selecting from the given character sets. Character sets are: 

* `lowercase` -> lower case ascii chars
* `uppercase` -> UPPER CASE ASCII CHARS
* `digits` -> 0123456789
* `symbols` -> *!"#$%&\'()+,\*-./:;<=>?@[\\]^_`{|}~*
* `all` -> everything above
Character sets are added by setting kwarg `<CHARSET_NAME>` to `True`.
If no character sets are specified, only lowercase is used.

You can specify length using `length`,`min` and `max` atributtes, where `length` overrides the boundaries(`min` and `max`).
Default length is picked between 6 and 20.
> :warning: Be careful! Don't select only one boundary, as it might cause `IndexError`.

You can also generate a pronounciable password by setting `pronounciable` to `True`.
Character sets don't apply to pronounciable passwords.
### word
This just selects a random word from the wordlist.
No attributes from `chars` apply to this.
### passgen
With `passgen`,you can select a method and call the method with given `**kwargs`. <br>
It's just a wrapper. <br>
The methods are selected by setting the first arg of `passgen` to `chars`,`word` or `pronounciable`. You can also set it to the first char of their name. 
## `number_suffix`
`chars`,`word` and `passgen` all have the argument `number_suffix`. It specifies how many digits are supposed to be added to the end of the password.
## `Password` object
Generation methods return this.<br>
It's a string wrapped in hashing.
Hashing is done with  `Password.hash(algorithm)`.
`Password.hash` returns `Hash` object with attributes `hexdigest`(hexadecimal representation of the digest) and `bytesdigest`(actual digest)
""",
    long_description_content_type='text/markdown',
    packages=['opensesame'],
    package_data={"opensesame":["list.txt"]},
    include_package_data=True,
    entry_points={"console_scripts":["opensesame = opensesame.main_click:main"]},
    author="Adam Jenca",
    classifiers=[ "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
                 "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                 ],
    author_email="jenca.a@gjh.sk",
    project_urls={
            "GitHub":"https://github.com/jenca-adam/opensesame/"
            }
)

