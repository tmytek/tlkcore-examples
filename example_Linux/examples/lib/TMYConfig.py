import json
import os
import re
import sys
sys.path.insert(0, os.path.abspath('.'))

class TMYConfig():
    def __init__(self, path):
        self.__config = None
        if not os.path.exists(path):
            print("Not exist!")
            return
        self.__config = self.__parse(path)

    def __parse(self, path):
        """ Parse a JSON file
            First remove comments and then use the json module package
            Comments look like :
                // ...
            or
                /*
                ...
                */
        """
        # Regular expression for comments
        comment_re = re.compile(
            '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
            re.DOTALL | re.MULTILINE
        )
        with open(path) as f:
            content = ''.join(f.readlines())
            ## Looking for comments
            match = comment_re.search(content)
            while match:
                # single line comment
                content = content[:match.start()] + content[match.end():]
                match = comment_re.search(content)

            # print content
            # Return json file
            return json.loads(content)

    def getConfig(self):
        if self.__config is None:
            return None
        return self.__config

if __name__ == '__main__':
    c = TMYConfig("config/device.conf")
    print(c.getConfig())