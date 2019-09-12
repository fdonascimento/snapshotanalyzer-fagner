import boto3
import click

session = boto3.Session(profile_name='default')
ec2 = session.resource('ec2')

def filter_instances(name):
    instances = []

    if name:
        filters = [{'Name':'tag:Name', 'Values':[name]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def cli():
    """Shotty manages snapshots"""

@cli.group('volumes')
def volumes():
    """Commands for volumes"""

@volumes.command('list')
@click.option('--name', default=None,
    help="Only volumes for name (tag Name:<name>)")
def list_volumes(name):
    "List EC2 volumes"
    instances = filter_instances(name)

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))
    return

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list')
@click.option('--name', default=None,
    help="Only snapshots for name (tag Name:<name>)")
def list_volumes(name):
    "List EC2 snapshots"
    instances = filter_instances(name)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))
    return

@cli.group('instances')
def instances():
    """Commands for instances"""

@instances.command('snapshot', help="Create snapshots of all volumes")
@click.option('--name', default=None,
    help="Only instances for name (tag Name:<name>)")
def create_snapshots(name):
    "Create snapshots for EC2 instances"

    instances = filter_instances(name)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by Snapshotanalyzer Fagner")

        print("Starting {0}...".format(i.id))
        i.start()
        i.wait_until_running()
        print("Job is done!")

    return

@instances.command('list')
@click.option('--name', default=None,
    help="Only instances for name (tag Name:<name>)")
def list_intances(name):
    "List EC2 instances"
    instances = filter_instances(name)

    for i in instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Name', '<no name>')
        )))
    return

@instances.command('stop')
@click.option('--name', default=None,
    help='Only instances for name')
def stop_instances(name):
    "Stop EC2 instances"
    instances = filter_instances(name)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()
    return

@instances.command('start')
@click.option('--name', default=None,
    help='Only instances for name')
def start_instances(name):
    "Start EC2 instances"
    instances = filter_instances(name)

    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()
    return

if __name__ =='__main__':
    cli()
