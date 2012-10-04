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
import subprocess
import json
import os


class Nodewebkit(sublime_plugin.TextCommand):
    settings = None

    def run(self, edit):
        """
        Compine project and execute this project for node-webkit
        """
        # Find folder where current file
        folder, fileName = self.view.file_name().rsplit('/', 1)

        # Load plugin settings
        self.settings = sublime.load_settings('node-webkit.sublime-settings')

        # Find project root folder
        # max deep is 100 folder
        for i in xrange(0, 100):
            print folder.encode('utf-8')
            try:
                fileDescriptor = open(folder + '/package.json', 'r')
            except:
                folderInfo = folder.rsplit('/', 1)
                if len(folderInfo) <= 1:
                    # We not find the need package file
                    sublime.status_message('Cannot start project, I dont find package.json')
                    return False
                elif folderInfo[0] == '/':
                    # If we comming to root folder, stop all
                    sublime.status_message('Cannot start project, I dont find package.json')
                    return False
                else:
                    folder = folderInfo[0]
            else:
                # Some sugar for try
                # If file open ok, lets move to next place
                break

        # Arguments for open NW project
        args = []
        # NW executable file
        args.append(self.settings.get('nw_command'))
        # NW flags open
        if self.settings.get('nw_flags'):
            args.append(self.settings.get('nw_flags'))
        # Project folder
        args.append(folder)

        subprocess.Popen(args)

        if self.settings.get('autopack'):
            self.compineProject(folder, fileDescriptor)
        else:
            fileDescriptor.close()

    def getProjectConfig(self, fileDescriptor):
        """
        Get the project name from package.json.
        """
        jsonData = "".join(fileDescriptor.readlines())
        fileDescriptor.close()

        return json.loads(jsonData)['name']

    def compineProject(self, folder, fileDescriptor):

        pathToSave = self.settings.get('save_to')

        if pathToSave != '.':
            folder = pathToSave

        # This is path and file name archive, but him don`t have standart name .zip
        # ZipFile can write zip archive without .zip extension
        project = self.getProjectConfig(fileDescriptor)
        archive = folder + '/' + project + '.nw'

        try:
            zf = zipfile.ZipFile(archive, mode='w')
        except:
            sublime.error_message('Error to create .nw file in Node Webkit')
            return False

        # Load from config data
        ignore = self.settings.get('ignore')
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

        zf.close()
