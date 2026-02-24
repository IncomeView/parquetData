import click
from parquetData.pipeline.bronze_pipeline import run_bronze_pipeline

@click.group()
def cli():
    pass

@cli.command()
@click.argument("table_name")
@click.option("--schema", default="public")
def bronze(table_name, schema):
    run_bronze_pipeline(table_name, schema)

if __name__ == "__main__":
    cli()
