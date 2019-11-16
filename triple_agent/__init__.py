__version__ = "0.0.1"

try:
    # This is to account for the difference between my local account and the CI environment.
    # If SpyPartyParse is installed and added to the python site-packages properly, there is no
    # need for a separate sys.path.append.  But if it's a git repo, I need to add it to my path.
    # This also means I won't accidentally check in changes to __init__ that I don't actually want to push.
    # pylint: disable=import-error
    import __append_spp_path__
except ModuleNotFoundError:
    pass
