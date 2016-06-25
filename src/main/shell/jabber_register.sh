#!/bin/sh

username=${1:-`hostname`}
password=${2:-'000000'}
host=${3:-'localhost'}

ejabberdctl register $username $host $password

