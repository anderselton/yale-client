# -*- coding: utf-8 -*-
import argparse
import os
from .client import YaleClient


class EnvDefault(argparse.Action):
    def __init__(self, envvar, help, required=True, default=None, **kwargs):
        if envvar:
            if envvar in os.environ:
                value_default = os.getenv(key=envvar, default=default)
                if not len(value_default.strip()):
                    value_default = default
                default = value_default
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required, help="{} (env: {})".format(help, envvar),
                                         **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


yale_base_cli = \
    argparse.ArgumentParser(description="Yale-cli is designed to operate on yale systems, and doing tasks like opening "
                                        "and closing locks/alarm systems.",
                            add_help=False)
yale_base_cli.add_argument('--api', type=str.upper, required=True,
                           choices=["LOCK", "ALARM"],
                           help='what API to use', default="LOCK")

yale_base_cli.add_argument('--username', type=str, action=EnvDefault, envvar='YALE_USERNAME',
                           help='yale username')
yale_base_cli.add_argument('--password', type=str, action=EnvDefault, envvar='YALE_PASSWORD',
                           help='yale password')

yale_lock_arguments = argparse.ArgumentParser(parents=[yale_base_cli], add_help=True)
yale_lock_arguments.add_argument('--lock_id', type=str, help='The lock to operate on.  If a this is not given then '
                                                             'operation will be executed on all')
yale_lock_arguments.add_argument('--operation', type=str.upper, required=True,
                                 choices=["STATUS", "OPEN", "CLOSE"],
                                 help='what operation to do', default="STATUS")
yale_lock_arguments.add_argument('--pin', type=str, action=EnvDefault, envvar='LOCK_PIN_CODE',
                                 help='lock pin code', required=False)


def api_locks():
    try:
        arguments = yale_lock_arguments.parse_args()
        client = YaleClient(username=arguments.username, password=arguments.password)
        for lock in client.lock_api.locks():
            if arguments.lock_id is None or arguments.lock_id == lock.name:
                if arguments.operation == 'STATUS':
                    pass  # already printing out state at bottom of loop.
                elif arguments.operation == 'CLOSE':
                    if not lock.is_locked():
                        lock.close()
                elif arguments.operation == 'OPEN':
                    if arguments.pin is None:
                        raise RuntimeError("To open a lock you must specify a pin!")
                    if lock.is_locked():
                        lock.open(pin_code=arguments.pin)
                print(lock)
    except argparse.ArgumentTypeError:
        yale_lock_arguments.print_help()
    except argparse.ArgumentError:
        yale_lock_arguments.print_help()


def api_not_implemented():
    raise RuntimeError("Not implemented.")


apis = {
    'LOCK': api_locks,
    'ALARM': api_not_implemented
}


def main():
    try:
        arguments, _ignore = yale_base_cli.parse_known_args()
        apis.get(arguments.api)()
    except argparse.ArgumentError:
        yale_base_cli.print_help()


if __name__ == '__main__':
    main()
