#!/bin/sh

VENV=./venv

usage()
{
  echo "Usage: $0 [-R] [-h]"
  echo "Create the venv"
  echo " -R Reinstall VENV at ${VENV}"
  echo " -v Verbose output"
  echo " -h Help"
  exit 2
}

unset VERBOSE
while getopts 'rRvh' c; do
  echo "Processing $c : OPTIND is $OPTIND"
  case $c in
    r) RUN=true ;;
    R) REINSTALL=true ;;
    v) VERBOSE=true ;;
    h|?) usage ;;
  esac
done

shift $((OPTIND-1))

which python3
status=$?
if [[ $status != 0 ]] ; then
    echo '*** Python3 must be installed!'
    exit
fi

if [ $REINSTALL ]; then
  echo "Removing Virtual Environment located at ${VENV}"
  rm -rf ${VENV}
fi

if [[ ! -d ${VENV} ]] ; then
    echo "*** Installing python3 venv to ${VENV}"
    python3 -m pip install --upgrade pip
    python3 -m venv ${VENV}
    source ${VENV}/bin/activate
    pip install -r requirements.txt
    brew install wget
    # https://openapi-generator.tech/docs/generators/python-flask
    brew install openapi-generator
    echo "*** Done installing python3 venv"
fi

echo "*** Using python3 venv in ${VENV}"
source ${VENV}/bin/activate

