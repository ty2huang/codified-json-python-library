"""The functions in this module encodes and decodes python objects into "codified json".

This module helps translate json-compatible python objects into a new json style that's less 
verbose when it contains many python dictionaries with the same keys. This new json style is 
known as "codified json". Reducing the size of json data can be useful for instance to avoid 
hitting payload limits when sending data across a network via REST APIs. The data encoded as 
codified json can be stored as a string or a stream of compressed bytes.

The most common functions include:

as_str(data)
as_compressed_bytes(data)
parse_str(cjson_str)
parse_compressed_bytes(cjson_bytes)

Example
-------
The code below demonstrates how to translate a python object "data" to and from codified json. 

As an example, "cjson_str" can be data sent from one system to another, and the receiving system
will parse it back into a python object called "decoded_data".

>>>> import codified_json as cjson
>>>>
>>>> data = [
>>>>     {"apple": "a", "clementine": 4, "banana": "e"}, 
>>>>     {"clementine": 4, "banana": 5, "apple": 34}, 
>>>>     {"banana": 4.5, "apple": False, "clementine": 4}, 
>>>>     {"clementine": 4, "apple": None, "banana": True}
>>>> ]
>>>>
>>>> cjson_str = cjson.as_str(data)
>>>> 
>>>> decoded_data = cjson.parse_str(cjson_str)
>>>>
>>>> assert data == decoded_data
>>>>
"""

import zlib
from codified_json import _object as cjo


def as_str(data):
    """Translates json-compatible python data into codified json string.

    Parameters
    ----------
    data : dict/list/str/int/float/bool/None
        Json-compatible python data.
    
    Returns
    -------
    str
        Codified json as string.
    """
    return cjo.encode(data)


def as_compressed_bytes(data):
    """Translates json-compatible python data into codified json bytes (compressed with GNU zip).

    Parameters
    ----------
    data : dict/list/str/int/float/bool/None
        Json-compatible python data.
    
    Returns
    -------
    bytes
        Codified json as bytes compressed with GNU zip.
    """
    return zlib.compress(as_str(data).encode())


def write_to_io(data, io):
    """Writes json-compatible python data as codified json string to io handler.

    Parameters
    ----------
    data : dict/list/str/int/float/bool/None
        Json-compatible python data.
    io : io.TextIOBase
        IO handler to write to.
    """
    io.write(as_str(data))


def write_to_compressed_bytes_io(data, io):
    """Writes json-compatible python data as codified json compressed bytes to io handler.

    Parameters
    ----------
    data : dict/list/str/int/float/bool/None
        Json-compatible python data.
    io : io.BufferedIOBase
        IO handler to write to.
    """
    io.write(as_compressed_bytes(data))


def write_to_file(data, filename):
    """Writes json-compatible python data as codified json string to file.

    Parameters
    ----------
    data : dict/list/str/int/float/bool/None
        Json-compatible python data.
    filename : str
        File path and name of file to write.
    """
    with open(filename, 'w') as f:
        write_to_io(data, f)


def write_to_compressed_bytes_file(data, filename):
    """Writes json-compatible python data as codified json compressed bytes to file.

    Parameters
    ----------
    data : dict/list/str/int/float/bool/None
        Json-compatible python data.
    filename : str
        File path and name of binary file to write.
    """
    with open(filename, 'wb') as f:
        write_to_compressed_bytes_io(data, f)


def parse_str(cjson_str):
    """Translates codified json string back into python data.

    Parameters
    ----------
    cjson_str : str
        Codified json string.

    Returns
    -------
    dict/list/str/int/float/bool/None
        Original json data as python object.
    """
    return cjo.decode(cjson_str)


def parse_compressed_bytes(cjson_bytes):
    """Translates codified json compressed bytes (decompressed with GNU zip) back into python data.

    Parameters
    ----------
    cjson_bytes : bytes
        Codified json bytes compressed with GNU zip.

    Returns
    -------
    dict/list/str/int/float/bool/None
        Original json data as python object.
    """
    return parse_str(zlib.decompress(cjson_bytes).decode())


def read_from_io(io):
    """Reads from io handler into json-compatible python data as codified json string.
    
    Parameters
    ----------
    io : io.TextIOBase
        IO handler to read from.

    Returns
    -------
    dict/list/str/int/float/bool/None
        Original json data as python object.
    """
    return parse_str(io.read())


def read_from_compressed_bytes_io(io):
    """Reads from io handler into json-compatible python data as codified json compressed bytes.
    
    Parameters
    ----------
    io : io.BufferedIOBase
        IO handler to read from.

    Returns
    -------
    dict/list/str/int/float/bool/None
        Original json data as python object.
    """
    return parse_compressed_bytes(io.read())


def read_from_file(filename):
    """Reads from file into json-compatible python data as codified json string.
    
    Parameters
    ----------
    filename : str
        File path and name of file to read from.

    Returns
    -------
    dict/list/str/int/float/bool/None
        Original json data as python object.
    """
    with open(filename, 'r') as f:
        return read_from_io(f)


def read_from_compressed_bytes_file(filename):
    """Reads from file into json-compatible python data as codified json compressed bytes.
    
    Parameters
    ----------
    filename : str
        File path and name of binary file to read from.

    Returns
    -------
    dict/list/str/int/float/bool/None
        Original json data as python object.
    """
    with open(filename, 'rb') as f:
        return read_from_compressed_bytes_io(f)

