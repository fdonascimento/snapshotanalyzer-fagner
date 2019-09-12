# snapshotanalyzer-fagner
Demo project to manage AWS EC2 instance snapshots

## About

This project is a demo, and uses boto3 to manage AWS EC2 instance snapshots.

## Configuring

Shotty uses the configuration file created by the AWS cli. e.g.

`aws configure`

## Running

`pipenv run "python shotty/shotty.py <command> <--name-NAME>"`

*command* is list, start, or stop
*name* is optional
