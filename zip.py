import os
import glob
import shutil
import sys
import time
import zipfile
import argparse
import logging
import tarfile

DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
LOG_FORMATTER = logging.Formatter(fmt='%(asctime)s.%(msecs)03d %(message)s', datefmt=DATETIME_FORMAT)
LOGGER = logging.Logger(__file__)

def timeit(f):
    """
    help: [ https://stackoverflow.com/questions/1622943/timeit-versus-timing-decorator ]
    :param f:
    :return:
    """
    def timed(*args, **kw):
        ts = time.time()
        LOGGER.debug('>>> func:[{}] started @ [{}]'.format(f.__name__, ts))
        result = f(*args, **kw)
        te = time.time()
        LOGGER.debug('<<< func:[{}] ended @ [{}]'.format(f.__name__, te))
        LOGGER.info('=== func:[{}] took: [{}]'.format(f.__name__, print_time(te - ts)))
        return result
    return timed

def print_time(time):
    miliseconds = time * 1000 % 1000
    seconds = time % 60
    time /= 60
    minutes = time % 60
    time /= 60
    hours = time % 24
    time /= 24
    days = time
    return "%ddays %.2d:%.2d:%.2d.%.3d" % (days, hours, minutes, seconds, miliseconds)

@timeit
def unzip_archives(paths):
    for path in paths:
        LOGGER.info("unzipping archive [%s]" % path)
        if ".zip" in path:
            with zipfile.ZipFile(path, 'r') as z:
                z.extractall()
                z.close()
            LOGGER.info("unzipped archive [%s]" % path)
        elif ".tar" in path:
            with tarfile.open(path, 'r') as t:
                t.extractall()
                t.close()
            LOGGER.info("untarred archive [%s]" % path)
        else:
            LOGGER.error("failed to unpack as [%s] is not [ .zip, .tar] file" % path)

@timeit
def zip_files_or_folders(archive, paths):
    LOGGER.info("creating archive [%s]" % archive)
    with zipfile.ZipFile(archive, 'w') as z:
        for path in paths:
            LOGGER.debug("zipping path [%s]" % path)
            if os.path.exists(path):
                if os.path.isdir(path):
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            filename = os.path.join(root, file)
                            arcname = os.path.relpath(os.path.join(root, file), 
                                                    os.path.join(path, '..'))
                            z.write(filename, arcname)
                            LOGGER.debug(">>> added file [%s] as [%s]" % (filename, arcname))
                else:
                    z.write(path, path)
                    LOGGER.debug(">>> added file [%s] as [%s]" % (path, path))
            else:
                LOGGER.error("failed to find file [%s]" % path)
            LOGGER.debug("zipped path [%s]" % path)
        z.close()
    LOGGER.info("closed archive [%s]" % archive)

def menu():
    parser = argparse.ArgumentParser(description='Zip or unzip selected paths. Will continue recursively if providing folders. Will use current directory as working folder.')

    parser.add_argument('-d', '--debug', choices=['critical', 'error', 'warning', 'info', 'debug', 'notset'],
                        default='info', required=False,
                        help='parameter indicating the level of logs to be shown on screen')

    parser.add_argument('-n', '--name', default="", required=False, type=str, 
                        help='parameter indicating the name of the archive to be created')
    parser.add_argument('-u', '--unzip', default=False, action='store_true', required=False,
                        help='flag indicating if the script should unzip. The default action is to zip if no flag is provided')
    
    parser.add_argument('paths', metavar='paths', nargs='+',
                        help='paths where to search through - list of strings separated by space')
    arguments = parser.parse_args()

    if arguments.name == "" and arguments.unzip == False:
        print("Provide a name for the archive to be created with the `-n` option, or provide the `-u` flag to unzip the paths selected.")
        sys.exit(1)

    if arguments.name != "":
        if ".zip" not in arguments.name[:-4]:
            arguments.name += ".zip"
        arguments.unzip = False

    # patch logging level to objects
    debug_name = arguments.debug
    debug_levels = {'critical': logging.CRITICAL, 'error': logging.ERROR, 'warning': logging.WARNING,
                    'info': logging.INFO, 'debug': logging.DEBUG, 'notset': logging.NOTSET}
    arguments.debug = debug_levels[arguments.debug]
    print("Using logging level [{}:{}]".format(debug_name, arguments.debug))

    return arguments

def main():
    args = menu()

    handler = logging.StreamHandler()
    handler.setFormatter(LOG_FORMATTER)
    handler.setLevel(args.debug)
    LOGGER.addHandler(handler)
    LOGGER.setLevel(args.debug)

    if args.unzip:
        unzip_archives(args.paths)
    else:
        zip_files_or_folders(args.name, args.paths)

if __name__ == "__main__":
    main()