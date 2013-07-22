#!/usr/bin/env python
# File created on 25 Jun 2013
from __future__ import division

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The BiPy project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from unittest import TestCase, main
from shutil import rmtree, copyfile, copytree
from random import choice
from os import mkdir, path, remove
from qcli.util import (compress_to_tgz, extract_from_tgz, ERROR_MSG,
    format_blast_db_string)
import tempfile

class UtilTest(TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.gettempdir()

        test_dir = path.dirname(path.abspath(__file__))

        self.tgz_dir = path.join(test_dir, './support_files/tar_dir.tgz')
        self.tgz_file = path.join(test_dir, './support_files/tar_file.tgz')

        self.refseqs_fp = path.join(test_dir, './support_files/refseqs.fasta')
        self.blast_db_dirpath = path.join(test_dir, './support_files/blast_db')

        self.tgz_dir_file1 = 'file1.txt'
        self.tgz_dir_file2 = 'file2.txt'
        self.tgz_dir_file3 = 'file3.txt'

        self._paths_to_clean_up = []
        self._dirs_to_clean_up = []

    def tearDown(self):
        map(remove, self._paths_to_clean_up)
        map(rmtree, self._dirs_to_clean_up)

    def _get_random_string(self):
        alpha = "abcdefghijklmnopqrstuvwxyz"
        alpha += alpha.upper()
        alpha += "0123456789"
        return ''.join([choice(alpha) for i in range(10)])

    def test_compress_to_tgz(self):
        #test compressing a single file
        filename = path.join(self.tmp_dir, self._get_random_string() + '.txt')
        f = open(filename, 'w')
        f.close()

        output_tgz = path.join(self.tmp_dir, self._get_random_string() + '.tgz')

        self._paths_to_clean_up = [filename, output_tgz]

        compress_to_tgz(filename, output_tgz)
        self.assertTrue(path.exists(output_tgz),
            'The tgz file was not created in the appropiate location')

        #test compressing a directory
        dirname = path.join(self.tmp_dir, self._get_random_string())
        mkdir(dirname)
        fileA = path.join(dirname, self._get_random_string() + '.txt')
        f = open(fileA, 'w')
        f.close()
        fileB = path.join(dirname, self._get_random_string() + '.txt')
        f = open(fileB, 'w')
        f.close()

        output_tgz = path.join(self.tmp_dir, self._get_random_string() + '.tgz')
        
        self._paths_to_clean_up.append(output_tgz)
        self._dirs_to_clean_up = [dirname]

        compress_to_tgz(dirname, output_tgz)
        self.assertTrue(path.exists(output_tgz),
            'The tgz file was not created in the appropiate location')


    def test_extract_from_tgz(self):
        #test with a tgz file which contains only one file
        filename = path.join(self.tmp_dir, self._get_random_string() + '.tgz')
        copyfile(self.tgz_file, filename)

        path_name = path.join(self.tmp_dir, self._get_random_string())

        self._paths_to_clean_up = [filename, path_name]

        extract_from_tgz(filename, path_name)
        self.assertTrue(path.exists(path_name),
            'The output file was not created in the appropiate location')
        self.assertTrue(path.isfile(path_name),
            'The output was not a file')

        #test with a tgz file which contains multiple files
        filename = path.join(self.tmp_dir, self._get_random_string() + '.tgz')
        copyfile(self.tgz_dir, filename)

        path_name = path.join(self.tmp_dir, self._get_random_string())

        self._paths_to_clean_up.append(filename)
        self._dirs_to_clean_up = [path_name]

        extract_from_tgz(filename, path_name)

        self.assertTrue(path.exists(path_name),
            'The output directory was not created in the appropiate location')
        self.assertTrue(path.isdir(path_name), 'The output was not a directory')
        self.assertTrue(path.exists(path.join(path_name, self.tgz_dir_file1)),
            'The tgz contents were not extracted correctly')
        self.assertTrue(path.exists(path.join(path_name, self.tgz_dir_file2)),
            'The tgz contents were not extracted correctly')
        self.assertTrue(path.exists(path.join(path_name, self.tgz_dir_file3)),
            'The tgz contents were not extracted correctly')

        #test passing a file which is not a tgz
        filename = path.join(self.tmp_dir, self._get_random_string() + '.tgz')
        f = open(filename, 'w')
        f.write("A")
        f.close()

        self._paths_to_clean_up.append(filename)

        self.assertRaises(ValueError, extract_from_tgz, filename, "")

    def test_format_blast_db_string_file(self):
        #Test when path is fasta file
        filename = path.join(self.tmp_dir, self._get_random_string() + '.fasta')
        copyfile(self.refseqs_fp, filename)

        self._paths_to_clean_up = [filename]

        obs = format_blast_db_string(filename)
        self.assertEqual(obs, filename)

        #Test when path is a blast db base directory
        dirname = path.join(self.tmp_dir, self._get_random_string())
        copytree(self.blast_db_dirpath, dirname)

        self._dirs_to_clean_up = [dirname]

        obs = format_blast_db_string(dirname)
        exp = path.join(dirname, 'refseqs.fasta')
        self.assertEqual(obs, exp)

if __name__ == '__main__':
    main()