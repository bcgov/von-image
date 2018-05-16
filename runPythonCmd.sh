#!/bin/bash
SCRIPT_DIR=$(dirname $0)
PYTHON_EXE=python
_pythonVirtualEnvFile="${SCRIPT_DIR}/python.env"
if [ -f ${_pythonVirtualEnvFile} ]; then
  . ${_pythonVirtualEnvFile}
  export PATH="$PATH:${PYTHON_ENV_DIR}"
fi

PYTHON_PATH=$(type -P "$PYTHON_EXE")
if [ -z ${PYTHON_PATH} ]; then
  echo -e "The ${PYTHON_EXE} executable is needed and not on your path."
  echo "To specify a virtual environment, create a file named python.env and"
  echo "set an environment variable named PYTHON_ENV_DIR to the directory containing the"
  echo "desired python executable."
  exit 1
fi

# ==============================================================================================================================
usage () {
  echo "========================================================================================"
  echo "Runs Python commands using the a default or virtual python environment."
  echo "----------------------------------------------------------------------------------------"
  echo "Usage:"
  echo
  echo "${0} <command>"
  echo
  echo "Where:"
  echo " - <command> is the Python command you wish to run."
  echo
  echo "Examples:"
  echo "${0} --version"
  echo "========================================================================================"
  exit 1
}

if [ -z "${1}" ]; then
  usage
fi
# ==============================================================================================================================

${PYTHON_PATH} ${@}