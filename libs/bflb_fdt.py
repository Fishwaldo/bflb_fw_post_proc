# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
# [GCC 9.4.0]
# Embedded file name: libs/bflb_fdt.py
import os, re
from struct import unpack_from, unpack, pack
from string import printable

def is_string(data):
    """ Check property string validity """
    if not len(data):
        return
    if data[-1] != 0:
        return
    pos = 0
    while pos < len(data):
        posi = pos
        while pos < len(data) and data[pos] != 0 and data[pos] in printable.encode() and data[pos] not in (ord('\r'), ord('\n')):
            pos += 1

        if not data[pos] != 0:
            if pos == posi:
                return
        pos += 1

    return True


def extract_string(data, offset=0):
    """ Extract string """
    str_end = offset
    while data[str_end] != 0:
        str_end += 1

    return data[offset:str_end].decode('ascii')


def line_offset(tabsize, offset, string):
    offset = ' ' * (tabsize * offset)
    return offset + string


def get_version_info(text):
    ret = dict()
    for line in text.split('\n'):
        line = line.rstrip('\x00')
        if line:
            if line.startswith('/ {'):
                break
        if line and line.startswith('//'):
            line = line.replace('//', '').replace(':', '')
            line = line.split()
            if line[0] in ('version', 'last_comp_version', 'boot_cpuid_phys'):
                ret[line[0]] = int(line[1], 0)

    return ret


def strip_comments(text):
    text = re.sub('//.*?(\r\n?|\n)|/\\*.*?\\*/', '\n', text, flags=(re.S))
    return text


def split_to_lines(text):
    lines = []
    mline = str()
    for line in text.split('\n'):
        line = line.replace('\t', ' ')
        line = line.rstrip('\x00')
        line = line.rstrip(' ')
        line = line.lstrip(' ')
        if line:
            if line.startswith('/dts-'):
                continue
            if line.endswith('{') or line.endswith(';'):
                line = line.replace(';', '')
                lines.append(mline + line)
                mline = str()
            else:
                mline += line

    return lines


DTB_BEGIN_NODE = 1
DTB_END_NODE = 2
DTB_PROP = 3
DTB_NOP = 4
DTB_END = 9

class Header:
    MIN_SIZE = 28
    MAX_SIZE = 40
    MAX_VERSION = 17
    MAGIC_NUMBER = 3490578157

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        if value > self.MAX_VERSION:
            raise ValueError(f"Invalid Version {value}, use: 0 - 17 !")
        self._size = self.MIN_SIZE
        if value >= 2:
            self._size += 4
        if value >= 3:
            self._size += 4
        if value >= 17:
            self._size += 4
        self._padding = 8 - self._size % 8 if self._size % 8 != 0 else 0
        self._version = value
        self.last_comp_version = value - 1

    @property
    def size(self):
        return self._size + self._padding

    @property
    def padding(self):
        return self._padding

    def __init__(self):
        self._version = None
        self._size = 0
        self._padding = 0
        self.total_size = 0
        self.off_dt_struct = 0
        self.off_dt_strings = 0
        self.off_mem_rsvmap = 0
        self.last_comp_version = 0
        self.boot_cpuid_phys = 0
        self.size_dt_strings = None
        self.size_dt_struct = None

    def __str__(self):
        return '<FDT-v{}, size: {}>'.format(self.version, self.size)

    def info(self):
        nfo = 'FDT Header:'
        nfo += '- Version: {}'.format(self.version)
        nfo += '- Size:    {}'.format(self.size)
        return nfo

    def export(self) -> bytes:
        """

        :return:
        """
        if self.version is None:
            raise Exception('Header Version must be specified !')
        blob = pack('>7I', self.MAGIC_NUMBER, self.total_size, self.off_dt_struct, self.off_dt_strings, self.off_mem_rsvmap, self.version, self.last_comp_version)
        if self.version >= 2:
            blob += pack('>I', self.boot_cpuid_phys)
        if self.version >= 3:
            blob += pack('>I', self.size_dt_strings)
        if self.version >= 17:
            blob += pack('>I', self.size_dt_struct)
        if self.padding:
            blob += bytes([0] * self.padding)
        return blob

    @classmethod
    def parse(cls, data: bytes, offset: int=0):
        """

        :param data:
        :param offset:
        """
        if len(data) < offset + cls.MIN_SIZE:
            raise ValueError('Data size too small !')
        header = cls()
        magic_number, header.total_size, header.off_dt_struct, header.off_dt_strings, header.off_mem_rsvmap, header.version, header.last_comp_version = unpack_from('>7I', data, offset)
        offset += cls.MIN_SIZE
        if magic_number != cls.MAGIC_NUMBER:
            raise Exception('Invalid Magic Number')
        if header.last_comp_version > cls.MAX_VERSION - 1:
            raise Exception(f"Invalid last compatible Version {header.last_comp_version}")
        if header.version >= 2:
            header.boot_cpuid_phys = unpack_from('>I', data, offset)[0]
            offset += 4
        if header.version >= 3:
            header.size_dt_strings = unpack_from('>I', data, offset)[0]
            offset += 4
        if header.version >= 17:
            header.size_dt_struct = unpack_from('>I', data, offset)[0]
            offset += 4
        return header


