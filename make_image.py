#!/usr/bin/env python3

import argparse
import re
import subprocess
import sys
import random

VERSIONS = {
    "1.8": {
        "version": "1.8-5",
        "args": {
            # 1.8.3
            "indy_sdk_url": "https://codeload.github.com/ianco/indy-sdk/tar.gz/26daafc28da10a8347c52fb2d13817301903b75b",
            # 0.5.1
            "indy_crypto_url": "https://codeload.github.com/hyperledger/indy-crypto/tar.gz/059e99ac526ad27eb1621c079bba6ebd36f16204",
        },
    },
    "1.9": {
        "version": "1.9-0",
        "args": {
            # 1.9.0
            "indy_sdk_url": "https://codeload.github.com/hyperledger/indy-sdk/tar.gz/41d97ab1dc9c8e55f9c3f9e95de70da58f5e384a",
            # 0.1.1
            "ursa_url": "https://codeload.github.com/hyperledger/ursa/tar.gz/d764981144bce9f5b0f1c085a8ebad222f429690",
        },
    },
    "1.10": {
        "version": "1.10-0",
        "args": {
            # 1.10.1
            "indy_sdk_url": "https://codeload.github.com/hyperledger/indy-sdk/tar.gz/0718ac0f2979d5c2ae649663c5e78e2f65f35100"
        },
    },
    "1.11": {
        "path": "1.10",
        "version": "1.11-0",
        "args": {
            # 1.11.0
            "indy_sdk_url": "https://codeload.github.com/hyperledger/indy-sdk/tar.gz/a583838aad867ad3dbb142b86bd76cadfe294682"
        },
    },
    "1.11.1": {
        "path": "1.10",
        "version": "1.11-1",
        "args": {
            # 1.11.1
            "indy_sdk_url": "https://codeload.github.com/hyperledger/indy-sdk/tar.gz/453edc895f2278f41e04820911d5a946199a44e4",
            "rust_version": "1.37.0",
        },
    },
    "1.12.0": {
        "path": "1.10",
        "version": "1.12-0",
        "args": {
            # 1.12.0
            "indy_sdk_url": "https://codeload.github.com/hyperledger/indy-sdk/tar.gz/55b77ec7b73b7ba4c830290f79ce7e2a37000863",
            "rust_version": "1.37.0",
        },
    },
    "1.14.1": {
        "path": "1.10",
        "version": "1.14-0",
        "args": {
            # 1.14.1 release
            "indy_sdk_url": "https://codeload.github.com/hyperledger/indy-sdk/tar.gz/e02532a575698851196ac0d48aaf7ff4647cb0d0",
            "rust_version": "1.37.0",
        },
    },
    "1.14.2": {
        "path": "1.10",
        "version": "1.14-1",
        "args": {
            # 1.14.2 release
            "indy_sdk_url": "https://codeload.github.com/hyperledger/indy-sdk/tar.gz/19dee23ad1bad04012ecb77ad8ed30113a23694f",
            "rust_version": "1.37.0",
        },
    },
    "1.15.0": {
        "path": "1.10",
        "version": "1.15-1",
        "args": {
            # 1.15.0 release
            "indy_sdk_url": "https://codeload.github.com/hyperledger/indy-sdk/tar.gz/f85afd2f94959eb59522e5dda160d2c7fdd1a4ba",
            "rust_version": "1.40.0",
        },
    },
    "1.16.0": {
        "path": "1.10",
        "version": "1.16-0",
        "args": {
            # 1.16.0 release
            "indy_sdk_url": "https://codeload.github.com/hyperledger/indy-sdk/tar.gz/b4b330ef326958d593ab42e25679c2dcd655494c",
            "rust_version": "1.44.0",
            "indy_postgres_url": "https://codeload.github.com/hyperledger/indy-sdk/tar.gz/b4b330ef326958d593ab42e25679c2dcd655494c",
        },
    },
    "1.16.0pg": {
        "path": "1.10",
        "version": "1.16-0pg",
        "args": {
            # 1.16.0 release
            "indy_sdk_url": "https://codeload.github.com/hyperledger/indy-sdk/tar.gz/b4b330ef326958d593ab42e25679c2dcd655494c",
            "rust_version": "1.44.0",
            "indy_postgres_url": "https://codeload.github.com/hyperledger/indy-sdk/tar.gz/9fbbb7939440b67e92f2698e868f14c2432cce72",
        },
    },
    "next-2": {
        "path": "next",
        "args": {
            # 1.15.0 release
            "indy_sdk_url": "https://codeload.github.com/hyperledger/indy-sdk/tar.gz/f85afd2f94959eb59522e5dda160d2c7fdd1a4ba",
        },
    },
}

