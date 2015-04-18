# -*- coding: UTF-8 -*-
import os
import sys
import codecs
import shutil

# 1: dict file
# 2: source path
# 3: dist path

path_dict = {}

with codecs.open(os.path.abspath(sys.argv[1]), 'r', 'utf-8') as f:
    for line in f:
        line = line.split('|')
        path_dict[line[0]] = line[1].strip()


source_path = os.path.abspath(sys.argv[2])
out_path = os.path.abspath(sys.argv[3])
if not os.path.exists(out_path):
    os.makedirs(out_path)
out_sum_file = codecs.open(out_path + '/SUMMARY.md', 'w', 'utf-8')
with codecs.open(source_path + '/SUMMARY.md', 'r', 'utf-8') as f:
    for line in f:
        if len(line.strip()) == 0:
            continue
        if line.startswith("#"):
            continue
        paths = line[line.rindex("(") + 1:line.rindex(")")]
        replace = paths[:-len(".md")]
        replacer = ''
        paths = replace.split('/')
        try:
            for path in paths:
                replacer = replacer + '/' + path_dict[path]
            replacer = replacer[1:]
        except (AttributeError, KeyError):
            print "Warning, no key: " + line[line.rindex("(") + 1:line.rindex(")")]
            replacer = replace
        if not os.path.exists(os.path.dirname(out_path + '/' + replacer + '.md').encode('utf-8')):
            os.mkdir(os.path.dirname(out_path + '/' + replacer + '.md').encode('utf-8'))
        shutil.copy2(source_path + '/' + replace + '.md', out_path + '/' + replacer + '.md')
        line = line.replace(replace, replacer)
        out_sum_file.write(line)
    out_sum_file.close()
        
            
        