def new_property(name: str, raw_value: bytes) -> object:
    """
    Instantiate property with raw value type

    :param name: Property name
    :param raw_value: Property raw data
    """
    if is_string(raw_value):
        obj = PropStrings(name)
        for st in raw_value.decode('ascii').split('\x00'):
            if st:
                obj.append(st)

        return obj
    if len(raw_value):
        if len(raw_value) % 4 == 0:
            obj = PropWords(name)
            for i in range(0, len(raw_value), 4):
                obj.append(unpack('>I', raw_value[i:i + 4])[0])

            return obj
    if len(raw_value):
        return PropBytes(name, data=raw_value)
    return Property(name)


class BaseItem:

    @property
    def name(self):
        return self._name

    @property
    def parent(self):
        return self._parent

    @property
    def path(self):
        node = self._parent
        path = ''
        while node:
            if node.name == '/':
                break
            path = '/' + node.name + path
            node = node.parent

        if path:
            return path
        return '/'

    def __init__(self, name: str):
        """ 
        BaseItem constructor
        
        :param name: Item name
        """
        assert isinstance(name, str)
        assert all((c in printable for c in name)), 'The value must contain just printable chars !'
        self._name = name
        self._parent = None

    def __str__(self):
        """ String representation """
        return (f"{self.name}")

    def set_name(self, value: str):
        """ 
        Set item name
        
        :param value: The name in string format
        """
        assert isinstance(value, str)
        assert all((c in printable for c in value)), 'The value must contain just printable chars !'
        self._name = value

    def set_parent(self, value):
        """ 
        Set item parent

        :param value: The parent node 
        """
        assert isinstance(value, Node)
        self._parent = value

    def to_dts(self, tabsize: int=4, depth: int=0):
        raise NotImplementedError()

    def to_dtb(self, strings: str, pos: int=0, version: int=Header.MAX_VERSION):
        raise NotImplementedError()


class Property(BaseItem):

    def __getitem__(self, value):
        """ Returns No Items """
        pass

    def __eq__(self, obj):
        """ Check Property object equality """
        return isinstance(obj, Property) and self.name == obj.name

    def copy(self):
        """ Get object copy """
        return Property(self.name)

    def to_dts(self, tabsize: int=4, depth: int=0):
        """
        Get string representation

        :param tabsize: Tabulator size in count of spaces
        :param depth: Start depth for line
        """
        return line_offset(tabsize, depth, '{};\n'.format(self.name))

    def to_dtb(self, strings: str, pos: int=0, version: int=Header.MAX_VERSION):
        """
        Get binary blob representation

        :param strings:
        :param pos:
        :param version:
        """
        strpos = strings.find(self.name + '\x00')
        if strpos < 0:
            strpos = len(strings)
            strings += self.name + '\x00'
        pos += 12
        return (pack('>III', DTB_PROP, 0, strpos), strings, pos)


class PropStrings(Property):
    __doc__ = 'Property with strings as value'

    @property
    def value(self):
        if self.data:
            return self.data[0]

    def __init__(self, name, *args):
        """ 
        PropStrings constructor
        
        :param name: Property name
        :param args: str1, str2, ...
        """
        super().__init__(name)
        self.data = []
        for arg in args:
            self.append(arg)

    def __str__(self):
        """ String representation """
        return f"{self.name} = {self.data}"

    def __len__(self):
        """ Get strings count """
        return len(self.data)

    def __getitem__(self, index):
        """ Get string by index """
        return self.data[index]

    def __eq__(self, obj):
        """ Check PropStrings object equality """
        if not isinstance(obj, PropStrings) or self.name != obj.name or len(self) != len(obj):
            return False
        for index in range(len(self)):
            if self.data[index] != obj[index]:
                return False

        return True

    def copy(self):
        """ Get object copy """
        return PropStrings(self.name, *self.data)

    def append(self, value: str):
        assert isinstance(value, str)
        assert len(value) > 0, 'Invalid strings value'
        assert all((c in printable or c in ('\r', '\n') for c in value)), 'Invalid chars in strings value'
        self.data.append(value)

    def pop(self, index: int):
        assert 0 <= index < len(self.data), 'Index out of range'
        return self.data.pop(index)

    def clear(self):
        self.data.clear()

    def to_dts(self, tabsize: int=4, depth: int=0):
        """
        Get string representation

        :param tabsize: Tabulator size in count of spaces
        :param depth: Start depth for line
        """
        result = line_offset(tabsize, depth, self.name)
        result += ' = "'
        result += '", "'.join(self.data)
        result += '";\n'
        return result

    def to_dtb(self, strings: str, pos: int=0, version: int=Header.MAX_VERSION):
        """
        Get blob representation

        :param strings:
        :param pos:
        :param version:
        """
        blob = pack('')
        for chars in self.data:
            blob += chars.encode('ascii') + pack('b', 0)

        blob_len = len(blob)
        if version < 16:
            if (pos + 12) % 8 != 0:
                blob = pack('b', 0) * (8 - (pos + 12) % 8) + blob
        if blob_len % 4:
            blob += pack('b', 0) * (4 - blob_len % 4)
        strpos = strings.find(self.name + '\x00')
        if strpos < 0:
            strpos = len(strings)
            strings += self.name + '\x00'
        blob = pack('>III', DTB_PROP, blob_len, strpos) + blob
        pos += len(blob)
        return (blob, strings, pos)


