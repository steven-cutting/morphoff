#! /usr/bin/env bash

env coverage erase
env coverage run -a --source=morphoff $(which py.test)
env coverage report -m
