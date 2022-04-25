#!/usr/bin/env python3

import os
import yaml


# Benchmark scripts use the include directive which is not required
# for this script to run, so let's stub it out.
class StubInclude():
    def __init__(self, path):
        self.path = path


def include_constructor(loader, node, Loader=yaml.SafeLoader):
    path = loader.construct_scalar(node)
    return StubInclude(path)


yaml.add_constructor(u'!include', include_constructor, Loader=yaml.SafeLoader)


def main():
    priorities = get_priorities()
    for key in sorted(priorities.keys()):
        print(key)
        for value in sorted(priorities[key]):
            print(' ', value)


def get_priorities():
    priorities = {}
    base_path = os.path.dirname(__file__)
    for root, dirs, files in os.walk(base_path):
        # ignore folder starting with a dot and the `common` directory
        # which is used for !include tag sources.
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'common']
        dirs.sort()

        # ignore folder starting with a dot
        files[:] = [f for f in files if f.endswith('.yaml')]
        files.sort()

        for f in files:
            path = os.path.join(root, f)
            relpath = os.path.relpath(path, base_path)
            collect_priorities(path, relpath, priorities)
    return priorities


def collect_priorities(path, relpath, priorities):
    with open(path, 'r') as h:
        data = yaml.load(h, Loader=yaml.SafeLoader)
    for key in sorted(data.keys()):
        if not key.endswith('_priority'):
            continue
        priority_value = data[key]
        if priority_value not in priorities:
            priorities[priority_value] = set([])
        priorities[priority_value].add(key + '::' + relpath)


if __name__ == '__main__':
    main()