class PropWords(Property):
    __doc__ = 'Property with words as value'

    @property
    def value(self):
        if self.data:
            return self.data[0]

    def __init__(self, name, *args):
        super().__init__(name)
        self.data = []
        self.word_size = 32
        for val in args:
            self.append(val)

    def __str__(self):
        """ String representation """
        return f"{self.name} = {self.data}"

    def __getitem__(self, index):
        """ Get word by index """
        return self.data[index]

    def __len__(self):
        """ Get words count """
        return len(self.data)

    def __eq__(self, prop):
        """ Check PropWords object equality  """
        if not isinstance(prop, PropWords):
            return False
        if self.name != prop.name:
            return False
        if len(self) != len(prop):
            return False
        for index in range(len(self)):
            if self.data[index] != prop[index]:
                return False

        return True

    def copy(self):
        return PropWords(self.name, *self.data)

    def append(self, value):
        assert isinstance(value, int), 'Invalid object type'
        assert 0 <= value < 2 ** self.word_size, 'Invalid word value {}, use <0x0 - 0x{:X}>'.format(value, 2 ** self.word_size - 1)
        self.data.append(value)

    def pop(self, index):
        assert 0 <= index < len(self.data), 'Index out of range'
        return self.data.pop(index)

    def clear(self):
        self.data.clear()

    def to_dts(self, tabsize: int=4, depth: int=0):
        """
        Get string representation

        :param tabsize: Tabulator size in count of spaces
        :param depth: Start depth for line
        """
        result = line_offset(tabsize, depth, self.name)
        result += ' = <'
        result += ' '.join(['0x{:X}'.format(word) for word in self.data])
        result += '>;\n'
        return result

    def to_dtb(self, strings: str, pos: int=0, version: int=Header.MAX_VERSION):
        """
        Get blob representation

        :param strings:
        :param pos:
        :param version:
        """
        strpos = strings.find(self.name + '\x00')
        if strpos < 0:
            strpos = len(strings)
            strings += self.name + '\x00'
        blob = pack('>III', DTB_PROP, len(self.data) * 4, strpos)
        for word in self.data:
            blob += pack('>I', word)

        pos += len(blob)
        return (blob, strings, pos)


class PropBytes(Property):
    __doc__ = 'Property with bytes as value'

    def __init__(self, name, data=None):
        """ 
        PropBytes constructor
        
        :param name: Property name
        :param data: Data as list, bytes or bytearray
        """
        super().__init__(name)
        self.data = bytearray()
        if data:
            assert isinstance(data, (list, bytes, bytearray))
            self.data = bytearray(data)

    def __str__(self):
        """ String representation """
        return f"{self.name} = {self.data}"

    def __getitem__(self, index):
        """Get byte by index """
        return self.data[index]

    def __len__(self):
        """ Get bytes count """
        return len(self.data)

    def __eq__(self, prop):
        """ Check PropBytes object equality  """
        if not isinstance(prop, PropBytes):
            return False
        if self.name != prop.name:
            return False
        if len(self) != len(prop):
            return False
        for index in range(len(self)):
            if self.data[index] != prop[index]:
                return False

        return True

    def copy(self):
        """ Create a copy of object """
        return PropBytes(self.name, self.data)

    def append(self, value):
        assert isinstance(value, int), 'Invalid object type'
        assert 0 <= value <= 255, 'Invalid byte value {}, use <0 - 255>'.format(value)
        self.data.append(value)

    def pop(self, index):
        assert 0 <= index < len(self.data), 'Index out of range'
        return self.data.pop(index)

    def clear(self):
        self.data = bytearray()

    def to_dts(self, tabsize: int=4, depth: int=0):
        """
        Get string representation

        :param tabsize: Tabulator size in count of spaces
        :param depth: Start depth for line
        """
        result = line_offset(tabsize, depth, self.name)
        result += ' = ['
        result += ' '.join(['{:02X}'.format(byte) for byte in self.data])
        result += '];\n'
        return result

    def to_dtb(self, strings: str, pos: int=0, version: int=Header.MAX_VERSION):
        """
        Get blob representation

        :param strings:
        :param pos:
        :param version:
        """
        strpos = strings.find(self.name + '\x00')
        if strpos < 0:
            strpos = len(strings)
            strings += self.name + '\x00'
        blob = pack('>III', DTB_PROP, len(self.data), strpos)
        blob += bytes(self.data)
        if len(blob) % 4:
            blob += bytes([0] * (4 - len(blob) % 4))
        pos += len(blob)
        return (blob, strings, pos)


