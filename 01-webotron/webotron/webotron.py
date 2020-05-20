#!/usr/bin/python
# -*- coding:utf-8 -*-

""" Webotron: Deploy websites with AWS."""

import boto3
import click
from bucket import BucketManager


session = boto3.Session(profile_name='pythonautomation')
bucket_manager=BucketManager(session)


@click.group()
def cli():
    """Webetron deploys websites to AWS"""


@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets"
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    "list objects in s3 bucket"
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    "create and configire s3 bucket"
    s3_bucket=bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)
    return


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    "sync contents of pathname to bucket"
    bucket_manager.sync(pathname, bucket)

if __name__ == '__main__':
    cli()
