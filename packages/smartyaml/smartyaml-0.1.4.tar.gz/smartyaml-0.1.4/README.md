# smartyaml
Library that simplifies defaulting and multi-file yaml config

## Motivation
Ever had to create simple yaml config based off default parameters and variables? I had the inspiration working with Bastille jail config, and hypothesize that the problem applies across multiple use cases. 

## Use cases
### Config
- [x] Simple multifile (parent) support
- [x] Defaulting support (child overrides parent)
- [ ] Export final config to file

### Variables
- [ ] Variable support
- [ ] Defaulting variable support
- [ ] Multile variable support

## Installation
### Pre-install
- Python 3.8 or later
- Pip

### Install
```
pip3 install smartyaml
```

## Implementation
### Special keys
- ```__parent```: loads parent file and overrides duplicate keys

## Test environment
- Zsh
- FreeBSD 13.1-RELEASE
- Root commands accessible via sudo