class PropIncBin(PropBytes):
    __doc__ = 'Property with bytes as value'

    def __init__(self, name, data=None, file_name=None, rpath=None):
        """
        PropIncBin constructor

        :param name: Property name
        :param data: Data as list, bytes or bytearray
        :param file_name: File name
        :param rpath: Relative path
        """
        super().__init__(name, data)
        self.file_name = file_name
        self.relative_path = rpath

    def __eq__(self, prop):
        """ Check PropIncBin object equality  """
        if not isinstance(prop, PropIncBin):
            return False
        if self.name != prop.name:
            return False
        if self.file_name != prop.file_name:
            return False
        if self.relative_path != prop.relative_path:
            return False
        if self.data != prop.data:
            return False
        return True

    def copy(self):
        """ Create a copy of object """
        return PropIncBin(self.name, self.data, self.file_name, self.relative_path)

    def to_dts(self, tabsize: int=4, depth: int=0):
        """
        Get string representation

        :param tabsize: Tabulator size in count of spaces
        :param depth: Start depth for line
        """
        file_path = self.file_name
        if self.relative_path is not None:
            file_path = '{}/{}'.format(self.relative_path, self.file_name)
        result = line_offset(tabsize, depth, self.name)
        result += ' = /incbin/("{}");\n'.format(file_path)
        return result


