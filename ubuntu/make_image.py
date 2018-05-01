#!/usr/bin/env python3

import argparse
import os.path
import subprocess
import sys

VERSIONS = {
    "1.3.1-dev-441-ew": {
        "args": {
            "indy_sdk_repo": "https://github.com/bcgov/indy-sdk.git",
            "indy_sdk_rev": "574ca3a881d188c3fd7400d27acbe5edc4c7f666",
            "indy_crypto_repo": "https://github.com/hyperledger/indy-crypto.git",
            "indy_crypto_rev": "96c79b36c5056eade5a8e3bae418f5a733cc8d8d",
        }
    },
    "1.3.1-dev-489-ew": {
        "args": {
            "indy_sdk_repo": "https://github.com/ianco/indy-sdk.git",
            "indy_sdk_rev": "c617b573fb233a31a2e042527c5ddd7de54ba5f3",
            "indy_crypto_repo": "https://github.com/hyperledger/indy-crypto.git",
            "indy_crypto_rev": "62b777dfce67b14065659b7824316b4433cd1f57",
        }
    }
}

DEFAULT_NAME = 'andrewwhitehead/von-image'
PY_35_VERSION = '3.5.5'
PY_36_VERSION = '3.6.3'


parser = argparse.ArgumentParser(description='Generate a von-image Docker image')
parser.add_argument('-n', '--name', default=DEFAULT_NAME, help='the base name for the docker image')
parser.add_argument('-t', '--tag', help='a custom tag for the docker image')
parser.add_argument('-f', '--file', help='use a custom Dockerfile')
parser.add_argument('--build-arg', metavar='ARG=VAL', action='append', help='add docker build arguments')
parser.add_argument('--no-cache', action='store_true', help='ignore docker image cache')
parser.add_argument('--py35', dest='python', action='store_const', const=PY_35_VERSION, help='use the default python 3.5 version')
parser.add_argument('--py36', dest='python', action='store_const', const=PY_36_VERSION, help='use the default python 3.6 version')
parser.add_argument('--python', help='use a specific python version')
parser.add_argument('--push', action='store_true', help='push the resulting image')
parser.add_argument('-q', '--quiet', action='store_true', help='suppress output from docker build')
parser.add_argument('--release', action='store_true', help='produce a release build of libindy')
parser.add_argument('--squash', action='store_true', help='produce a smaller image')
parser.add_argument('--test', action='store_true', help='print docker command line instead of executing')
parser.add_argument('version', choices=VERSIONS.keys(), help='the predefined release version')

args = parser.parse_args()
py_ver = args.python or PY_35_VERSION
reqs_path = 'requirements-' + args.version + '.txt'
if not os.path.exists(reqs_path):
    raise Exception('Missing requirements file: {}'.format(reqs_path))

build_args = {}
ver = VERSIONS[args.version]
build_args.update(ver['args'])
build_args['python_version'] = py_ver
build_args['requirements'] = reqs_path
if args.release:
    build_args['indy_build_flags'] = '--release'
if args.build_arg:
    for arg in args.build_arg:
        key, val = arg.split('=', 2)
        build_args[key] = val

tag = args.tag
if not tag:
    pfx = args.name + ':py' + py_ver[0:1] + py_ver[2:3] + '-'
    tag = pfx + 'indy' + args.version
    if not args.release:
        tag += '-debug'

cmd_args = []
for k,v in build_args.items():
    cmd_args.extend(['--build-arg', '{}={}'.format(k,v)])
target = '.'
if args.file:
    cmd_args.extend(['-f', args.file])
if args.no_cache:
    cmd_args.append('--no-cache')
if args.squash:
    cmd_args.append('--squash')
cmd_args.extend(['-t', tag])
cmd_args.append(target)
cmd = ['docker', 'build'] + cmd_args
if args.test:
    print(' '.join(cmd))
else:
    print('Building docker image...')
    proc = subprocess.run(cmd, stdout=(subprocess.PIPE if args.quiet else None))
    if proc.returncode:
        print('build failed')
        sys.exit(1)
    else:
        if args.quiet:
            print('Successfully tagged {}'.format(tag))
        proc_sz = subprocess.run(['docker', 'image', 'inspect', tag, '--format={{.Size}}'], stdout=subprocess.PIPE)
        size = int(proc_sz.stdout.decode('ascii').strip()) / 1024.0 / 1024.0
        print('%0.2f%s' % (size, 'MB'))
        if args.push:
            print('Pushing docker image...')
            proc = subprocess.run(['docker', 'push', tag])
            if proc.returncode:
                print('push failed')
                sys.exit(1)
