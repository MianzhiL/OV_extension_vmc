# vmc_parser.py

def parse_vmc_message(data):
    """
    Parse an OSC (Open Sound Control) formatted binary VMC message.
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
            # Read the size of the next VMC message
            if index + 4 > len(data):
                break
            size = struct.unpack(">I", data[index:index + 4])[0]
            index += 4

            # Extract the VMC message
            VMC_message = data[index:index + size]
            index += size

            # Parse the VMC message
            parsed_message = parse_single_vmc_message(VMC_message)
            if parsed_message:
                parsed_messages.append(parsed_message)

    else:
        # Not a bundle, try parsing as a single VMC message
        parsed_message = parse_single_VMC_message(data)
        if parsed_message:
            parsed_messages.append(parsed_message)

    return parsed_messages


def parse_single_vmc_message(data):
    """
    Parse a single VMC message.
    :param data: Binary data of an VMC message
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

        return {"address": address, "args": args}

    except Exception as e:
        print(f"Failed to parse VMC message: {e}")
        return None