class Node(BaseItem):
    __doc__ = 'Node representation'

    @property
    def props(self):
        return self._props

    @property
    def nodes(self):
        return self._nodes

    @property
    def empty(self):
        if self.nodes or self.props:
            return False
        return True

    def __init__(self, name, *args):
        super().__init__(name)
        self._props = []
        self._nodes = []
        for item in args:
            self.append(item)

    def __str__(self):
        """ String representation """
        return '< {}: {} props, {} nodes >'.format(self.name, len(self.props), len(self.nodes))

    def __eq__(self, node):
        """ Check node equality """
        if not isinstance(node, Node):
            return False
        if self.name != node.name or len(self.props) != len(node.props) or len(self.nodes) != len(node.nodes):
            return False
        for p in self.props:
            if p not in node.props:
                return False

        for n in self.nodes:
            if n not in node.nodes:
                return False

        return True

    def copy(self):
        """ Create a copy of Node object """
        node = Node(self.name)
        for p in self.props:
            node.append(p.copy())

        for n in self.nodes:
            node.append(n.copy())

        return node

    def get_property(self, name):
        """ 
        Get property object by its name
        
        :param name: Property name
        """
        for p in self.props:
            if p.name == name:
                return p

    def set_property(self, name, value):
        """
        Set property

        :param name: Property name
        :param value: Property value
        """
        if value is None:
            new_prop = Property(name)
        else:
            if isinstance(value, int):
                new_prop = PropWords(name, value)
            else:
                if isinstance(value, str):
                    new_prop = PropStrings(name, value)
                else:
                    if isinstance(value, list) and isinstance(value[0], int):
                        new_prop = PropWords(name, *value)
                    else:
                        if isinstance(value, list):
                            if isinstance(value[0], str):
                                new_prop = PropStrings(name, *value)
                            else:
                                if isinstance(value, (bytes, bytearray)):
                                    new_prop = PropBytes(name, data=value)
                                else:
                                    raise TypeError('Value type not supported')
                        else:
                            new_prop.set_parent(self)
                            old_prop = self.get_property(name)
                            if old_prop is None:
                                self.props.append(new_prop)
                            else:
                                index = self.props.index(old_prop)
                            self.props[index] = new_prop

    def get_subnode(self, name: str):
        """ 
        Get subnode object by name

        :param name: Subnode name
        """
        for n in self.nodes:
            if n.name == name:
                return n

    def exist_property(self, name: str) -> bool:
        """ 
        Check if property exist and return True if exist else False
        
        :param name: Property name
        """
        if self.get_property(name) is None:
            return False
        return True

    def exist_subnode(self, name: str) -> bool:
        """ 
        Check if subnode exist and return True if exist else False
        
        :param name: Subnode name
        """
        if self.get_subnode(name) is None:
            return False
        return True

    def remove_property(self, name: str):
        """ 
        Remove property object by its name.
        
        :param name: Property name
        """
        item = self.get_property(name)
        if item is not None:
            self.props.remove(item)

    def remove_subnode(self, name: str):
        """ 
        Remove subnode object by its name.
        
        :param name: Subnode name
        """
        item = self.get_subnode(name)
        if item is not None:
            self.nodes.remove(item)

    def append(self, item):
        """ 
        Append node or property
        
        :param item: The node or property object
        """
        assert isinstance(item, (
         Node, Property)), 'Invalid object type, use "Node" or "Property"'
        if isinstance(item, Property):
            if self.get_property(item.name) is not None:
                raise Exception('{}: "{}" property already exists'.format(self, item.name))
            item.set_parent(self)
            self.props.append(item)
        else:
            if self.get_subnode(item.name) is not None:
                raise Exception('{}: "{}" node already exists'.format(self, item.name))
            if item is self:
                raise Exception('{}: append the same node {}'.format(self, item.name))
            item.set_parent(self)
            self.nodes.append(item)

    def merge(self, node_obj, replace: bool=True):
        """ 
        Merge two nodes
        
        :param node_obj: Node object
        :param replace: If True, replace current properties with the given properties
        """
        assert isinstance(node_obj, Node), 'Invalid object type'

        def get_property_index(name):
            for i, p in enumerate(self.props):
                if p.name == name:
                    return i

        def get_subnode_index(name):
            for i, n in enumerate(self.nodes):
                if n.name == name:
                    return i

        for prop in node_obj.props:
            index = get_property_index(prop.name)
            if index is None:
                self.append(prop.copy())
            elif prop in self._props:
                continue
            elif replace:
                new_prop = prop.copy()
                new_prop.set_parent(self)
                self._props[index] = new_prop
                continue

        for sub_node in node_obj.nodes:
            index = get_subnode_index(sub_node.name)
            if index is None:
                self.append(sub_node.copy())
            elif sub_node in self._nodes:
                continue
            else:
                self._nodes[index].merge(sub_node, replace)

    def to_dts(self, tabsize: int=4, depth: int=0) -> str:
        """ 
        Get string representation of NODE object
        
        :param tabsize: Tabulator size in count of spaces
        :param depth: Start depth for line
        """
        dts = line_offset(tabsize, depth, self.name + ' {\n')
        dts += ''.join((prop.to_dts(tabsize, depth + 1) for prop in self._props))
        dts += ''.join((node.to_dts(tabsize, depth + 1) for node in self._nodes))
        dts += line_offset(tabsize, depth, '};\n')
        return dts

    def to_dtb(self, strings, pos=0, version=Header.MAX_VERSION):
        """ 
        Get NODE in binary blob representation
        
        :param strings: 
        :param pos:
        :param version:
        """
        if self.name == '/':
            blob = pack('>II', DTB_BEGIN_NODE, 0)
        else:
            blob = pack('>I', DTB_BEGIN_NODE)
            blob += self.name.encode('ascii') + b'\x00'
        if len(blob) % 4:
            blob += pack('b', 0) * (4 - len(blob) % 4)
        pos += len(blob)
        for prop in self._props:
            data, strings, pos = prop.to_dtb(strings, pos, version)
            blob += data

        for node in self._nodes:
            data, strings, pos = node.to_dtb(strings, pos, version)
            blob += data

        pos += 4
        blob += pack('>I', DTB_END_NODE)
        return (blob, strings, pos)


class ItemType:
    NODE = 0
    PROP = 1
    BOTH = 3


