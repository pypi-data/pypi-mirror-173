from iutils.utils import remove_last_n_chars
import hmac
import os
import sys


class Site:
    def get_signature(self, n_characters_to_remove=1):
        """Read from STDIN, remove specified columns and output to STDOUT.

        rm_columns: a sorted list of unique numbers that denotes the columns to be
                    removed.
        """
        data = sys.stdin.read()
        data = remove_last_n_chars(data, n_characters_to_remove)

        return hmac.new(
            os.environb[b"EVENT_ROUTER_CIRCLECI_SECRET"], bytes(data, "utf-8"), "sha256"
        ).hexdigest()

    def print_signature(self):
        print(self.get_signature())


class CircleCI(Site):
    pass


if __name__ == "__main__":
    circleci = CircleCI()
    circleci.print_signature()
