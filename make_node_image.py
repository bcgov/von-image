#!/usr/bin/env python3

import argparse
import re
import subprocess
import sys

DEFAULT_NAME = "bcgovimages/von-image"
PY_35_VERSION = "3.5.7"
PY_36_VERSION = "3.6.13"
PY_DEFAULT_VERSION = PY_35_VERSION


VERSIONS = {
    "1.12": {
        "path": "node-1.12",
        "version": "node-1.12-6",
        "args": {
            # 1.16.0 release
            "indy_sdk_url": "https://codeload.github.com/hyperledger/indy-sdk/tar.gz/b4b330ef326958d593ab42e25679c2dcd655494c",
            # 0.3.2
            "ursa_url": "https://codeload.github.com/hyperledger/ursa/tar.gz/394bcdf1413ac41793e96175d46d745ed6ffd970",
            "rocksdb_lib_ver":"5.8.fb",
            "rust_version": "1.46.0",
        },
        "python_version": PY_36_VERSION,
    },
}


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
    "--py35",
    dest="python",
    action="store_const",
    const=PY_35_VERSION,
    help="build with the default python 3.5 version",
)
parser.add_argument(
    "--py36",
    dest="python",
    action="store_const",
    const=PY_36_VERSION,
    help="build with the default python 3.6 version",
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
dockerfile = target + "/Dockerfile.ubuntu"
if args.file:
    dockerfile = args.file

tag = args.tag
tag_name = args.name
if tag:
    tag_name, tag_version = tag.split(":", 2)
else:
    tag_version = ver.get("version", args.version)
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
