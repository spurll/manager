import os
from glob import glob
from zipfile import ZipFile, ZIP_DEFLATED
from time import localtime, strftime

def logroll(log, archive_max=10):
    if not os.path.isfile(log):
        return

    if archive_max <= 0:
        # Delete the existing log instead of archiving it
        os.remove(logfile)
        return

    # Archive the existing log
    modified = strftime('%Y%m%d.%H%M%S', localtime(os.path.getmtime(log)))
    zip_file = f'{log}.{modified}.zip'

    # It would be nice to keep everything in one archive and rotate individual
    # files in and out, but ZipFile doesn't allow us to remove items from an
    # archive without creating a new one, so don't bother.
    with ZipFile(zip_file, 'w', compression=ZIP_DEFLATED) as z:
        z.write(log, arcname=os.path.basename(log))

    # Remove the file after archiving it
    os.remove(log)

    # Rotate
    files = sorted(glob(f'{log}.*.zip'))
    if len(files) > archive_max:
        for f in files[:-archive_max]:
            os.remove(f)