class FDT:
    __doc__ = ' Flattened Device Tree Class '

    @property
    def empty(self):
        return self.root.empty

    def __init__(self, header=None):
        """
        FDT class constructor

        :param header:
        """
        self.entries = []
        self.header = Header() if header is None else header
        self.root = Node('/')

    def __str__(self):
        """ String representation """
        return self.info()

    def info(self):
        """ Return object info in human readable format """
        msg = 'FDT Content:\n'
        for path, nodes, props in self.walk():
            msg += '{} [{}N, {}P]\n'.format(path, len(nodes), len(props))

        return msg

    def get_node(self, path: str, create: bool=False) -> Node:
        """ 
        Get node object from specified path
        
        :param path: Path as string
        :param create: If True, not existing nodes will be created
        """
        assert isinstance(path, str), 'Node path must be a string type !'
        node = self.root
        path = path.lstrip('/')
        if path:
            names = path.split('/')
            for name in names:
                item = node.get_subnode(name)
                if item is None:
                    if create:
                        item = Node(name)
                        node.append(item)
                    else:
                        raise ValueError('Path "{}" doesn\'t exists'.format(path))
                node = item

        return node

    def get_property(self, name: str, path: str='') -> Property:
        """ 
        Get property object by name from specified path
        
        :param name: Property name
        :param path: Path to sub-node
        """
        return self.get_node(path).get_property(name)

    def set_property(self, name: str, value, path: str='', create: bool=True):
        """
        Set property object by name
        
        :param name: Property name
        :param value: Property value
        :param path: Path to subnode
        :param create: If True, not existing nodes will be created
        """
        self.get_node(path, create).set_property(name, value)

    def exist_node(self, path: str) -> bool:
        """ 
        Check if <path>/node exist and return True
        
        :param path: path/node name
        :return True if <path>/node exist else False
        """
        try:
            self.get_node(path)
        except ValueError:
            return False
        else:
            return True

    def exist_property(self, name: str, path: str='') -> bool:
        """ 
        Check if property exist
        
        :param name: Property name
        :param path: The path
        """
        if self.exist_node(path):
            return self.get_node(path).exist_property(name)
        return False

    def remove_node(self, name: str, path: str=''):
        """ 
        Remove node obj by path/name. Raises ValueError if path/name doesn't exist
        
        :param name: Node name
        :param path: Path to sub-node
        """
        self.get_node(path).remove_subnode(name)

    def remove_property(self, name: str, path: str=''):
        """ 
        Remove property obj by name. Raises ValueError if path/name doesn't exist
        
        :param name: Property name
        :param path: Path to subnode
        """
        self.get_node(path).remove_property(name)

    def add_item(self, obj, path: str='', create: bool=True):
        """ 
        Add sub-node or property at specified path. Raises ValueError if path doesn't exist
        
        :param obj: The node or property object
        :param path: The path to subnode
        :param create: If True, not existing nodes will be created
        """
        self.get_node(path, create).append(obj)

    def search(self, name, itype=ItemType.BOTH, path=''):
        """ 
        Search properties and/or nodes with specified name. Return list of founded items
        
        :param name: Property or Node name
        :param itype: Item type - NODE, PROP or BOTH
        :param path: Path to root node
        """
        assert isinstance(name, str), 'Property name must be a string type !'
        node = self.get_node(path)
        nodes = []
        items = []
        while 1:
            nodes += node.nodes
            if itype == ItemType.NODE or itype == ItemType.BOTH:
                if node.name == name:
                    items.append(node)
            if not itype == ItemType.PROP:
                if itype == ItemType.BOTH:
                    for p in node.props:
                        if p.name == name:
                            items.append(p)

                if not nodes:
                    break
                node = nodes.pop()

        return items

    def walk(self, path: str='', relative: bool=False) -> list:
        """ 
        Walk trough nodes and return relative/absolute path with list of sub-nodes and properties
        
        :param path: The path to root node
        :param relative: True for relative or False for absolute return path
        """
        all_nodes = []
        node = self.get_node(path)
        while True:
            all_nodes += node.nodes
            current_path = f"{node.path}/{node.name}"
            current_path = current_path.replace('///', '/')
            current_path = current_path.replace('//', '/')
            if path:
                if relative:
                    current_path = current_path.replace(path, '').lstrip('/')
            yield (
             current_path, node.nodes, node.props)
            if not all_nodes:
                break
            node = all_nodes.pop()

    def merge(self, fdt_obj, replace: bool=True):
        """
        Merge external FDT object into this object.
        
        :param fdt_obj: The FDT object which will be merged into this
        :param replace: True for replace existing items or False for keep old items
        """
        assert isinstance(fdt_obj, FDT)
        if self.header.version is None:
            self.header = fdt_obj.header
        else:
            if fdt_obj.header.version is not None:
                if fdt_obj.header.version > self.header.version:
                    self.header.version = fdt_obj.header.version
        if fdt_obj.entries:
            for in_entry in fdt_obj.entries:
                exist = False
                for index in range(len(self.entries)):
                    if self.entries[index]['address'] == in_entry['address']:
                        self.entries[index]['address'] = in_entry['size']
                        exist = True
                        break

                if not exist:
                    self.entries.append(in_entry)

        self.root.merge(fdt_obj.get_node('/'), replace)

    def update_phandles(self):
        all_nodes = []
        phandle_value = 0
        no_phandle_nodes = []
        node = self.root
        all_nodes += self.root.nodes
        while all_nodes:
            props = (
             node.get_property('phandle'), node.get_property('linux,phandle'))
            value = None
            for i, p in enumerate(props):
                if isinstance(p, PropWords) and isinstance(p.value, int):
                    value = None if (i == 1 and p.value != value) else (p.value)

            if value is None:
                no_phandle_nodes.append(node)
            else:
                if phandle_value < value:
                    phandle_value = value
            node = all_nodes.pop()
            all_nodes += node.nodes

        if phandle_value > 0:
            phandle_value += 1
        for node in no_phandle_nodes:
            node.set_property('linux,phandle', phandle_value)
            node.set_property('phandle', phandle_value)
            phandle_value += 1

    def to_dts(self, tabsize: int=4) -> str:
        """
        Store FDT Object into string format (DTS)

        :param tabsize:
        """
        result = '/dts-v1/;\n'
        if self.header.version is not None:
            result += '// version: {}\n'.format(self.header.version)
            result += '// last_comp_version: {}\n'.format(self.header.last_comp_version)
            if self.header.version >= 2:
                result += '// boot_cpuid_phys: 0x{:X}\n'.format(self.header.boot_cpuid_phys)
        result += '\n'
        if self.entries:
            for entry in self.entries:
                result += '/memreserve/ '
                result += '{:#x} '.format(entry['address']) if entry['address'] else '0 '
                result += '{:#x}'.format(entry['size']) if entry['size'] else '0'
                result += ';\n'

        if self.root is not None:
            result += self.root.to_dts(tabsize)
        return result

    def to_dtb(self, version=None, last_comp_version=None, boot_cpuid_phys=None):
        """
        Export FDT Object into Binary Blob format (DTB)

        :param version:
        :param last_comp_version:
        :param boot_cpuid_phys:
        """
        if self.root is None:
            return b''
        from struct import pack
        if version is not None:
            self.header.version = version
        if last_comp_version is not None:
            self.header.last_comp_version = last_comp_version
        if boot_cpuid_phys is not None:
            self.header.boot_cpuid_phys = boot_cpuid_phys
        if self.header.version is None:
            raise Exception('DTB Version must be specified !')
        blob_entries = bytes()
        if self.entries:
            for entry in self.entries:
                blob_entries += pack('>QQ', entry['address'], entry['size'])

        blob_entries += pack('>QQ', 0, 0)
        blob_data_start = self.header.size + len(blob_entries)
        blob_data, blob_strings, data_pos = self.root.to_dtb('', blob_data_start, self.header.version)
        blob_data += pack('>I', DTB_END)
        self.header.size_dt_strings = len(blob_strings)
        self.header.size_dt_struct = len(blob_data)
        self.header.off_mem_rsvmap = self.header.size
        self.header.off_dt_struct = blob_data_start
        self.header.off_dt_strings = blob_data_start + len(blob_data)
        self.header.total_size = blob_data_start + len(blob_data) + len(blob_strings)
        blob_header = self.header.export()
        return blob_header + blob_entries + blob_data + blob_strings.encode('ascii')


