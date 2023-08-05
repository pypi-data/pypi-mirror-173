from copy import deepcopy
import json
import yaml
from os.path import exists

KEY_PARENT = '__parent'

def hello():
  return 'worldssss'

def mergeDicts(DictX, DictY, isDictXCopied = False):
  if not isDictXCopied:
    DictX = deepcopy(DictX)
  
  for key in DictY:
    if key in DictX:
      # key exists: 
      if isinstance(DictX[key], dict) and isinstance(DictY[key], dict):
        # value is a dict: recurse
        mergeDicts(DictX[key], DictY[key], True)
      else: 
        # value is simple: overwrite
        DictX[key] = DictY[key]
    else:
      # new key: copy over
      DictX[key] = DictY[key]

  return DictX

def loadConfig(fname):
  if not exists(fname):
    raise Exception('Missing config file: {}'.format(fname))

  InStream = open(fname,'r')
  ret = yaml.load(InStream, Loader=yaml.Loader)
  InStream.close()

  if KEY_PARENT in ret:
    parent = loadConfig(ret[KEY_PARENT])
    # print ('parent:\n' + json.dumps(parent, indent = 2))
    # remove the meta-key in the child
    del ret[KEY_PARENT]
    final = mergeDicts(parent, ret)
    # print ('merged:\n' + json.dumps(final, indent = 2))
    # print ('parent:\n' + json.dumps(parent, indent = 2))
    return final
    return {**parent, **ret}
    return parent | ret
  else:
    return ret
