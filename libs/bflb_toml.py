# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bflb_toml.py
import re, sys, io, datetime
from datetime import tzinfo, timedelta
from os import linesep
from collections import OrderedDict
if sys.version_info < (3, ):
    _range = xrange
else:
    unicode = str
    _range = range
    basestring = str
    unichr = chr

def _detect_pathlib_path(p):
    if (3, 4) <= sys.version_info:
        import pathlib
        if isinstance(p, pathlib.PurePath):
            return True
    return False


def _ispath(p):
    if isinstance(p, basestring):
        return True
    return _detect_pathlib_path(p)


def _getpath(p):
    if (3, 6) <= sys.version_info:
        import os
        return os.fspath(p)
    if _detect_pathlib_path(p):
        return str(p)
    return p


try:
    FNFError = FileNotFoundError
except NameError:
    FNFError = IOError

TIME_RE = re.compile('([0-9]{2}):([0-9]{2}):([0-9]{2})(\\.([0-9]{3,6}))?')

class TomlDecodeError(ValueError):
    __doc__ = 'Base toml Exception / Error.'

    def __init__(self, msg, doc, pos):
        lineno = doc.count('\n', 0, pos) + 1
        colno = pos - doc.rfind('\n', 0, pos)
        emsg = '{} (line {} column {} char {})'.format(msg, lineno, colno, pos)
        ValueError.__init__(self, emsg)
        self.msg = msg
        self.doc = doc
        self.pos = pos
        self.lineno = lineno
        self.colno = colno


_number_with_underscores = re.compile('([0-9])(_([0-9]))*')

def _strictly_valid_num(n):
    n = n.strip()
    if not n:
        return False
    if n[0] == '_':
        return False
    if n[-1] == '_':
        return False
    if '_.' in n or '._' in n:
        return False
    if len(n) == 1:
        return True
    if n[0] == '0':
        if n[1] not in ('.', 'o', 'b', 'x'):
            return False
    if n[0] == '+' or n[0] == '-':
        n = n[1:]
        if len(n) > 1:
            if n[0] == '0':
                if n[1] != '.':
                    return False
    if '__' in n:
        return False
    return True


def load(f, _dict=dict, decoder=None):
    """Parses named file or files as toml and returns a dictionary

    Args:
        f: Path to the file to open, array of files to read into single dict
           or a file descriptor
        _dict: (optional) Specifies the class of the returned toml dictionary

    Returns:
        Parsed toml file represented as a dictionary

    Raises:
        TypeError -- When f is invalid type
        TomlDecodeError: Error while decoding toml
        IOError / FileNotFoundError -- When an array with no valid (existing)
        (Python 2 / Python 3)          file paths is passed
    """
    if _ispath(f):
        with io.open((_getpath(f)), encoding='utf-8') as (ffile):
            return loads(ffile.read(), _dict, decoder)
    else:
        if isinstance(f, list):
            from os import path as op
            from warnings import warn
            if not [path for path in f if op.exists(path)]:
                error_msg = 'Load expects a list to contain filenames only.'
                error_msg += linesep
                error_msg += 'The list needs to contain the path of at least one existing file.'
                raise FNFError(error_msg)
            if decoder is None:
                decoder = TomlDecoder()
            d = decoder.get_empty_table()
            for l in f:
                if op.exists(l):
                    d.update(load(l, _dict, decoder))
                else:
                    warn('Non-existent filename in list with at least one valid filename')

            return d
    try:
        return loads(f.read(), _dict, decoder)
    except AttributeError:
        raise TypeError('You can only load a file descriptor, filename or list')


_groupname_re = re.compile('^[A-Za-z0-9_-]+$')

