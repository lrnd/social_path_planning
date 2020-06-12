#!/bin/bash
# Check for zsh and populate BASH_SOURCE with equivalent expression
if [ -n "$ZSH_VERSION" ]; then BASH_SOURCE=${(%):-%x}; fi
REPO_PATH=$(dirname $BASH_SOURCE)
PATH_TO_ADD=$(readlink -f $REPO_PATH/social_planner/src)
export PYTHONPATH=$PYTHONPATH:$PATH_TO_ADD
echo "Added $PATH_TO_ADD to PYTHONPATH"
PATH_TO_ADD=$(readlink -f $REPO_PATH/social_planner/scripts)
export PATH=$PATH:$PATH_TO_ADD
echo "Added $PATH_TO_ADD to PATH"