def parse_dts(text: str, root_dir: str='') -> FDT:
    """
    Parse DTS text file and create FDT Object

    :param text:
    :param root_dir: 
    """
    ver = get_version_info(text)
    text = strip_comments(text)
    dts_lines = split_to_lines(text)
    fdt_obj = FDT()
    if 'version' in ver:
        fdt_obj.header.version = ver['version']
    if 'last_comp_version' in ver:
        fdt_obj.header.last_comp_version = ver['last_comp_version']
    if 'boot_cpuid_phys' in ver:
        fdt_obj.header.boot_cpuid_phys = ver['boot_cpuid_phys']
    fdt_obj.entries = []
    for line in dts_lines:
        if line.endswith('{'):
            break
        if line.startswith('/memreserve/'):
            line = line.strip(';')
            line = line.split()
            if len(line) != 3:
                raise Exception()
            fdt_obj.entries.append({'address':int(line[1], 0),  'size':int(line[2], 0)})

    curnode = None
    fdt_obj.root = None
    for line in dts_lines:
        if line.endswith('{'):
            node_name = line.split()[0]
            new_node = Node(node_name)
            if fdt_obj.root is None:
                fdt_obj.root = new_node
            if curnode is not None:
                curnode.append(new_node)
            curnode = new_node

    return fdt_obj