def loads(s, _dict=dict, decoder=None):
    """Parses string as toml

    Args:
        s: String to be parsed
        _dict: (optional) Specifies the class of the returned toml dictionary

    Returns:
        Parsed toml file represented as a dictionary

    Raises:
        TypeError: When a non-string is passed
        TomlDecodeError: Error while decoding toml
    """
    implicitgroups = []
    if decoder is None:
        decoder = TomlDecoder(_dict)
    retval = decoder.get_empty_table()
    currentlevel = retval
    if not isinstance(s, basestring):
        raise TypeError('Expecting something like a string')
    if not isinstance(s, unicode):
        s = s.decode('utf8')
    original = s
    sl = list(s)
    openarr = 0
    openstring = False
    openstrchar = ''
    multilinestr = False
    arrayoftables = False
    beginline = True
    keygroup = False
    dottedkey = False
    keyname = 0
    for i, item in enumerate(sl):
        if item == '\r':
            if sl[i + 1] == '\n':
                sl[i] = ' '
                continue
            elif keyname:
                if item == '\n':
                    raise TomlDecodeError('Key name found without value. Reached end of line.', original, i)
                if openstring:
                    if item == openstrchar:
                        keyname = 2
                        openstring = False
                        openstrchar = ''
                        continue
                elif keyname == 1:
                    if item.isspace():
                        keyname = 2
                        continue
                elif item == '.':
                    dottedkey = True
                    continue
                else:
                    if item.isalnum() or item == '_' or item == '-':
                        continue
                    else:
                        if not dottedkey or sl[i - 1] == '.' and (item == '"' or item == "'"):
                            openstring = True
                            openstrchar = item
                            continue
            else:
                if keyname == 2:
                    if item.isspace():
                        if dottedkey:
                            nextitem = sl[i + 1]
                            if nextitem.isspace() or nextitem != '.':
                                keyname = 1
                                continue
                            if item == '.':
                                dottedkey = True
                                nextitem = sl[i + 1]
                                if nextitem.isspace() or nextitem != '.':
                                    keyname = 1
                                    continue
                            if item == '=':
                                keyname = 0
                                dottedkey = False
                            else:
                                raise TomlDecodeError("Found invalid character in key name: '" + item + "'. Try quoting the key name.", original, i)
                        if item == "'":
                            if openstrchar != '"':
                                k = 1
                                try:
                                    while sl[i - k] == "'":
                                        k += 1
                                        if k == 3:
                                            break

                                except IndexError:
                                    pass

                                if k == 3:
                                    multilinestr = not multilinestr
                                    openstring = multilinestr
                                else:
                                    openstring = not openstring
                                if openstring:
                                    openstrchar = "'"
                                else:
                                    openstrchar = ''
                        if item == '"':
                            if openstrchar != "'":
                                oddbackslash = False
                                k = 1
                                tripquote = False
                                try:
                                    while sl[i - k] == '"':
                                        k += 1
                                        if k == 3:
                                            tripquote = True
                                            break

                                    if (k == 1 or k) == 3:
                                        if tripquote:
                                            while sl[i - k] == '\\':
                                                oddbackslash = not oddbackslash
                                                k += 1

                                except IndexError:
                                    pass

                                if not oddbackslash:
                                    if tripquote:
                                        multilinestr = not multilinestr
                                        openstring = multilinestr
                                    else:
                                        openstring = not openstring
                                if openstring:
                                    openstrchar = '"'
                                else:
                                    openstrchar = ''
                        if item == '#' and not openstring or keygroup or arrayoftables:
                            j = i
                            try:
                                while sl[j] != '\n':
                                    sl[j] = ' '
                                    j += 1

                            except IndexError:
                                break

                            if item == '[' and not openstring:
                                if not keygroup:
                                    if not arrayoftables:
                                        if beginline:
                                            if len(sl) > i + 1 and sl[i + 1] == '[':
                                                arrayoftables = True
                            else:
                                keygroup = True
                else:
                    openarr += 1
            if item == ']' and not openstring:
                if keygroup:
                    keygroup = False
                else:
                    if arrayoftables:
                        if sl[i - 1] == ']':
                            arrayoftables = False
                        else:
                            openarr -= 1
                    elif item == '\n':
                        if openstring or multilinestr:
                            if not multilinestr:
                                raise TomlDecodeError('Unbalanced quotes', original, i)
                            if sl[i - 1] == "'" or sl[i - 1] == '"':
                                if sl[i - 2] == sl[i - 1]:
                                    sl[i] = sl[i - 1]
                                    if sl[i - 3] == sl[i - 1]:
                                        sl[i - 3] = ' '
                    elif openarr:
                        sl[i] = ' '
                    else:
                        beginline = True
            elif beginline:
                if sl[i] != ' ' and sl[i] != '\t':
                    beginline = False
                    if keygroup or arrayoftables or sl[i] == '=':
                        raise TomlDecodeError('Found empty keyname. ', original, i)
                keyname = 1

    s = ''.join(sl)
    s = s.split('\n')
    multikey = None
    multilinestr = ''
    multibackslash = False
    pos = 0
    for idx, line in enumerate(s):
        if idx > 0:
            pos += len(s[idx - 1]) + 1
        elif multilinestr:
            if multibackslash or '\n' not in multilinestr:
                line = line.strip()
            if line == '':
                if multikey:
                    if multibackslash:
                        continue
            if multikey:
                if multibackslash:
                    multilinestr += line
                else:
                    multilinestr += line
                multibackslash = False
                if len(line) > 2 and line[-1] == multilinestr[0]:
                    if line[-2] == multilinestr[0]:
                        if line[-3] == multilinestr[0]:
                            try:
                                value, vtype = decoder.load_value(multilinestr)
                            except ValueError as err:
                                try:
                                    raise TomlDecodeError(str(err), original, pos)
                                finally:
                                    err = None
                                    del err

                            currentlevel[multikey] = value
                            multikey = None
                            multilinestr = ''
                    k = len(multilinestr) - 1
                    while k > -1 and multilinestr[k] == '\\':
                        multibackslash = not multibackslash
                        k -= 1

                    if multibackslash:
                        multilinestr = multilinestr[:-1]
                else:
                    multilinestr += '\n'
                    continue
            if line[0] == '[':
                arrayoftables = False
                if len(line) == 1:
                    raise TomlDecodeError('Opening key group bracket on line by itself.', original, pos)
                if line[1] == '[':
                    arrayoftables = True
                    line = line[2:]
                    splitstr = ']]'
        else:
            line = line[1:]
            splitstr = ']'
        i = 1
        quotesplits = decoder._get_split_on_quotes(line)
        quoted = False
        for quotesplit in quotesplits:
            if not quoted:
                if splitstr in quotesplit:
                    break
                i += quotesplit.count(splitstr)
                quoted = not quoted

        line = line.split(splitstr, i)
        if not len(line) < i + 1:
            if line[-1].strip() != '':
                raise TomlDecodeError('Key group not on a line by itself.', original, pos)
            groups = splitstr.join(line[:-1]).split('.')
            i = 0
            while i < len(groups):
                groups[i] = groups[i].strip()
                if not len(groups[i]) > 0 or groups[i][0] == '"' or groups[i][0] == "'":
                    groupstr = groups[i]
                    j = i + 1
                    while not groupstr[0] == groupstr[-1]:
                        j += 1
                        if j > len(groups) + 2:
                            raise TomlDecodeError("Invalid group name '" + groupstr + "' Something " + 'went wrong.', original, pos)
                        groupstr = '.'.join(groups[i:j]).strip()

                    groups[i] = groupstr[1:-1]
                    groups[i + 1:j] = []
                else:
                    if not _groupname_re.match(groups[i]):
                        raise TomlDecodeError("Invalid group name '" + groups[i] + "'. Try quoting it.", original, pos)
                    i += 1

            currentlevel = retval
            for i in _range(len(groups)):
                group = groups[i]
                if group == '':
                    raise TomlDecodeError("Can't have a keygroup with an empty name", original, pos)
                try:
                    currentlevel[group]
                    if i == len(groups) - 1:
                        if group in implicitgroups:
                            implicitgroups.remove(group)
                            if arrayoftables:
                                raise TomlDecodeError("An implicitly defined table can't be an array", original, pos)
                        elif arrayoftables:
                            currentlevel[group].append(decoder.get_empty_table())
                        else:
                            raise TomlDecodeError('What? ' + group + ' already exists?' + str(currentlevel), original, pos)
                except TypeError:
                    currentlevel = currentlevel[-1]
                    if group not in currentlevel:
                        currentlevel[group] = decoder.get_empty_table()
                        if i == len(groups) - 1:
                            if arrayoftables:
                                currentlevel[group] = [
                                 decoder.get_empty_table()]
                except KeyError:
                    if i != len(groups) - 1:
                        implicitgroups.append(group)
                    currentlevel[group] = decoder.get_empty_table()
                    if i == len(groups) - 1:
                        if arrayoftables:
                            currentlevel[group] = [
                             decoder.get_empty_table()]

                currentlevel = currentlevel[group]
                if arrayoftables:
                    try:
                        currentlevel = currentlevel[-1]
                    except KeyError:
                        pass

        elif line[0] == '{':
            if line[-1] != '}':
                raise TomlDecodeError('Line breaks are not allowed in inlineobjects', original, pos)
            try:
                decoder.load_inline_object(line, currentlevel, multikey, multibackslash)
            except ValueError as err:
                try:
                    raise TomlDecodeError(str(err), original, pos)
                finally:
                    err = None
                    del err

        elif '=' in line:
            try:
                ret = decoder.load_line(line, currentlevel, multikey, multibackslash)
            except ValueError as err:
                try:
                    raise TomlDecodeError(str(err), original, pos)
                finally:
                    err = None
                    del err

            if ret is not None:
                multikey, multilinestr, multibackslash = ret

    return retval