DEFAULT_NAME = "bcgovimages/von-image"
PY_36_VERSION = "3.6.13"
PY_37_VERSION = "3.7.10"
PY_38_VERSION = "3.8.8"
PY_DEFAULT_VERSION = PY_36_VERSION


parser = argparse.ArgumentParser(description="Generate a von-image Docker image")
parser.add_argument(
    "-n", "--name", default=DEFAULT_NAME, help="the base name for the docker image"
)
parser.add_argument("-t", "--tag", help="a custom tag for the docker image")
parser.add_argument("-f", "--file", help="use a custom Dockerfile")
parser.add_argument(
    "--build-arg", metavar="ARG=VAL", action="append", help="add docker build arguments"
)
parser.add_argument(
    "--debug", action="store_true", help="produce a debug build of libindy"
)
parser.add_argument(
    "--dry-run",
    action="store_true",
    help="print docker command line instead of executing",
)
parser.add_argument("--no-cache", action="store_true", help="ignore docker image cache")
parser.add_argument(
    "-o",
    "--output",
    help="output an updated Dockerfile with the build arguments replaced",
)
parser.add_argument(
    "--py36",
    dest="python",
    action="store_const",
    const=PY_36_VERSION,
    help="build with the default python 3.6 version",
)
parser.add_argument(
    "--py37",
    dest="python",
    action="store_const",
    const=PY_37_VERSION,
    help="build with the default python 3.7 version",
)
parser.add_argument(
    "--py38",
    dest="python",
    action="store_const",
    const=PY_38_VERSION,
    help="build with the default python 3.8 version",
)
parser.add_argument("--python", help="use a specific python version")
parser.add_argument("--push", action="store_true", help="push the resulting image")
parser.add_argument(
    "-q", "--quiet", action="store_true", help="suppress output from docker build"
)
parser.add_argument(
    "--release",
    dest="debug",
    action="store_false",
    help="produce a release build of libindy",
)
parser.add_argument("--platform", help="build for a specific platform")
parser.add_argument(
    "--postgres",
    action="store_true",
    help="force re-install of postgres plug-in from github",
)
parser.add_argument(
    "--vonx",
    action="store_true",
    help="force re-install of von-x from library in requirements-vonx.txt",
)
parser.add_argument(
    "--s2i", action="store_true", help="build the s2i image for this version"
)
parser.add_argument("--squash", action="store_true", help="produce a smaller image")
parser.add_argument("--test", action="store_true", help="perform tests on docker image")
parser.add_argument(
    "version", choices=VERSIONS.keys(), help="the predefined release version"
)

args = parser.parse_args()
ver = VERSIONS[args.version]
py_ver = args.python or ver.get("python_version", PY_DEFAULT_VERSION)

target = ver.get("path", args.version)
if target.startswith("next"):
    dockerfile = target + "/Dockerfile"
else:
    dockerfile = target + "/Dockerfile.ubuntu"
if args.file:
    dockerfile = args.file

tag = args.tag
tag_name = args.name
if tag:
    tag_name, tag_version = tag.split(":", 2)
else:
    if target.startswith("next"):
        pfx = ""
    else:
        pfx = "py" + py_ver[0:1] + py_ver[2:3] + "-"
    tag_version = pfx + ver.get("version", args.version)
    if args.debug:
        tag_version += "-debug"
    tag = tag_name + ":" + tag_version

