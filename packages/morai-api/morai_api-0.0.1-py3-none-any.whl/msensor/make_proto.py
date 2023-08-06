import os, sys
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_path, '..'))

from proto.make_proto_util import make_proto

if __name__ == '__main__':
    proto_path = os.path.normpath(os.path.join(current_path, '../proto'))
    protoc_path = os.path.normpath(os.path.join(current_path, 'protobuf'))
    
    make_proto(proto_path, protoc_path)