def _load_date(val):
    microsecond = 0
    tz = None
    try:
        if len(val) > 19:
            if val[19] == '.':
                if val[-1].upper() == 'Z':
                    subsecondval = val[20:-1]
                    tzval = 'Z'
                else:
                    subsecondvalandtz = val[20:]
                    if '+' in subsecondvalandtz:
                        splitpoint = subsecondvalandtz.index('+')
                        subsecondval = subsecondvalandtz[:splitpoint]
                        tzval = subsecondvalandtz[splitpoint:]
                    else:
                        if '-' in subsecondvalandtz:
                            splitpoint = subsecondvalandtz.index('-')
                            subsecondval = subsecondvalandtz[:splitpoint]
                            tzval = subsecondvalandtz[splitpoint:]
                        else:
                            tzval = None
                            subsecondval = subsecondvalandtz
                if tzval is not None:
                    tz = TomlTz(tzval)
                microsecond = int(int(subsecondval) * 10 ** (6 - len(subsecondval)))
            else:
                tz = TomlTz(val[19:])
    except ValueError:
        tz = None

    if '-' not in val[1:]:
        return
    try:
        if len(val) == 10:
            d = datetime.date(int(val[:4]), int(val[5:7]), int(val[8:10]))
        else:
            d = datetime.datetime(int(val[:4]), int(val[5:7]), int(val[8:10]), int(val[11:13]), int(val[14:16]), int(val[17:19]), microsecond, tz)
    except ValueError:
        return
    else:
        return d


def _load_unicode_escapes(v, hexbytes, prefix):
    skip = False
    i = len(v) - 1
    while i > -1 and v[i] == '\\':
        skip = not skip
        i -= 1

    for hx in hexbytes:
        if skip:
            skip = False
            i = len(hx) - 1
            while i > -1 and hx[i] == '\\':
                skip = not skip
                i -= 1

            v += prefix
            v += hx
            continue
        hxb = ''
        i = 0
        hxblen = 4
        if prefix == '\\U':
            hxblen = 8
        hxb = ''.join(hx[i:i + hxblen]).lower()
        if hxb.strip('0123456789abcdef'):
            raise ValueError('Invalid escape sequence: ' + hxb)
        if hxb[0] == 'd':
            if hxb[1].strip('01234567'):
                raise ValueError('Invalid escape sequence: ' + hxb + '. Only scalar unicode points are allowed.')
        v += unichr(int(hxb, 16))
        v += unicode(hx[len(hxb):])

    return v


_escapes = [
 "'0'", "'b'", "'f'", "'n'", "'r'", "'t'", '\'"\'']
_escapedchars = [
 "'\\x00'", "'\\x08'", "'\\x0c'", "'\\n'", "'\\r'", "'\\t'", '\'"\'']
_escape_to_escapedchars = dict(zip(_escapes, _escapedchars))

def _unescape(v):
    """Unescape characters in a TOML string."""
    i = 0
    backslash = False
    while i < len(v):
        if backslash:
            backslash = False
            if v[i] in _escapes:
                v = v[:i - 1] + _escape_to_escapedchars[v[i]] + v[i + 1:]
        elif v[i] == '\\':
            v = v[:i - 1] + v[i:]
        else:
            if not v[i] == 'u':
                if v[i] == 'U':
                    i += 1
                else:
                    raise ValueError('Reserved escape sequence used')
                continue
            elif v[i] == '\\':
                backslash = True
            i += 1

    return v


class InlineTableDict(object):
    __doc__ = 'Sentinel subclass of dict for inline tables.'


