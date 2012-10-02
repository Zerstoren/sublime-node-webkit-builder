#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2012, <Zerstoren>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sublime
import sublime_plugin
import zipfile
import os
import subprocess
import json


class Nodewebkit(sublime_plugin.TextCommand):
    settings = None

    def run(self, edit):
        """
        Compine project and execute this project for node-webkit
        """
        # Find folder where current file and file name
        folder, fileName = self.view.file_name().rsplit('/', 1)

        # If this is not a package.json, nothing to do here
        if fileName.replace('\n', '') != 'package.json':
            return False

        # Load plugin settings and project name
        settings = sublime.load_settings('node-webkit.sublime-settings')
        project = self.getProjectConfig()

        pathToSave = settings.get('save_to')

        if pathToSave != '.':
            folder = pathToSave

        # This is path and file name archive, but him don`t have standart name .zip
        # ZipFile can write zip archive without .zip extension
        archive = folder + '/' + project + '.nw'

        try:
            zf = zipfile.ZipFile(archive, mode='w')
        except:
            sublime.error_message('Error to create .nw file in Node Webkit')
            return False

        # Load from config data
        ignore = settings.get('ignore')
        for root, dirs, files in os.walk(folder):
            for item in files:
                path = root + '/' + item
                if item == project + '.nw':
                    continue

                next = False
                for i in ignore:
                    if path.find(i) != -1:
                        next = True
                        break

                if next == True:
                    continue

                # Write file to archive
                zf.write(path, path.replace(folder, ''))
        #except:
        #    sublime.error_message('Cannot add files to archive')
        #    return False

        zf.close()

        # if auto start is true, start the project
        if settings.get('autostart'):
            subprocess.Popen([settings.get('nw_command'), archive])

    def getProjectConfig(self):
        """
        Get the project name from package.json.
        """
        op = file(self.view.file_name().replace('\n', ''))
        jsonData = "".join(op.readlines())
        op.close()

        return json.loads(jsonData)['name']