def parse_dtb(data: bytes, offset: int=0) -> FDT:
    """
    Parse FDT Binary Blob and create FDT Object
    
    :param data: FDT Binary Blob as bytes or bytearray
    :param offset:
    """
    assert isinstance(data, (bytes, bytearray)), 'Invalid argument type'
    from struct import unpack_from
    fdt_obj = FDT()
    fdt_obj.header = Header.parse(data)
    index = fdt_obj.header.off_mem_rsvmap
    while True:
        entrie = dict(zip(('address', 'size'), unpack_from('>QQ', data, offset + index)))
        index += 16
        if entrie['address'] == 0:
            if entrie['size'] == 0:
                break
        fdt_obj.entries.append(entrie)

    current_node = None
    fdt_obj.root = None
    index = fdt_obj.header.off_dt_struct
    while 1:
        if len(data) < offset + index + 4:
            raise Exception('Index out of range !')
        tag = unpack_from('>I', data, offset + index)[0]
        index += 4
        if tag == DTB_BEGIN_NODE:
            node_name = extract_string(data, offset + index)
            index = index + len(node_name) + 4 & -4
            if not node_name:
                node_name = '/'
            new_node = Node(node_name)
            if fdt_obj.root is None:
                fdt_obj.root = new_node
            if current_node is not None:
                current_node.append(new_node)
            current_node = new_node
        elif tag == DTB_END_NODE:
            if current_node is not None:
                current_node = current_node.parent
        elif tag == DTB_PROP:
            prop_size, prop_string_pos = unpack_from('>II', data, offset + index)
            prop_start = index + 8
            if fdt_obj.header.version < 16:
                if prop_size >= 8:
                    prop_start = prop_start + 7 & -8
                prop_name = extract_string(data, fdt_obj.header.off_dt_strings + prop_string_pos)
                prop_raw_value = data[offset + prop_start:offset + prop_start + prop_size]
                index = prop_start + prop_size
                index = index + 3 & -4
                if current_node is not None:
                    current_node.append(new_property(prop_name, prop_raw_value))
            else:
                if tag == DTB_END:
                    break
        else:
            raise Exception('Unknown Tag: {}'.format(tag))

    return fdt_obj


def diff(fdt1: FDT, fdt2: FDT) -> tuple:
    """ 
    Compare two flattened device tree objects and return list of 3 objects (same in 1 and 2, specific for 1, specific for 2)
    
    :param fdt1: The object 1 of FDT
    :param fdt2: The object 2 of FDT
    """
    if not isinstance(fdt1, FDT):
        raise AssertionError('Invalid argument type')
    else:
        assert isinstance(fdt2, FDT), 'Invalid argument type'
        fdt_a = FDT(fdt1.header)
        fdt_b = FDT(fdt2.header)
        if fdt1.header.version is not None and fdt2.header.version is not None:
            fdt_same = FDT(fdt1.header if fdt1.header.version > fdt2.header.version else fdt2.header)
        else:
            fdt_same = FDT(fdt1.header)
        if fdt1.entries and fdt2.entries:
            for entry_a in fdt1.entries:
                for entry_b in fdt2.entries:
                    if entry_a['address'] == entry_b['address'] and entry_a['size'] == entry_b['size']:
                        fdt_same.entries.append(entry_a)
                        break

    for entry_a in fdt1.entries:
        found = False
        for entry_s in fdt_same.entries:
            if entry_a['address'] == entry_s['address'] and entry_a['size'] == entry_s['size']:
                found = True
                break

        if not found:
            fdt_a.entries.append(entry_a)

    for entry_b in fdt2.entries:
        found = False
        for entry_s in fdt_same.entries:
            if entry_b['address'] == entry_s['address'] and entry_b['size'] == entry_s['size']:
                found = True
                break

        if not found:
            fdt_b.entries.append(entry_b)

    for path, nodes, props in fdt1.walk():
        try:
            rnode = fdt2.get_node(path)
        except:
            rnode = None

        for node_b in nodes:
            if rnode is None or rnode.get_subnode(node_b.name) is None:
                fdt_a.add_item(Node(node_b.name), path)
            else:
                fdt_same.add_item(Node(node_b.name), path)

        for prop_a in props:
            if rnode is not None and prop_a == rnode.get_property(prop_a.name):
                fdt_same.add_item(prop_a.copy(), path)
            else:
                fdt_a.add_item(prop_a.copy(), path)

    for path, nodes, props in fdt2.walk():
        try:
            rnode = fdt_same.get_node(path)
        except:
            rnode = None

        for node_b in nodes:
            if not rnode is None:
                if rnode.get_subnode(node_b.name) is None:
                    pass
                fdt_b.add_item(Node(node_b.name), path)

        for prop_b in props:
            if not rnode is None:
                if prop_b != rnode.get_property(prop_b.name):
                    pass
                fdt_b.add_item(prop_b.copy(), path)

    return (
     fdt_same, fdt_a, fdt_b)