class TomlDecoder(object):

    def __init__(self, _dict=dict):
        self._dict = _dict

    def get_empty_table(self):
        return self._dict()

    def get_empty_inline_table(self):

        class DynamicInlineTableDict(self._dict, InlineTableDict):
            __doc__ = 'Concrete sentinel subclass for inline tables.\n            It is a subclass of _dict which is passed in dynamically at load\n            time\n\n            It is also a subclass of InlineTableDict\n            '

        return DynamicInlineTableDict()

    def load_inline_object--- This code section failed: ---

 L. 582         0  LOAD_FAST                'line'
                2  LOAD_CONST               1
                4  LOAD_CONST               -1
                6  BUILD_SLICE_2         2 
                8  BINARY_SUBSCR    
               10  LOAD_METHOD              split
               12  LOAD_STR                 ','
               14  CALL_METHOD_1         1  '1 positional argument'
               16  STORE_FAST               'candidate_groups'

 L. 583        18  BUILD_LIST_0          0 
               20  STORE_FAST               'groups'

 L. 584        22  LOAD_GLOBAL              len
               24  LOAD_FAST                'candidate_groups'
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  LOAD_CONST               1
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    54  'to 54'
               34  LOAD_FAST                'candidate_groups'
               36  LOAD_CONST               0
               38  BINARY_SUBSCR    
               40  LOAD_METHOD              strip
               42  CALL_METHOD_0         0  '0 positional arguments'
               44  POP_JUMP_IF_TRUE     54  'to 54'

 L. 585        46  LOAD_FAST                'candidate_groups'
               48  LOAD_METHOD              pop
               50  CALL_METHOD_0         0  '0 positional arguments'
               52  POP_TOP          
             54_0  COME_FROM            44  '44'
             54_1  COME_FROM            32  '32'

 L. 586        54  SETUP_LOOP          294  'to 294'
               56  LOAD_GLOBAL              len
               58  LOAD_FAST                'candidate_groups'
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  LOAD_CONST               0
               64  COMPARE_OP               >
            66_68  POP_JUMP_IF_FALSE   292  'to 292'

 L. 587        70  LOAD_FAST                'candidate_groups'
               72  LOAD_METHOD              pop
               74  LOAD_CONST               0
               76  CALL_METHOD_1         1  '1 positional argument'
               78  STORE_FAST               'candidate_group'

 L. 588        80  SETUP_EXCEPT        102  'to 102'

 L. 589        82  LOAD_FAST                'candidate_group'
               84  LOAD_METHOD              split
               86  LOAD_STR                 '='
               88  LOAD_CONST               1
               90  CALL_METHOD_2         2  '2 positional arguments'
               92  UNPACK_SEQUENCE_2     2 
               94  STORE_FAST               '_'
               96  STORE_FAST               'value'
               98  POP_BLOCK        
              100  JUMP_FORWARD        130  'to 130'
            102_0  COME_FROM_EXCEPT     80  '80'

 L. 590       102  DUP_TOP          
              104  LOAD_GLOBAL              ValueError
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   128  'to 128'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 591       116  LOAD_GLOBAL              ValueError
              118  LOAD_STR                 'Invalid inline table encountered'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  RAISE_VARARGS_1       1  'exception instance'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
            128_0  COME_FROM           108  '108'
              128  END_FINALLY      
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM           100  '100'

 L. 592       130  LOAD_FAST                'value'
              132  LOAD_METHOD              strip
              134  CALL_METHOD_0         0  '0 positional arguments'
              136  STORE_FAST               'value'

 L. 593       138  LOAD_FAST                'value'
              140  LOAD_CONST               0
              142  BINARY_SUBSCR    
              144  LOAD_FAST                'value'
              146  LOAD_CONST               -1
              148  BINARY_SUBSCR    
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   166  'to 166'
              154  LOAD_FAST                'value'
              156  LOAD_CONST               0
              158  BINARY_SUBSCR    
              160  LOAD_CONST               ('"', "'")
              162  COMPARE_OP               in
              164  POP_JUMP_IF_TRUE    234  'to 234'
            166_0  COME_FROM           152  '152'

 L. 594       166  LOAD_FAST                'value'
              168  LOAD_CONST               0
              170  BINARY_SUBSCR    
              172  LOAD_STR                 '-0123456789'
              174  COMPARE_OP               in
              176  POP_JUMP_IF_TRUE    234  'to 234'
              178  LOAD_FAST                'value'
              180  LOAD_CONST               ('true', 'false')
              182  COMPARE_OP               in
              184  POP_JUMP_IF_TRUE    234  'to 234'

 L. 595       186  LOAD_FAST                'value'
              188  LOAD_CONST               0
              190  BINARY_SUBSCR    
              192  LOAD_STR                 '['
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_FALSE   210  'to 210'
              198  LOAD_FAST                'value'
              200  LOAD_CONST               -1
              202  BINARY_SUBSCR    
              204  LOAD_STR                 ']'
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_TRUE    234  'to 234'
            210_0  COME_FROM           196  '196'

 L. 596       210  LOAD_FAST                'value'
              212  LOAD_CONST               0
              214  BINARY_SUBSCR    
              216  LOAD_STR                 '{'
              218  COMPARE_OP               ==
              220  POP_JUMP_IF_FALSE   246  'to 246'
              222  LOAD_FAST                'value'
              224  LOAD_CONST               -1
              226  BINARY_SUBSCR    
              228  LOAD_STR                 '}'
              230  COMPARE_OP               ==
              232  POP_JUMP_IF_FALSE   246  'to 246'
            234_0  COME_FROM           208  '208'
            234_1  COME_FROM           184  '184'
            234_2  COME_FROM           176  '176'
            234_3  COME_FROM           164  '164'

 L. 597       234  LOAD_FAST                'groups'
              236  LOAD_METHOD              append
              238  LOAD_FAST                'candidate_group'
              240  CALL_METHOD_1         1  '1 positional argument'
              242  POP_TOP          
              244  JUMP_BACK            56  'to 56'
            246_0  COME_FROM           232  '232'
            246_1  COME_FROM           220  '220'

 L. 598       246  LOAD_GLOBAL              len
              248  LOAD_FAST                'candidate_groups'
              250  CALL_FUNCTION_1       1  '1 positional argument'
              252  LOAD_CONST               0
              254  COMPARE_OP               >
          256_258  POP_JUMP_IF_FALSE   282  'to 282'

 L. 599       260  LOAD_FAST                'candidate_group'
              262  LOAD_STR                 ','
              264  BINARY_ADD       
              266  LOAD_FAST                'candidate_groups'
              268  LOAD_CONST               0
              270  BINARY_SUBSCR    
              272  BINARY_ADD       
              274  LOAD_FAST                'candidate_groups'
              276  LOAD_CONST               0
              278  STORE_SUBSCR     
              280  JUMP_BACK            56  'to 56'
            282_0  COME_FROM           256  '256'

 L. 601       282  LOAD_GLOBAL              ValueError
              284  LOAD_STR                 'Invalid inline table value encountered'
              286  CALL_FUNCTION_1       1  '1 positional argument'
              288  RAISE_VARARGS_1       1  'exception instance'
              290  JUMP_BACK            56  'to 56'
            292_0  COME_FROM            66  '66'
              292  POP_BLOCK        
            294_0  COME_FROM_LOOP       54  '54'

 L. 602       294  SETUP_LOOP          338  'to 338'
              296  LOAD_FAST                'groups'
              298  GET_ITER         
            300_0  COME_FROM           326  '326'
              300  FOR_ITER            336  'to 336'
              302  STORE_FAST               'group'

 L. 603       304  LOAD_FAST                'self'
              306  LOAD_METHOD              load_line
              308  LOAD_FAST                'group'
              310  LOAD_FAST                'currentlevel'
              312  LOAD_FAST                'multikey'
              314  LOAD_FAST                'multibackslash'
              316  CALL_METHOD_4         4  '4 positional arguments'
              318  STORE_FAST               'status'

 L. 604       320  LOAD_FAST                'status'
              322  LOAD_CONST               None
              324  COMPARE_OP               is-not
          326_328  POP_JUMP_IF_FALSE   300  'to 300'

 L. 605       330  BREAK_LOOP       
          332_334  JUMP_BACK           300  'to 300'
              336  POP_BLOCK        
            338_0  COME_FROM_LOOP      294  '294'

