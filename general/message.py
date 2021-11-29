import json

class Message():
    HEADER = 256
    FORMAT = 'utf-8'
    
    def __init__(self, msg_type: str, source: str, dest: str, content: str):
        self.msg_type = msg_type
        self.source = source
        self.dest = dest
        self.content = content
        
    def encode(self):
        enc_content = self.content.encode(Message.FORMAT)
        
        header = {
            'type': self.msg_type,
            'source': self.source,
            'dest': self.dest,
            'length': len(enc_content)
        }
        enc_header = json.dumps(header).encode(Message.FORMAT)
        enc_header += b' ' * (Message.HEADER - len(enc_header))
        
        enc_message = enc_header + enc_content
        return enc_message
        
    @staticmethod
    def decode_header(enc_header):
        return json.loads(enc_header.decode(Message.FORMAT))
    
    @staticmethod
    def decode_content(enc_content):
        return enc_content.decode(Message.FORMAT)
    
    @staticmethod
    def decode_message(enc_message):
        enc_header = enc_message[:Message.HEADER]
        enc_content = enc_message[Message.HEADER:]
        header = Message.decode_header(enc_header)
        content = Message.decode_content(enc_content)
        
        return Message(header['type'], header['source'], header['dest'], content)
        
        
msg = Message('private', 'drew', 'edmund', 'whats poppin')
print(msg.encoded[:Message.HEADER])
Message.decode_header(msg.encoded[:Message.HEADER])