build_args = {}
build_args.update(ver["args"])
build_args["python_version"] = py_ver
build_args["tag_name"] = tag_name
build_args["tag_version"] = tag_version
if not args.debug:
    build_args["indy_build_flags"] = "--release"
if args.build_arg:
    for arg in args.build_arg:
        key, val = arg.split("=", 2)
        build_args[key] = val

if args.output:
    src_path = dockerfile
    src_replace = build_args
    if args.test:
        src_path = target + "/Dockerfile.test"
        src_replace = {"base_image": tag}
    elif args.s2i:
        src_path = target + "/Dockerfile.s2i"
        src_replace = {"base_image": tag}
    with open(args.output, "w") as out:
        with open(src_path) as src:
            for line in src:
                m = re.match(r"^ARG\s+(\w+)=?(.*)$", line)
                if m:
                    line = "ARG {}={}\n".format(
                        m.group(1), src_replace.get(m.group(1), m.group(2))
                    )
                out.write(line)
    sys.exit(0)

cmd_args = []
for k, v in build_args.items():
    cmd_args.extend(["--build-arg", "{}={}".format(k, v)])
if dockerfile:
    cmd_args.extend(["-f", dockerfile])
if args.no_cache:
    cmd_args.append("--no-cache")
if args.squash:
    cmd_args.append("--squash")
cmd_args.extend(["-t", tag])
if args.platform:
    cmd_args.extend(["--platform", args.platform])
if args.postgres:
    cmd_args.extend(
        ["--build-arg", "CACHEBUSTPX=" + str(random.randint(100000, 999999)) + ""]
    )
if args.vonx:
    cmd_args.extend(
        ["--build-arg", "CACHEBUSTVX=" + str(random.randint(100000, 999999)) + ""]
    )
    cmd_args.extend(["--build-arg", "VONX_FORCE=True"])

cmd_args.append(target)
cmd = ["docker", "build"] + cmd_args

if args.dry_run:
    print(" ".join(cmd))
else:
    print("Building docker image...")
    proc = subprocess.run(cmd, stdout=(subprocess.PIPE if args.quiet else None))
    if proc.returncode:
        print("build failed")
        sys.exit(1)
    if args.quiet:
        print("Successfully tagged {}".format(tag))
    proc_sz = subprocess.run(
        ["docker", "image", "inspect", tag, "--format={{.Size}}"],
        stdout=subprocess.PIPE,
    )
    size = int(proc_sz.stdout.decode("ascii").strip()) / 1024.0 / 1024.0
    print("%0.2f%s" % (size, "MB"))

if args.s2i:
    s2i_tag = tag + "-s2i"
    s2i_cmd = [
        "docker",
        "build",
        "--build-arg",
        "base_image=" + tag,
        "-t",
        s2i_tag,
        "-f",
        target + "/Dockerfile.s2i",
        target,
    ]
    if args.dry_run:
        print(" ".join(s2i_cmd))
    else:
        proc = subprocess.run(s2i_cmd, stdout=(subprocess.PIPE if args.quiet else None))
        if proc.returncode:
            print("s2i build failed")
            sys.exit(1)
        if args.quiet:
            print("Successfully tagged {}".format(s2i_tag))

if not args.dry_run:
    if args.test or args.push:
        test_path = target + "/Dockerfile.test"
        test_tag = tag + "-test"
        proc_bt = subprocess.run(
            [
                "docker",
                "build",
                "--build-arg",
                "base_image=" + tag,
                "-t",
                test_tag,
                "-f",
                test_path,
                target,
            ]
        )
        if proc_bt.returncode:
            print("test image build failed")
            sys.exit(1)
        proc_test = subprocess.run(["docker", "run", "--rm", "-i", test_tag])
        if proc_test.returncode:
            print("One or more tests failed")
            sys.exit(1)
        print("All tests passed")

    if args.push:
        print("Pushing docker image...")
        proc = subprocess.run(["docker", "push", s2i_tag if args.s2i else tag])
        if proc.returncode:
            print("push failed")
            sys.exit(1)
