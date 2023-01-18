# %%
import argparse
import sys
import logging


def create_logger():
    logger = logging.getLogger(__name__)
    handlers = logger.handlers
    if len(handlers) < 1:
        fh = logging.StreamHandler(sys.stdout)
        fh_formatter = logging.Formatter(
            "[%(levelname)s] [%(asctime)s] [%(funcName)s] %(message)s")
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)
        logger.setLevel(logging.DEBUG)
    return logger

logger = create_logger()


class Actions():
    """
    Class wrapping up the possible script tasks.

    Parameters
    ----------
    Args:
        input_args (argparse.ArgumentParser): argument parser object.
    """
    def __init__(self, input_args):
        self._option_1 = input_args.option_1
        if input_args.action not in self.dir():
              
            raise Exception(f'action {args.action} does not exist')
    
    def action_1(self) -> None:
        logger.info(f'Starting action {args.action}...')
        pass
    
    def action_2(self) -> None:
        logger.info(f'Starting action {args.action}...')
        pass


def init_argparse() -> argparse.ArgumentParser:
    """Initialize the Argument Parser to handle the input arguments passed
    to the script.

    Returns:
        argparse.ArgumentParser: argument parser object
    """
    parser = argparse.ArgumentParser(
       usage='%(prog)s action -o [OPTION]',
       description='Some useful description of the script usage.'
    )
    parser.add_argument(
        'action',
        nargs='?',
        help='The action or task to run.',
        type=str,
        choices=[
            'action_1',
            'action_2',
        ]
    )
    parser.add_argument(
        '-option_1',
        nargs='?',
        help='Some option description.',
        type=str,
        default=None
    )
    return parser

if __name__ == '__main__':
    parser = init_argparse()
    args = parser.parse_args()
    if not (args.action):
        parser.print_help()
        sys.exit(1)
    else:
        a = Actions(args)
        action = getattr(a, args.action)
        action()