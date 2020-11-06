# File Grep
The finder Help to find the word in the many folder or many files

## Quick Start
```shell=
git clone https://github.com/t0239184/FileGrep
cd FileGrep
python fgrep.py pattern=TODO
```


## Usage
```
args:
  help      print help information.
  pattern   the grep word.
  path      the search path.
  deep      the fold deep level.

example:
    python fgrep pattern=TODO 
    python fgrep path=./ pattern=TODO 
    python fgrep path=./ deep=10 pattern=TODO 
```