Parse error at or near `COME_FROM' instruction at offset 246_1

    def _get_split_on_quotes(self, line):
        doublequotesplits = line.split('"')
        quoted = False
        quotesplits = []
        if len(doublequotesplits) > 1:
            if "'" in doublequotesplits[0]:
                singlequotesplits = doublequotesplits[0].split("'")
                doublequotesplits = doublequotesplits[1:]
                while len(singlequotesplits) % 2 == 0 and len(doublequotesplits):
                    singlequotesplits[-1] += '"' + doublequotesplits[0]
                    doublequotesplits = doublequotesplits[1:]
                    if "'" in singlequotesplits[-1]:
                        singlequotesplits = singlequotesplits[:-1] + singlequotesplits[-1].split("'")

                quotesplits += singlequotesplits
        for doublequotesplit in doublequotesplits:
            if quoted:
                quotesplits.append(doublequotesplit)
            else:
                quotesplits += doublequotesplit.split("'")
                quoted = not quoted

        return quotesplits

    def load_line(self, line, currentlevel, multikey, multibackslash):
        i = 1
        quotesplits = self._get_split_on_quotes(line)
        quoted = False
        for quotesplit in quotesplits:
            if not quoted:
                if '=' in quotesplit:
                    break
            i += quotesplit.count('=')
            quoted = not quoted

        pair = line.split('=', i)
        strictly_valid = _strictly_valid_num(pair[-1])
        if _number_with_underscores.match(pair[-1]):
            pair[-1] = pair[-1].replace('_', '')
        while len(pair[-1]) and pair[-1][0] != ' ' and pair[-1][0] != '\t' and pair[-1][0] != "'" and pair[-1][0] != '"' and pair[-1][0] != '[' and pair[-1][0] != '{' and pair[-1] != 'true' and pair[-1] != 'false':
            try:
                float(pair[-1])
                break
            except ValueError:
                pass

            if _load_date(pair[-1]) is not None:
                break
            i += 1
            prev_val = pair[-1]
            pair = line.split('=', i)
            if prev_val == pair[-1]:
                raise ValueError('Invalid date or number')
            if strictly_valid:
                strictly_valid = _strictly_valid_num(pair[-1])

        pair = [
         '='.join(pair[:-1]).strip(), pair[-1].strip()]
        if '.' in pair[0]:
            if '"' in pair[0] or "'" in pair[0]:
                quotesplits = self._get_split_on_quotes(pair[0])
                quoted = False
                levels = []
                for quotesplit in quotesplits:
                    if quoted:
                        levels.append(quotesplit)
                    else:
                        levels += [level.strip() for level in quotesplit.split('.')]
                    quoted = not quoted

            else:
                levels = pair[0].split('.')
            while levels[-1] == '':
                levels = levels[:-1]

            for level in levels[:-1]:
                if level == '':
                    continue
                if level not in currentlevel:
                    currentlevel[level] = self.get_empty_table()
                currentlevel = currentlevel[level]

            pair[0] = levels[-1].strip()
        else:
            if not pair[0][0] == '"':
                if pair[0][0] == "'":
                    if pair[0][-1] == pair[0][0]:
                        pair[0] = pair[0][1:-1]
                if not len(pair[1]) > 2 or pair[1][0] == '"' or pair[1][0] == "'":
                    if pair[1][1] == pair[1][0] and pair[1][2] == pair[1][0]:
                        if len(pair[1]) > 5:
                            if pair[1][-1] == pair[1][0]:
                                if not (pair[1][-2] == pair[1][0] and pair[1][-3] == pair[1][0]):
                                    k = len(pair[1]) - 1
                                    while k > -1 and pair[1][k] == '\\':
                                        multibackslash = not multibackslash
                                        k -= 1

                                    if multibackslash:
                                        multilinestr = pair[1][:-1]
                else:
                    multilinestr = pair[1] + '\n'
                multikey = pair[0]
            else:
                value, vtype = self.load_value(pair[1], strictly_valid)
            try:
                currentlevel[pair[0]]
                raise ValueError('Duplicate keys!')
            except TypeError:
                raise ValueError('Duplicate keys!')
            except KeyError:
                if multikey:
                    return (
                     multikey, multilinestr, multibackslash)
                currentlevel[pair[0]] = value

    def load_value(self, v, strictly_valid=True):
        if not v:
            raise ValueError('Empty value is invalid')
        else:
            if v == 'true':
                return (True, 'bool')
            if v == 'false':
                return (False, 'bool')
            if v[0] == '"' or v[0] == "'":
                quotechar = v[0]
                testv = v[1:].split(quotechar)
                triplequote = False
                triplequotecount = 0
                if len(testv) > 1:
                    if testv[0] == '':
                        if testv[1] == '':
                            testv = testv[2:]
                            triplequote = True
                closed = False
                for tv in testv:
                    if tv == '':
                        if triplequote:
                            triplequotecount += 1
                        else:
                            closed = True

                if quotechar == '"':
                    escapeseqs = v.split('\\')[1:]
                    backslash = False
                    for i in escapeseqs:
                        if i == '':
                            backslash = not backslash
                        elif i[0] not in _escapes and i[0] != 'u' and i[0] != 'U':
                            if not backslash:
                                raise ValueError('Reserved escape sequence used')
                        if backslash:
                            backslash = False

                    for prefix in ('\\u', '\\U'):
                        if prefix in v:
                            hexbytes = v.split(prefix)
                            v = _load_unicode_escapes(hexbytes[0], hexbytes[1:], prefix)

                    v = _unescape(v)
                if len(v) > 1 and v[1] == quotechar and not len(v) < 3:
                    if v[1] == v[2]:
                        v = v[2:-2]
                return (
                 v[1:-1], 'str')
            if v[0] == '[':
                return (
                 self.load_array(v), 'array')
            if v[0] == '{':
                inline_object = self.get_empty_inline_table()
                self.load_inline_object(v, inline_object)
                return (inline_object, 'inline_object')
            if TIME_RE.match(v):
                h, m, s, _, ms = TIME_RE.match(v).groups()
                time = datetime.time(int(h), int(m), int(s), int(ms) if ms else 0)
                return (time, 'time')
            parsed_date = _load_date(v)
            if parsed_date is not None:
                return (
                 parsed_date, 'date')
            assert strictly_valid, 'Weirdness with leading zeroes or underscores in your number.'
        itype = 'int'
        neg = False
        if v[0] == '-':
            neg = True
            v = v[1:]
        else:
            if v[0] == '+':
                v = v[1:]
            else:
                v = v.replace('_', '')
                lowerv = v.lower()
                if not ('.' in v or 'x') not in v or 'e' in v or 'E' in v:
                    if '.' in v:
                        if v.split('.', 1)[1] == '':
                            raise ValueError('This float is missing digits after the point')
                        if v[0] not in '0123456789':
                            raise ValueError("This float doesn't have a leading digit")
                        v = float(v)
                        itype = 'float'
                    else:
                        pass
                if len(lowerv) == 3 and not lowerv == 'inf':
                    if lowerv == 'nan':
                        v = float(v)
                        itype = 'float'
            if itype == 'int':
                v = int(v, 0)
            if neg:
                return (
                 0 - v, itype)
            return (
             v, itype)

    def bounded_string(self, s):
        if len(s) == 0:
            return True
        if s[-1] != s[0]:
            return False
        i = -2
        backslash = False
        while len(s) + i > 0:
            if s[i] == '\\':
                backslash = not backslash
                i -= 1
            else:
                break

        return not backslash

    def load_array(self, a):
        atype = None
        retval = []
        a = a.strip()
        if '[' not in a[1:-1] or '' != a[1:-1].split('[')[0].strip():
            strarray = False
            tmpa = a[1:-1].strip()
            if tmpa != '':
                if tmpa[0] == '"' or tmpa[0] == "'":
                    strarray = True
            if not a[1:-1].strip().startswith('{'):
                a = a[1:-1].split(',')
            else:
                new_a = []
                start_group_index = 1
                end_group_index = 2
                in_str = False
                while end_group_index < len(a[1:]) and not a[end_group_index] == '"':
                    if a[end_group_index] == "'":
                        if in_str:
                            backslash_index = end_group_index - 1
                            while backslash_index > -1 and a[backslash_index] == '\\':
                                in_str = not in_str
                                backslash_index -= 1

                        in_str = not in_str
                    if in_str or a[end_group_index] != '}':
                        end_group_index += 1
                        continue
                    end_group_index += 1
                    new_a.append(a[start_group_index:end_group_index])
                    start_group_index = end_group_index + 1
                    while start_group_index < len(a[1:]) and a[start_group_index] != '{':
                        start_group_index += 1

                    end_group_index = start_group_index + 1

                a = new_a
            b = 0
            if strarray:
                while b < len(a) - 1:
                    ab = a[b].strip()
                    while self.bounded_string(ab):
                        if len(ab) > 2:
                            if ab[0] == ab[1] == ab[2]:
                                if not ab[-2] != ab[0] or ab[-3] != ab[0]:
                                    a[b] = a[b] + ',' + a[b + 1]
                                    ab = a[b].strip()
                                    if b < len(a) - 2:
                                        a = a[:b + 1] + a[b + 2:]
                                    else:
                                        a = a[:b + 1]

                    b += 1

        else:
            al = list(a[1:-1])
            a = []
            openarr = 0
            j = 0
            for i in _range(len(al)):
                if al[i] == '[':
                    openarr += 1
                else:
                    if al[i] == ']':
                        openarr -= 1

            a.append(''.join(al[j:]))
        for i in _range(len(a)):
            a[i] = a[i].strip()
            if a[i] != '':
                nval, ntype = self.load_value(a[i])
                if atype:
                    if ntype != atype:
                        raise ValueError('Not a homogeneous array')
                else:
                    atype = ntype
                retval.append(nval)

        return retval


def dump(o, f):
    """Writes out dict as toml to a file

    Args:
        o: Object to dump into toml
        f: File descriptor where the toml should be stored

    Returns:
        String containing the toml corresponding to dictionary

    Raises:
        TypeError: When anything other than file descriptor is passed
    """
    if not f.write:
        raise TypeError('You can only dump an object to a file descriptor')
    d = dumps(o)
    f.write(d)
    return d


def dumps(o, encoder=None):
    """Stringifies input dict as toml

    Args:
        o: Object to dump into toml

        preserve: Boolean parameter. If true, preserve inline tables.

    Returns:
        String containing the toml corresponding to dict
    """
    retval = ''
    if encoder is None:
        encoder = TomlEncoder(o.__class__)
    addtoretval, sections = encoder.dump_sections(o, '')
    retval += addtoretval
    while sections:
        newsections = encoder.get_empty_table()
        for section in sections:
            addtoretval, addtosections = encoder.dump_sections(sections[section], section)
            if not addtoretval:
                if not addtoretval:
                    if not addtosections:
                        if retval:
                            if retval[-2:] != '\n\n':
                                retval += '\n'
                        retval += '[' + section + ']\n'
                        if addtoretval:
                            retval += addtoretval
                for s in addtosections:
                    newsections[section + '.' + s] = addtosections[s]

        sections = newsections

    return retval


def _dump_str(v):
    if sys.version_info < (3, ):
        if hasattr(v, 'decode'):
            if isinstance(v, str):
                v = v.decode('utf-8')
    v = '%r' % v
    if v[0] == 'u':
        v = v[1:]
    singlequote = v.startswith("'")
    if singlequote or v.startswith('"'):
        v = v[1:-1]
    if singlequote:
        v = v.replace("\\'", "'")
        v = v.replace('"', '\\"')
    f = v[:]
    v = v.split('\\x')
    while len(v) > 1:
        i = -1
        if not v[0]:
            v = v[1:]
        else:
            v[0] = v[0].replace('\\\\', '\\')
            joinx = v[0][i] != '\\'
            while v[0][:i] and v[0][i] == '\\':
                joinx = not joinx
                i -= 1

            if joinx:
                joiner = 'x'
            else:
                joiner = 'u00'
        v = [
         v[0] + joiner + v[1]] + v[2:]
        import os
        if os.path.isfile(f):
            v[0] = v[0].replace('\\', '\\\\')

    return unicode('"' + v[0] + '"')


def _dump_float(v):
    return '{0:.16}'.format(v).replace('e+0', 'e+').replace('e-0', 'e-')


def _dump_time(v):
    utcoffset = v.utcoffset()
    if utcoffset is None:
        return v.isoformat()
    return v.isoformat()[:-6]


class TomlEncoder(object):

    def __init__(self, _dict=dict, preserve=False):
        self._dict = _dict
        self.preserve = preserve
        self.dump_funcs = {str: _dump_str, 
         unicode: _dump_str, 
         list: self.dump_list, 
         bool: lambda v: unicode(v).lower(), 
         int: lambda v: v, 
         float: _dump_float, 
         datetime.datetime: lambda v: v.isoformat().replace('+00:00', 'Z'), 
         datetime.time: _dump_time, 
         datetime.date: lambda v: v.isoformat()}

    def get_empty_table(self):
        return self._dict()

    def dump_list(self, v):
        retval = '['
        for u in v:
            retval += ' ' + unicode(self.dump_value(u)) + ','

        retval += ']'
        return retval

    def dump_inline_table(self, section):
        """Preserve inline table in its compact syntax instead of expanding
        into subsection.

        https://github.com/toml-lang/toml#user-content-inline-table
        """
        retval = ''
        if isinstance(section, dict):
            val_list = []
            for k, v in section.items():
                val = self.dump_inline_table(v)
                val_list.append(k + ' = ' + val)

            retval += '{ ' + ', '.join(val_list) + ' }\n'
            return retval
        return unicode(self.dump_value(section))

    def dump_value(self, v):
        dump_fn = self.dump_funcs.get(type(v))
        if dump_fn is None:
            if hasattr(v, '__iter__'):
                dump_fn = self.dump_funcs[list]
        if dump_fn is not None:
            return dump_fn(v)
        return self.dump_funcs[str](v)

    def dump_sections--- This code section failed: ---

 L.1068         0  LOAD_STR                 ''
                2  STORE_FAST               'retstr'

 L.1069         4  LOAD_FAST                'sup'
                6  LOAD_STR                 ''
                8  COMPARE_OP               !=
               10  POP_JUMP_IF_FALSE    32  'to 32'
               12  LOAD_FAST                'sup'
               14  LOAD_CONST               -1
               16  BINARY_SUBSCR    
               18  LOAD_STR                 '.'
               20  COMPARE_OP               !=
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L.1070        24  LOAD_FAST                'sup'
               26  LOAD_STR                 '.'
               28  INPLACE_ADD      
               30  STORE_FAST               'sup'
             32_0  COME_FROM            22  '22'
             32_1  COME_FROM            10  '10'

 L.1071        32  LOAD_FAST                'self'
               34  LOAD_METHOD              _dict
               36  CALL_METHOD_0         0  '0 positional arguments'
               38  STORE_FAST               'retdict'

 L.1072        40  LOAD_STR                 ''
               42  STORE_FAST               'arraystr'

 L.1073     44_46  SETUP_LOOP          570  'to 570'
               48  LOAD_FAST                'o'
               50  GET_ITER         
            52_54  FOR_ITER            568  'to 568'
               56  STORE_FAST               'section'

 L.1074        58  LOAD_GLOBAL              unicode
               60  LOAD_FAST                'section'
               62  CALL_FUNCTION_1       1  '1 positional argument'
               64  STORE_FAST               'section'

 L.1075        66  LOAD_FAST                'section'
               68  STORE_FAST               'qsection'

 L.1076        70  LOAD_GLOBAL              re
               72  LOAD_METHOD              match
               74  LOAD_STR                 '^[A-Za-z0-9_-]+$'
               76  LOAD_FAST                'section'
               78  CALL_METHOD_2         2  '2 positional arguments'
               80  POP_JUMP_IF_TRUE    116  'to 116'

 L.1077        82  LOAD_STR                 '"'
               84  LOAD_FAST                'section'
               86  COMPARE_OP               in
               88  POP_JUMP_IF_FALSE   104  'to 104'

 L.1078        90  LOAD_STR                 "'"
               92  LOAD_FAST                'section'
               94  BINARY_ADD       
               96  LOAD_STR                 "'"
               98  BINARY_ADD       
              100  STORE_FAST               'qsection'
              102  JUMP_FORWARD        116  'to 116'
            104_0  COME_FROM            88  '88'

 L.1080       104  LOAD_STR                 '"'
              106  LOAD_FAST                'section'
              108  BINARY_ADD       
              110  LOAD_STR                 '"'
              112  BINARY_ADD       
              114  STORE_FAST               'qsection'
            116_0  COME_FROM           102  '102'
            116_1  COME_FROM            80  '80'

 L.1081       116  LOAD_GLOBAL              isinstance
              118  LOAD_FAST                'o'
              120  LOAD_FAST                'section'
              122  BINARY_SUBSCR    
              124  LOAD_GLOBAL              dict
              126  CALL_FUNCTION_2       2  '2 positional arguments'
          128_130  POP_JUMP_IF_TRUE    502  'to 502'

 L.1082       132  LOAD_CONST               False
              134  STORE_FAST               'arrayoftables'

 L.1083       136  LOAD_GLOBAL              isinstance
              138  LOAD_FAST                'o'
              140  LOAD_FAST                'section'
              142  BINARY_SUBSCR    
              144  LOAD_GLOBAL              list
              146  CALL_FUNCTION_2       2  '2 positional arguments'
              148  POP_JUMP_IF_FALSE   182  'to 182'

 L.1084       150  SETUP_LOOP          182  'to 182'
              152  LOAD_FAST                'o'
              154  LOAD_FAST                'section'
              156  BINARY_SUBSCR    
              158  GET_ITER         
            160_0  COME_FROM           172  '172'
              160  FOR_ITER            180  'to 180'
              162  STORE_FAST               'a'

 L.1085       164  LOAD_GLOBAL              isinstance
              166  LOAD_FAST                'a'
              168  LOAD_GLOBAL              dict
              170  CALL_FUNCTION_2       2  '2 positional arguments'
              172  POP_JUMP_IF_FALSE   160  'to 160'

 L.1086       174  LOAD_CONST               True
              176  STORE_FAST               'arrayoftables'
              178  JUMP_BACK           160  'to 160'
              180  POP_BLOCK        
            182_0  COME_FROM_LOOP      150  '150'
            182_1  COME_FROM           148  '148'

 L.1087       182  LOAD_FAST                'arrayoftables'
          184_186  POP_JUMP_IF_FALSE   452  'to 452'

 L.1088   188_190  SETUP_LOOP          500  'to 500'
              192  LOAD_FAST                'o'
              194  LOAD_FAST                'section'
              196  BINARY_SUBSCR    
              198  GET_ITER         
              200  FOR_ITER            448  'to 448'
              202  STORE_FAST               'a'

 L.1089       204  LOAD_STR                 '\n'
              206  STORE_FAST               'arraytabstr'

 L.1090       208  LOAD_FAST                'arraystr'
              210  LOAD_STR                 '[['
              212  LOAD_FAST                'sup'
              214  BINARY_ADD       
              216  LOAD_FAST                'qsection'
              218  BINARY_ADD       
              220  LOAD_STR                 ']]\n'
              222  BINARY_ADD       
              224  INPLACE_ADD      
              226  STORE_FAST               'arraystr'

 L.1091       228  LOAD_FAST                'self'
              230  LOAD_METHOD              dump_sections
              232  LOAD_FAST                'a'
              234  LOAD_FAST                'sup'
              236  LOAD_FAST                'qsection'
              238  BINARY_ADD       
              240  CALL_METHOD_2         2  '2 positional arguments'
              242  UNPACK_SEQUENCE_2     2 
              244  STORE_FAST               's'
              246  STORE_FAST               'd'

 L.1092       248  LOAD_FAST                's'
          250_252  POP_JUMP_IF_FALSE   286  'to 286'

 L.1093       254  LOAD_FAST                's'
              256  LOAD_CONST               0
              258  BINARY_SUBSCR    
              260  LOAD_STR                 '['
              262  COMPARE_OP               ==
          264_266  POP_JUMP_IF_FALSE   278  'to 278'

 L.1094       268  LOAD_FAST                'arraytabstr'
              270  LOAD_FAST                's'
              272  INPLACE_ADD      
              274  STORE_FAST               'arraytabstr'
              276  JUMP_FORWARD        286  'to 286'
            278_0  COME_FROM           264  '264'

 L.1096       278  LOAD_FAST                'arraystr'
              280  LOAD_FAST                's'
              282  INPLACE_ADD      
              284  STORE_FAST               'arraystr'
            286_0  COME_FROM           276  '276'
            286_1  COME_FROM           250  '250'

 L.1097       286  SETUP_LOOP          438  'to 438'
              288  LOAD_FAST                'd'
          290_292  POP_JUMP_IF_FALSE   436  'to 436'

 L.1098       294  LOAD_FAST                'self'
              296  LOAD_METHOD              _dict
              298  CALL_METHOD_0         0  '0 positional arguments'
              300  STORE_FAST               'newd'

 L.1099       302  SETUP_LOOP          428  'to 428'
              304  LOAD_FAST                'd'
              306  GET_ITER         
              308  FOR_ITER            426  'to 426'
              310  STORE_FAST               'dsec'

 L.1100       312  LOAD_FAST                'self'
              314  LOAD_METHOD              dump_sections
              316  LOAD_FAST                'd'
              318  LOAD_FAST                'dsec'
              320  BINARY_SUBSCR    
              322  LOAD_FAST                'sup'
              324  LOAD_FAST                'qsection'
              326  BINARY_ADD       
              328  LOAD_STR                 '.'
              330  BINARY_ADD       
              332  LOAD_FAST                'dsec'
              334  BINARY_ADD       
              336  CALL_METHOD_2         2  '2 positional arguments'
              338  UNPACK_SEQUENCE_2     2 
              340  STORE_FAST               's1'
              342  STORE_FAST               'd1'

 L.1101       344  LOAD_FAST                's1'
          346_348  POP_JUMP_IF_FALSE   386  'to 386'

 L.1102       350  LOAD_FAST                'arraytabstr'
              352  LOAD_STR                 '['
              354  LOAD_FAST                'sup'
              356  BINARY_ADD       
              358  LOAD_FAST                'qsection'
              360  BINARY_ADD       
              362  LOAD_STR                 '.'
              364  BINARY_ADD       
              366  LOAD_FAST                'dsec'
              368  BINARY_ADD       
              370  LOAD_STR                 ']\n'
              372  BINARY_ADD       
              374  INPLACE_ADD      
              376  STORE_FAST               'arraytabstr'

 L.1103       378  LOAD_FAST                'arraytabstr'
              380  LOAD_FAST                's1'
              382  INPLACE_ADD      
              384  STORE_FAST               'arraytabstr'
            386_0  COME_FROM           346  '346'

 L.1104       386  SETUP_LOOP          422  'to 422'
              388  LOAD_FAST                'd1'
              390  GET_ITER         
              392  FOR_ITER            420  'to 420'
              394  STORE_FAST               's1'

 L.1105       396  LOAD_FAST                'd1'
              398  LOAD_FAST                's1'
              400  BINARY_SUBSCR    
              402  LOAD_FAST                'newd'
              404  LOAD_FAST                'dsec'
              406  LOAD_STR                 '.'
              408  BINARY_ADD       
              410  LOAD_FAST                's1'
              412  BINARY_ADD       
              414  STORE_SUBSCR     
          416_418  JUMP_BACK           392  'to 392'
              420  POP_BLOCK        
            422_0  COME_FROM_LOOP      386  '386'
          422_424  JUMP_BACK           308  'to 308'
              426  POP_BLOCK        
            428_0  COME_FROM_LOOP      302  '302'

 L.1106       428  LOAD_FAST                'newd'
              430  STORE_FAST               'd'
          432_434  JUMP_BACK           288  'to 288'
            436_0  COME_FROM           290  '290'
              436  POP_BLOCK        
            438_0  COME_FROM_LOOP      286  '286'

 L.1107       438  LOAD_FAST                'arraystr'
              440  LOAD_FAST                'arraytabstr'
              442  INPLACE_ADD      
              444  STORE_FAST               'arraystr'
              446  JUMP_BACK           200  'to 200'
              448  POP_BLOCK        
              450  JUMP_FORWARD        500  'to 500'
            452_0  COME_FROM           184  '184'

 L.1109       452  LOAD_FAST                'o'
              454  LOAD_FAST                'section'
              456  BINARY_SUBSCR    
              458  LOAD_CONST               None
              460  COMPARE_OP               is-not
          462_464  POP_JUMP_IF_FALSE   566  'to 566'

 L.1110       466  LOAD_FAST                'retstr'
              468  LOAD_FAST                'qsection'
              470  LOAD_STR                 ' = '
              472  BINARY_ADD       
              474  LOAD_GLOBAL              unicode
              476  LOAD_FAST                'self'
              478  LOAD_METHOD              dump_value
              480  LOAD_FAST                'o'
              482  LOAD_FAST                'section'
              484  BINARY_SUBSCR    
              486  CALL_METHOD_1         1  '1 positional argument'
              488  CALL_FUNCTION_1       1  '1 positional argument'
              490  BINARY_ADD       
              492  LOAD_STR                 '\n'
              494  BINARY_ADD       
              496  INPLACE_ADD      
              498  STORE_FAST               'retstr'
            500_0  COME_FROM           450  '450'
            500_1  COME_FROM_LOOP      188  '188'
              500  JUMP_BACK            52  'to 52'
            502_0  COME_FROM           128  '128'

 L.1111       502  LOAD_FAST                'self'
              504  LOAD_ATTR                preserve
          506_508  POP_JUMP_IF_FALSE   554  'to 554'
              510  LOAD_GLOBAL              isinstance
              512  LOAD_FAST                'o'
              514  LOAD_FAST                'section'
              516  BINARY_SUBSCR    
              518  LOAD_GLOBAL              InlineTableDict
              520  CALL_FUNCTION_2       2  '2 positional arguments'
          522_524  POP_JUMP_IF_FALSE   554  'to 554'

 L.1112       526  LOAD_FAST                'retstr'
              528  LOAD_FAST                'qsection'
              530  LOAD_STR                 ' = '
              532  BINARY_ADD       
              534  LOAD_FAST                'self'
              536  LOAD_METHOD              dump_inline_table
              538  LOAD_FAST                'o'
              540  LOAD_FAST                'section'
              542  BINARY_SUBSCR    
              544  CALL_METHOD_1         1  '1 positional argument'
              546  BINARY_ADD       
              548  INPLACE_ADD      
              550  STORE_FAST               'retstr'
              552  JUMP_BACK            52  'to 52'
            554_0  COME_FROM           522  '522'
            554_1  COME_FROM           506  '506'

 L.1114       554  LOAD_FAST                'o'
              556  LOAD_FAST                'section'
              558  BINARY_SUBSCR    
              560  LOAD_FAST                'retdict'
              562  LOAD_FAST                'qsection'
              564  STORE_SUBSCR     
            566_0  COME_FROM           462  '462'
              566  JUMP_BACK            52  'to 52'
              568  POP_BLOCK        
            570_0  COME_FROM_LOOP       44  '44'

 L.1115       570  LOAD_FAST                'retstr'
              572  LOAD_FAST                'arraystr'
              574  INPLACE_ADD      
              576  STORE_FAST               'retstr'

 L.1116       578  LOAD_FAST                'retstr'
              580  LOAD_FAST                'retdict'
              582  BUILD_TUPLE_2         2 
              584  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 500_1


class TomlPreserveInlineDictEncoder(TomlEncoder):

    def __init__(self, _dict=dict):
        super(TomlPreserveInlineDictEncoder, self).__init__(_dict, True)


class TomlArraySeparatorEncoder(TomlEncoder):

    def __init__(self, _dict=dict, preserve=False, separator=','):
        super(TomlArraySeparatorEncoder, self).__init__(_dict, preserve)
        if separator.strip() == '':
            separator = ',' + separator
        else:
            if separator.strip(' \t\n\r,'):
                raise ValueError('Invalid separator for arrays')
        self.separator = separator

    def dump_list(self, v):
        t = []
        retval = '['
        for u in v:
            t.append(self.dump_value(u))

        while t != []:
            s = []
            for u in t:
                if isinstance(u, list):
                    for r in u:
                        s.append(r)

                else:
                    retval += ' ' + unicode(u) + self.separator

            t = s

        retval += ']'
        return retval


class TomlOrderedDecoder(TomlDecoder):

    def __init__(self):
        super(self.__class__, self).__init__(_dict=OrderedDict)


class TomlOrderedEncoder(TomlEncoder):

    def __init__(self):
        super(self.__class__, self).__init__(_dict=OrderedDict)


class TomlTz(tzinfo):

    def __init__(self, toml_offset):
        if toml_offset == 'Z':
            self._raw_offset = '+00:00'
        else:
            self._raw_offset = toml_offset
        self._sign = -1 if self._raw_offset[0] == '-' else 1
        self._hours = int(self._raw_offset[1:3])
        self._minutes = int(self._raw_offset[4:6])

    def tzname(self, dt):
        return 'UTC' + self._raw_offset

    def utcoffset(self, dt):
        return self._sign * timedelta(hours=(self._hours), minutes=(self._minutes))

    def dst(self, dt):
        return timedelta(0)