# -*- coding: utf-8 -*-

import os


class CLIItem:
    def __init__(self, name, function=None, value=None, enabled=True, subitems=[], tab_delimiter=" ", category=None):
        self._name = name
        self._function = function
        self._value = value
        self._enabled = enabled
        self._subitems = subitems
        self._tab_delimiter = tab_delimiter
        self._category = category

    def get_name(self):
        return self._name

    def get_completion_name(self):
        return self._name + self._tab_delimiter

    def get_function(self):
        return self._function

    def get_value(self):
        return self._value

    def is_enabled(self):
        return self._enabled

    def get_item_by_line(self, line):
        if line.startswith(self.get_completion_name()):
            item, args = line.split(self._tab_delimiter, 1)
            if not args:
                return self, args
            else:
                for i in self._subitems:
                    subitem = subargs = i.get_item_by_line(args)
                    if subitem is not None:
                        if subitem.get_function() is not None:
                            return subitem, subargs
                        else:
                            return self, args
                return self, args
        elif self._name == line:
            return self, ""
        else:
            return None, line

    def complete(self, line):
        matches = []
        if self._enabled:
            if line.startswith(self.get_completion_name()):
                item, args = line.split(self._tab_delimiter, 1)
                for s in self._subitems:
                    for i in s.complete(args):
                        matches.append(i)
            elif self.get_completion_name().startswith(line):
                matches.append(self)
        return matches


class CLISysPathItem(CLIItem):
    def __init__(self):
        CLIItem.__init__(self, "path_item")

    def _listdir(self, root):
        matches = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
            matches.append(name)
        return matches

    def _complete_path(self, path):
        matches = []
        if path == "":
            return self._listdir(".")
        dirname, filename_part = os.path.split(path)
        tmp_dirname = dirname if dirname else "."
        matches = [p for p in self._listdir(tmp_dirname) if p.startswith(filename_part)]
        if len(matches) > 1:
            return matches
        if os.path.isdir(os.path.join(dirname, matches[0])):
            return matches
        return [matches[0] + self._tab_delimiter]

    def complete(self, line):
        return self._complete_path(line)