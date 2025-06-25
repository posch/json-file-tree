#!/usr/bin/env python3

import argparse
import json
import sys
import os
import tempfile
import base64
import logging

def verbose(msg):
    if opts.verbose:
        print(msg, file=sys.stdout)
    
def error(msg):
    print(f"ERROR {msg}", file=sys.stderr)
    
def emit_symlink(path, o):
    verbose(f"SYMLINK {path}")
    try:
        os.unlink(path)
    except Exception:
        pass
    try:
        os.symlink(o.get('symlink'), path)
    except Exception as e:
        error(f"{path}: {e}")
    
def emit_file(path, o):
    verbose(f"FILE {path}")
    try:
        d = os.path.dirname(path)
        b = os.path.basename(path)
        fd, t = tempfile.mkstemp(prefix='.', suffix=b, dir=d)
        if 'contents' in o:
            os.write(fd, o.get('contents').encode('utf-8'))
        elif 'base64_contents' in o:
            os.write(fd, base64.b64decode(o.get('base64_contents')))
        else:
            print(f"{path}: empty file")
        if 'mode' in o:
            os.fchmod(fd, o.get('mode'))
        if 'uid' in o or 'gid' in o:
            os.fchown(fd, o.get('uid', -1), o.get('gid', -1))
        os.rename(t, path)
    except Exception as e:
        error(f"{path}: {e}")

def emit_dir(path, o):
    verbose(f"DIR {path}")
    try:
        os.makedirs(path, mode=0o755, exist_ok=True)
        if 'mode' in o:
            os.chmod(path, o.get('mode'))
        if 'uid' in o or 'gid' in o:
            os.chown(path, o.get('uid', -1), o.get('gid', -1))
    except Exception as e:
        error(f"DIR {path}: {e}")
        
def parse_options():
    p = argparse.ArgumentParser()
    p.add_argument('-f', '--file')
    p.add_argument('-v', '--verbose', action='store_true')
    return p.parse_args()

opts = parse_options()

if opts.file is not None:
    with open(opts.file, 'r') as fp:
        config = json.loads(fp.read())
else:
    config = json.loads(sys.stdin.read())

for path in sorted(config.keys()):
    o = config.get(path)
    if path.endswith('/'):
        emit_dir(path, o)
    elif 'symlink' in o:
        emit_symlink(path, o)
    else:
        emit_file(path, o)
    
