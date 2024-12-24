import socket
import struct

# Define the UDP server address and port
UDP_IP = "127.0.0.1"  # Listen on all available interfaces
UDP_PORT = 39539

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((UDP_IP, UDP_PORT))

print(f"Listening on {UDP_IP}:{UDP_PORT}")

def parse_osc_message(data):
    """
    Parse an OSC (Open Sound Control) formatted binary message.
    :param data: Binary data from UDP
    :return: Parsed messages as a list of dictionaries
    """
    parsed_messages = []
    index = 0

    # Check for OSC bundle header
    if data[index:index + 8] == b"#bundle\x00":
        index += 8  # Skip "#bundle\0"
        # Extract timestamp (8 bytes)
        timestamp = struct.unpack(">q", data[index:index + 8])[0]
        index += 8
        print(f"Bundle Timestamp: {timestamp}")

        # Process each element in the bundle
        while index < len(data):
            # Read the size of the next OSC message
            if index + 4 > len(data):
                break
            size = struct.unpack(">I", data[index:index + 4])[0]
            index += 4

            # Extract the OSC message
            osc_message = data[index:index + size]
            index += size

            # Parse the OSC message
            parsed_message = parse_single_osc_message(osc_message)
            if parsed_message:
                parsed_messages.append(parsed_message)

    else:
        # Not a bundle, try parsing as a single OSC message
        parsed_message = parse_single_osc_message(data)
        if parsed_message:
            parsed_messages.append(parsed_message)

    return parsed_messages


def parse_single_osc_message(data):
    """
    Parse a single OSC message.
    :param data: Binary data of an OSC message
    :return: Parsed message as a dictionary
    """
    try:
        # Extract the address pattern (null-terminated string)
        address_end = data.find(b'\x00')
        address = data[:address_end].decode('utf-8')
        
        # Align to 4-byte boundary
        address_end = (address_end + 4) & ~0x03

        # Extract the type tag string (starts with ',')
        type_tag_start = address_end
        type_tag_end = data.find(b'\x00', type_tag_start)
        type_tags = data[type_tag_start:type_tag_end].decode('utf-8')

        # Align to 4-byte boundary
        type_tag_end = (type_tag_end + 4) & ~0x03

        # Extract arguments based on type tags
        args = []
        index = type_tag_end
        for tag in type_tags[1:]:  # Skip ',' at the start of type tags
            if tag == 'i':  # Integer
                args.append(struct.unpack(">i", data[index:index + 4])[0])
                index += 4
            elif tag == 'f':  # Float
                args.append(struct.unpack(">f", data[index:index + 4])[0])
                index += 4
            elif tag == 's':  # String
                str_end = data.find(b'\x00', index)
                arg = data[index:str_end].decode('utf-8')
                args.append(arg)
                index = (str_end + 4) & ~0x03  # Align to 4-byte boundary

        return {"address": address, "type_tags": type_tags, "args": args}

    except Exception as e:
        print(f"Failed to parse OSC message: {e}")
        return None


while True:
    # Receive binary data from client
    data, addr = server_socket.recvfrom(65535)  # Buffer size is 4096 bytes
    print(f"Received {len(data)} bytes from {addr}")

    # Parse the received binary message
    parsed_messages = parse_osc_message(data)

    # Print parsed messages
    for msg in parsed_messages:
        print(msg)