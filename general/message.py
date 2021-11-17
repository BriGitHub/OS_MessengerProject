import json

HEADER = 256
FORMAT = 'utf-8'

class Message():
    def __init__(self, msg_type: str, source: str, dest: str, content: str):
        self.msg_type = msg_type
        self.source = source
        self.dest = dest
        self.content = content
        
    def encode(self):
        enc_content = self.content.encode(FORMAT)
        
        header = {
            'type': self.msg_type,
            'source': self.source,
            'dest': self.dest,
            'length': len(enc_content)
        }
        enc_header = json.dumps(header).encode(FORMAT)
        enc_header += b' ' * (HEADER - len(enc_header))
        
        enc_message = enc_header + enc_content
        return enc_message
        
    @staticmethod
    def decode_header(enc_header):
        return json.loads(enc_header.decode(FORMAT))
    
    @staticmethod
    def decode_content(enc_content):
        return enc_content.decode(FORMAT)
    
    @staticmethod
    def decode_message(enc_message):
        enc_header = enc_message[:HEADER]
        enc_content = enc_message[HEADER:]
        header = Message.decode_header(enc_header)
        content = Message.decode_content(enc_content)
        
        return Message(header['type'], header['source'], header['dest'], content)
        
        
msg = Message('private', 'drew', 'edmund', 'whats poppin')
print(msg.encoded[:HEADER])
Message.decode_header(msg.encoded[:HEADER])