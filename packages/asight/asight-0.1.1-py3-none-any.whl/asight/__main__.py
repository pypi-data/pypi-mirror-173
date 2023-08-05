"""The CLI entry of asight."""
from asight.asight_wrapper.asight_entrance import AsightEntrance


def main():
    """Entrance of asight."""
    AsightEntrance().main()


def init():
    """For unit  test only."""
    if __name__ == '__main__':
        main()


init()
