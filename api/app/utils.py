import hashlib
import os


def allowed_file(filename):
    """
    Checks if the format for the file received is acceptable. For this
    particular case, we must accept only image files. This is, files with
    extension ".png", ".jpg", ".jpeg" or ".gif".

    Parameters
    ----------
    filename : str
        Filename from werkzeug.datastructures.FileStorage file.

    Returns
    -------
    bool
        True if the file is an image, False otherwise.
    """
    # TODO: Implement the allowed_file function
    # Current implementation will return True for any file
    # Check if the file extension of the filename received is in the set of allowed extensions (".png", ".jpg", ".jpeg", ".gif")
    allowed_extensions = {".png", ".jpg", ".jpeg", ".gif"}
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)
    #return os.path.splitext(filename)[1].lower() in allowed_extensions
    #return True

async def get_file_hash(file):
    """
    Returns a new filename based on the file content using MD5 hashing.
    It uses hashlib.md5() function from Python standard library to get
    the hash.

    Parameters
    ----------
    file : werkzeug.datastructures.FileStorage
        File sent by user.

    Returns
    -------
    str
        New filename based in md5 file hash.
    """
    # TODO: Implement the get_file_hash function
    # Current implementation will return the original file name.

    # Read file content and generate md5 hash (Check: https://docs.python.org/3/library/hashlib.html#hashlib.md5)

    # Return file pointer to the beginning

    # Add original file extension

    #return file.filename
    # Read the file content
    file_content = await file.read()

    # Generate MD5 hash
    md5_hash = hashlib.md5(file_content).hexdigest()

    # Reset file pointer to the beginning
    await file.seek(0)

    # Get the original file extension
    file_extension = os.path.splitext(file.filename)[1].lower()

    # Return the new filename with the MD5 hash and original file extension
    return f"{md5_hash}{file_extension}"
