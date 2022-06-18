from pkg_resources import require
from core.RequestHandler import RequestHandler
from libs.logger import Logger
from getpass import getpass
import argparse
import click

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)

    if debug:
        logger = Logger("DEBUG", COLORED=True)
    else:
        logger = Logger("INFO", COLORED=True)
    requests_handler = RequestHandler()
    ctx.obj['request_handler'] = requests_handler

@cli.command()
@click.pass_context
@click.option("-l", "--list")
@click.option("-d", "--description")
def create(ctx, list, description):
    ctx.obj['request_handler'].create( list=list, 
                                       description=description )

@cli.command()
@click.pass_context
@click.option("-l", "--list")
@click.option("-d", "--description")
def modify(ctx, list, description):
    ctx.obj['request_handler'].modify( list=list, 
                                        description=description)

@cli.command()
@click.pass_context
@click.option("-l", "--list")
def delete(ctx, list):
    ctx.obj['request_handler'].delete( list=list )

@cli.command()
@click.pass_context
def set(ctx):
    pass

@cli.command()
@click.pass_context
def unset(ctx):
    pass

@cli.command()
@click.pass_context
@click.argument("title")
@click.option("-l", "--list", required=True)
@click.option("-d", "--description")
@click.option("-f", "--filters")
@click.option("-a", "--attachments")
@click.option("-i", "--information")
def add(ctx, title, list, description, filters, attachments, information):
    ctx.obj['request_handler'].add( title=title, 
                                    listName=list, 
                                    description=description, 
                                    filters=filters, 
                                    attachments=attachments, 
                                    information=information )

@cli.command()
@click.pass_context
def update(ctx):
    pass

@cli.command()
@click.pass_context
@click.argument("title")
@click.option("-l", "--list", required=True)
def remove(ctx, title, list):
    ctx.obj['request_handler'].remove( title=title,
                                       list=list )

@cli.command()
@click.pass_context
@click.option("-l", "--list")
@click.option("-n", "--object-name")
@click.option("-f", "--filter")
def get(ctx, list, object_name, filter):
    ctx.obj['request_handler'].get( list=list, 
                                    name=object_name, 
                                    filter=filter )

@cli.command()
@click.pass_context
def logout(ctx):
    ctx.obj['request_handler'].logout()

if __name__ == "__main__":
    cli()