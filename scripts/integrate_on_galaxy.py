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


from qcli import (parse_command_line_parameters, 
                  make_option)
from qcli.galaxy_integration import integrate

script_info = {}
script_info['brief_description'] = "Integrate a set of qcli compatible scripts \
on a Galaxy instance."
script_info['script_description'] = "For each script present in the input \
directory, generates the corresponding XML file, put it in the correct Galaxy \
directory and updates the Galaxy's tool_conf.xml file."
script_info['script_usage'] = []
script_info['script_usage'].append(("Example",
"Integrate the scripts under 'scripts_dir' on the Galaxy instance \
'galaxy_dist_dir', using the configuration file 'config_file.txt'.",
"%prog -i scripts_dir -g galaxy_dist_dir -c config_file.txt"))
script_info['output_description']= ""
script_info['required_options'] = [
    make_option('-i', '--input_dir', type="existing_dirpath",
                help='directory containing the scripts to integrate'),
    make_option('-g', '--galaxy_dist_dir', type="existing_dirpath",
                help='The Galaxy installation directory'),
    make_option('-c', '--config_file', type="existing_filepath",
                help='Configuration file which contains the section structure' +
                    ' of the scripts')
]
script_info['optional_options'] = [
    make_option('--update_tool_conf', action='store_true',
                help='By default, the Galaxy tool_conf file is overwritten.' + 
                    ' Use this option to update it instead of overwrite it.'),
    make_option('-l', '--log_file', type='new_filepath',
                help='File path where to store the log file.' +
                    ' [Default: <input_dir>/integration.log]')
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    integrate(opts.input_dir, opts.galaxy_dist_dir, opts.config_file,
        opts.update_tool_conf, opts.log_file)

if __name__ == "__main__":
    main()