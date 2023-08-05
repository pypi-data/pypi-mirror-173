import logging
import sys, os
import importlib
from pathlib import Path
from argparse import ArgumentParser
from os import popen

from .containers import PostgreContainer, Flavors
from .exceptions import UnknownFlavorException

# DB Connectivity
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

# Logging Config
Path("./logs").mkdir(parents=True, exist_ok=True)
log_format = "[%(levelname)s] %(asctime)s - %(name)s - %(message)s"
logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt="%y-%m-%dT%H:%M.%S",
    filename="./logs/gen.log",
    filemode="a",
)
formatter = logging.Formatter(log_format)


def main(argv=None):
    parser = ArgumentParser(description="Convert a SQLAlchemy declarative base into an Atlas HCL file.")
    parser.add_argument(
        "filepath",
        help="The relative path to the python module containing a SQLAlchemy declarative base.",
    )
    parser.add_argument(
        "--flavor",
        type=str,
        default=Flavors.POSTGRES.value,
        choices=[Flavors.POSTGRES.value],
        help="The flavor of the database HCL you want to generate.",
    )
    parser.add_argument(
        "--base",
        type=str,
        default="Base",
        help="The name of the declarative base object in the schema file.",
    )

    args = parser.parse_args(argv)
    path = args.filepath.replace("/", ".").replace(".py", "")

    sys.path.append(os.getcwd())
    mod = importlib.import_module(path)
    base = getattr(mod, args.base)

    try:
        if args.flavor == Flavors.POSTGRES.value:
            db = PostgreContainer()
        else:
            raise UnknownFlavorException(f"Flavor {args.flavor} not supported.")

        engine = create_engine(db.connection_string, poolclass=NullPool)
        base.metadata.create_all(engine)

        stream = popen(f'atlas schema inspect --url "{db.connection_string}"')
        output = stream.read()
        logging.info(output)

    finally:
        logging.debug("Completed generating HCL. Cleaning up.")
        try:
            db.container.kill()
            db.container.remove()
        except UnboundLocalError as err:
            logging.warning("db container failed to initialize, nothing to kill.")
        logging.debug("Done cleaning up.")

    print(output, file=sys.stdout)


if __name__ == "__main__":
    main()
