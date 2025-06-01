"""
Copyright (C) 2025, Jabez Winston C

kwp2txt - Converts Kamban Word Processor (KWP) files to plain text

Author  : Jabez Winston C <jabezwinston@gmail.com>
License : MIT
Date    : 01-June-2025

"""

import os
import sys

tamil_char = [
    #  0    1      2      3      4       5     6      7      8      9      A      B      C      D      E      F
    None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None,  # 0
    None , None , None , None , None , ''   , None , None , None , None , None , None , None , None , None , None,  # 1
    None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None,  # 2
    None , None , None , None , None , None , None , None , None , None , None , None , None , None , None , None,  # 3
    None , 'கி' , 'ஙி' , 'சி' , 'ஞி' , 'ணி', 'தி' , 'நி' , 'பி' , 'மி'  , 'யி' , 'ரி' ,'லி'  , 'வி' , 'ழி' , 'ளி',  # 4
    'றி' , 'னி' , None, None , None , None  , None , 'கீ' , 'ஙீ' , 'சீ'  , 'ஞீ' , None , None , None , None , None ,  # 5
    None , 'ணீ', 'தீ'  , 'நீ' , 'பீ'  , 'மீ'  , 'யீ' , 'ரீ'  , 'லீ' , 'வீ' , 'ழீ'  , 'ளீ' , 'றீ' , 'னீ' ,  None , None,  # 6
    None , None , None , None , None , None , 'ஸ்' ,'ஷ்' , 'ஜ்'  , 'ஹ்', 'க்ஷ்', None , None , None , None , None,  # 7
    None , None , 'க்' , 'ங்' , 'ச்'   , 'ஞ்' , 'ட்' , 'ண்' , 'த்' , 'ந்'  , 'ப்' , 'ம்'  , 'ய்' , None , None , None ,  # 8
    None , None , None , None , None , None , None , None , 'ர்' , 'ல்' ,  'வ்' , 'ழ்'  , 'ள்' , None , None , 'ற்' ,  # 9
    ''   , 'ன்' , None , 'ா' , None , None , None , None , None , None , 'ெ' , 'ே' , 'ை' , None , 'டி'  , 'டீ',  # A
    'கு' , 'ஙு' , 'சு'  , 'ஞு' , 'டு' , 'ணு' , 'து' , None , 'நு'  , 'பு' , 'மு'  , 'யு' , 'ரு' , 'லு' , 'வு' , 'ழு', # B 
    'ளு', 'று' , 'னு' , 'கூ' , 'ஙூ' , 'சூ'  , 'ஞூ', 'டூ'  , 'ணூ', 'தூ' , None, 'நூ' , 'பூ' , 'மூ' , 'யூ' , 'ரூ', # C
    None , None , None , None , None , None , 'லூ' , 'வூ' , 'ழூ' , 'ளூ' , 'றூ' , 'னூ', 'அ' , 'ஆ', 'இ' , 'ஈ',  # D
    'உ' , 'ஊ' , 'எ' , 'ஏ'  , 'ஐ' , 'ஒ'  , 'ஓ'  , 'ஃ' , 'க'  , 'ங'  , 'ச'  , 'ஞ' , 'ட' , 'ண', 'த'  , 'ந' , # E
    'ப' , 'ம'  , 'ய'  , 'ர'  , 'ல' , 'வ'  , 'ழ'  , 'ள' , 'ற'  , 'ன'  , 'ஸ', 'ஷ' , 'ஜ', 'ஹ' , 'க்ஷ', 'ஸ்ரீ', # F
]

KWP_HEADER_SIGNATURE = bytearray([0xD2, 0xB0, 0xAC, 0xFF])
KWP_EOF_MARKER = b'~`!@#$%^&*()-+|=-TeCfMt'
VOWEL_MARKERS = {0xAA, 0xAB, 0xAC}  # Tamil vowel symbols like 'ெ', 'ே', 'ை'


def kwp_to_utf8(byte_val):
    return tamil_char[byte_val]


def is_kwp_file(header):
    return header[:4] == KWP_HEADER_SIGNATURE


def is_eof_sequence(f, old_byte, new_byte):
    if old_byte == KWP_EOF_MARKER[0] and new_byte == KWP_EOF_MARKER[1]:
        remaining = f.read(len(KWP_EOF_MARKER) - 2)
        if remaining == KWP_EOF_MARKER[2:]:
            return True
        f.seek(-len(remaining), 1)  # rewind
    return False


def convert_kwp_to_txt(input_path, output_path='convert.txt'):
    with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
        header = infile.read(365)
        eof_marker_used = KWP_EOF_MARKER if is_kwp_file(header) else None

        if not eof_marker_used:
            infile.seek(0)

        prev_byte = None
        combining_marker = None

        while True:
            ch = infile.read(1)
            if not ch:
                break

            byte_val = ord(ch)

            if eof_marker_used and prev_byte is not None:
                if is_eof_sequence(infile, prev_byte, byte_val):
                    break

            # Handle combining vowel marks
            if byte_val in VOWEL_MARKERS:
                combining_marker = byte_val
                continue

            utf8_char = kwp_to_utf8(byte_val)

            if combining_marker is not None:
                # Write combining vowel first
                marker_utf8 = kwp_to_utf8(combining_marker)
                if utf8_char and marker_utf8:
                    outfile.write(utf8_char.encode('utf-8'))
                    outfile.write(marker_utf8.encode('utf-8'))
                combining_marker = None
            elif utf8_char:
                outfile.write(utf8_char.encode('utf-8'))
            elif utf8_char == '':
                continue
            else:
                outfile.write(ch)

            prev_byte = byte_val
            outfile.flush()



def main():
    if len(sys.argv) < 2:
        print("Usage: kwp2txt <input_file> [output_file]")
        return

    input_path = sys.argv[1]
    
    # Derive output path from input if not provided
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        base, _ = os.path.splitext(input_path)
        output_path = base + '.txt'

    convert_kwp_to_txt(input_path, output_path)


if __name__ == "__main__":
    main()
