import zlib


class KeyValueParser:
    commit_keys = [b'tree', b'parent', b'author', b'committer']
    message_key = b'commit_message'

    def parse_key_value_list_with_message(self, raw):
        contents = raw.split(b"\n")
        key_val = {i.split(b' ', maxsplit=1)[0]: i.split(b' ', maxsplit=1)[1] for i in contents if len(i.split(b' ')) > 1}
        for key in key_val.keys():
            if key not in self.commit_keys:
                message = key + b' ' + key_val[key]
                key_val.pop(key)
                key_val[self.message_key] = message
        return key_val

    def serialize_parse_key_value_list_with_message(self, kvlm: dict[bytes, bytes]):
        ret = b'\n'.join([i + b' ' + kvlm[i] for i in self.commit_keys]) + b'\n\n' + kvlm[self.message_key] + b'\n'
        return ret



if __name__ == "__main__":
    raw_file = r"D:\PycharmProjects\git-from-scratch\.git\objects\6c\36cda8fa8e6debac592ad1c8c333edf75f353d"

    with open(raw_file, "rb") as f:
        content = zlib.decompress(f.read()).split(b'\x00', maxsplit=1)[1]
    print(content.decode())
    key_val_parser = KeyValueParser()
    key_vals = key_val_parser.parse_key_value_list_with_message(content)
    print(content)
    key_val_parser.serialize_parse_key_value_list_with_message(key_vals)
