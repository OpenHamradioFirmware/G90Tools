import sys

def find_offsets(logo_file, firmware_file):
    try:
        # Read the binary content of the files
        with open(logo_file, 'rb') as logo_f:
            logo = logo_f.read()

        with open(firmware_file, 'rb') as firmware_f:
            firmware = firmware_f.read()

        # Initialize the starting position and a list to store offsets
        start = 0
        offsets = []

        # Search for all occurrences of the logo in the firmware
        while True:
            offset = firmware.find(logo, start)
            if offset == -1:
                break
            offsets.append(offset)
            start = offset + 1  # Move start position to the next byte after the found offset

        if offsets:
            # Print all offsets in decimal and hexadecimal
            for offset in offsets:
                print(f"Logo found at offset: {offset} (decimal), 0x{offset:X} (hexadecimal)")
        else:
            print("Logo not found in firmware.")

    except FileNotFoundError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Ensure two arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python find_offsets.py <logo_file> <firmware_file>")
        sys.exit(1)

    logo_file = sys.argv[1]
    firmware_file = sys.argv[2]

    # Call the function to search for the logo
    find_offsets(logo_file, firmware_file)
