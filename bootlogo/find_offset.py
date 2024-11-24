import sys

def find_offset(logo_file, firmware_file):
    try:
        # Read the binary content of the files
        with open(logo_file, 'rb') as logo_f:
            logo = logo_f.read()

        with open(firmware_file, 'rb') as firmware_f:
            firmware = firmware_f.read()

        # Search for the logo in the firmware
        offset = firmware.find(logo)

        if offset != -1:
            # Print the offset in decimal and hex
            print(f"logo found at offset: {offset} (decimal), 0x{offset:X} (hexadecimal)")
        else:
            print("logo not found in firmware.")

    except FileNotFoundError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Ensure two arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python find_offset.py <logo_file> <firmware_file>")
        sys.exit(1)

    logo_file = sys.argv[1]
    firmware_file = sys.argv[2]

    # Call the function to search for the logo
    find_offset(logo_file, firmware_file)
