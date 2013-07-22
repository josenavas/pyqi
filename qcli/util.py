#!/usr/bin/env python
""" Utilities for parsing command line options and arguments

This code was derived from QIIME (www.qiime.org), where it was initally
developed. It has been ported to qcli to support accessing this functionality 
without those dependencies.

"""

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The BiPy Project"
__credits__ = ["Greg Caporaso", "Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"

from os import remove, listdir
from os.path import isdir, splitext, join, basename
from subprocess import Popen, PIPE, STDOUT
import tarfile
from shutil import move

ERROR_MSG = "The input file is not a tar file!"

def qcli_system_call(cmd, shell=True):
    """Call cmd and return (stdout, stderr, return_value).

    cmd can be either a string containing the command to be run, or a sequence
    of strings that are the tokens of the command.

    Please see Python's subprocess. Popen for a description of the shell
    parameter and how cmd is interpreted differently based on its value.
    
    This function is ported from QIIME (previously qiime_system_call).
    """
    proc = Popen(cmd,
                 shell=shell,
                 universal_newlines=True,
                 stdout=PIPE,
                 stderr=PIPE)
    # communicate pulls all stdout/stderr from the PIPEs to 
    # avoid blocking -- don't remove this line!
    stdout, stderr = proc.communicate()
    return_value = proc.returncode
    return stdout, stderr, return_value

def remove_files(list_of_filepaths, error_on_missing=True):
    """Remove list of filepaths, optionally raising an error if any are missing
    
       This function is ported from PyCogent.
    """
    missing = []
    for fp in list_of_filepaths:
        try:
            remove(fp)
        except OSError:
            missing.append(fp)

    if error_on_missing and missing:
        raise OSError, "Some filepaths were not accessible: %s" % '\t'.join(missing)

def format_blast_db_string(in_path):
    """Generate a string with the path to the blast database

    Input:
        in_path: the path to the blast database base directory or to a fasta
            file with the reference sequences to create the DB on-the-fly
    """
    if isdir(in_path):
        # The path is the base directory of a blast database
        # Get one file of the directory
        f = listdir(in_path)[0]
        f = join(in_path, f)
        # Get the base path of the file
        basepath, ext = splitext(f)
        return basepath
    else:
        # The path is a fasta file
        return in_path

def compress_to_tgz(in_path, tgz_fp):
    """Generate a tgz file with the contents of the provided path

    Input:
        in_path: path to include in the tgz file
        tgz_fp: path to the result tgz file
    """
    t = tarfile.open(name = tgz_fp, mode = 'w:gz')
    t.add(in_path, basename(in_path))
    t.close()

def extract_from_tgz(tgz_file, output_path):
    """Extract the contents of the tgz file in the provided output path

    Input:
        tgz_file: filepath to the tgz file
        output_path: path to the output directory

    If the tgz_file only contains one file, it is extracted and renamed as the
    path indicated 'output_path'

    Note: raises a ValueError if tgz_file is not a tgz_file
        If there is any other error during the extraction, it propagates the
        error raised by tarfile
    """
    try:
        t = tarfile.open(name = tgz_file, mode = 'r')
    except tarfile.ReadError:
        raise ValueError, ERROR_MSG
    else:
        names_list = t.getnames()
        # if the tgz_file only has one file is not necessary to generate an
        # output directory
        if len(names_list) == 1:
            t.extractall()
            move(names_list[0], output_path)
        else:
            t.extractall(path=output_path)
        t.close()