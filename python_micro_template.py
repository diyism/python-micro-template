# Copyright (c) DIYism (email/msn/gtalk:kexianbin@diyism.com web:http://diyism.com)
# Licensed under GPL (http://www.opensource.org/licenses/gpl-license.php) license.
# Version: ke1r

import re
import collections

class tpl:
    @staticmethod
    def re_sub_call(m):
        rtn=re.sub(r"\\", r"\\\\", m.group(0))
        rtn=re.sub("'", r"\'", rtn)
        return rtn

    @staticmethod
    def recursive_indent(arr, level):
        for i in range(len(arr)):
            if isinstance(arr[i], list):
                arr[i]=tpl.recursive_indent(arr[i], level+1)
            else:
                arr[i]=re.sub("#;#", "\n"+'    '*level, arr[i])
        return arr

    @staticmethod
    def flatten(l):
        for el in l:
            if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
                for sub in tpl.flatten(el):
                    yield sub
            else:
                yield el

    @staticmethod
    def parse(kvml):
        kvml=re.sub('<:', '\r', kvml)
        kvml=re.sub('(?:^|:>)[^\r]*', tpl.re_sub_call, kvml)
        kvml=re.sub('(?:\r)=(.*?)(?::>)', "\rwrite.append(\\1):>", kvml)
        kvml=re.sub('\r', "''')#;#", kvml)
        kvml=re.sub(':>', "#;#write.append('''", kvml)
        kvml="write=[]\nwrite.append('''"+kvml+"''')"
        kvml=re.sub(r"\\", r"\\\\", kvml)
        kvml=re.sub("'", r"\'", kvml)
        kvml=re.sub("#{#", "''',['''", kvml)
        kvml=re.sub("#}#", "'''],'''", kvml)
        kvml=eval("['''"+kvml+"''']")
        kvml=tpl.recursive_indent(kvml, 0)
        kvml=list(tpl.flatten(kvml))
        exec(''.join(kvml))
        kvml=''.join([str(x) for x in write])
        return kvml
