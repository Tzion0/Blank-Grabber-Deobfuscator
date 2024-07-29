import random, string, base64, codecs, argparse, os, sys, re
from textwrap import wrap
from lzma import compress, decompress
from marshal import dumps
import dis, io
import contextlib

def printerr(data):
    print(data, file= sys.stderr)

class BlankDEOBF:
    def __init__(self, code, outputpath):
        self.code = code
        self.outpath = outputpath
        self.decrypt()
        self.finalize()

    def decrypt(self):

        # Extract LZMA compressed code
        pattern = r'b\'(\\x.*)\'\n'
        LZMA_compressed_data = re.search(pattern, self.code, re.MULTILINE).group(1)
        LZMA_compressed_data = bytes(LZMA_compressed_data, "latin-1").decode('unicode_escape').encode('latin-1')
        self.code = decompress(LZMA_compressed_data).decode()

        # Decode all encoded bytes
        encoded_bytes = re.findall(r'bytes\(\[([\d+,? ?]+)\]\)', self.code)
        decoded_bytes = ["".join(chr(c) for c in list(map(int, string.split(", ")))) for string in encoded_bytes]
        decoded_bytes_iter = iter(decoded_bytes)
        self.code = re.sub(r'bytes\(\[([\d+,? ?]+)\]\)', lambda match: f"\"{next(decoded_bytes_iter)}\"", self.code)

        # Decode all UTF-8 encoded strings
        pattern = r'"([^"]+)"\.decode\(\)'
        # Use re.sub to replace the encoded string with its decoded value
        self.code = re.sub(pattern, lambda match: f"\"{match.group(1)}\"", self.code)

        # Decode all base64 encoded strings
        pattern = r'getattr\(__import__\("base64"\), "b64decode"\)\("([^"]+)"\).decode\(\)'
        self.code = re.sub(pattern, lambda match: f"'{base64.b64decode(match.group(1)).decode()}'", self.code)

        # Use dis.dis to disassemble the marshal code
        pattern = r"__import__\('builtins'\).exec"
        self.code = re.sub(pattern, lambda match: "dis.dis", self.code) # Change here to other function if you wish to save raw deobfuscated pyc file

        pyc_output = io.StringIO()

        # Use contextlib.redirect_stdout to capture the output of exec
        with contextlib.redirect_stdout(pyc_output):
            exec(self.code)

        # Get the captured output
        deobfuscated_pyc_output = pyc_output.getvalue()
        self.code = deobfuscated_pyc_output

    def finalize(self):
        if os.path.dirname(self.outpath).strip() != "":
            os.makedirs(os.path.dirname(self.outpath), exist_ok= True)
        with open(self.outpath, "w") as e:
            e.write(self.code)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog= sys.argv[0], description= "Deobfuscate the python program obfuscated by Blank-C Obfuscation")
    parser.add_argument("FILE", help= "Path to the file containing the python code")
    parser.add_argument("-o", type= str, help= 'Output file path [Default: "Obfuscated_<FILE>.py"]', dest= "path")
    args = parser.parse_args()

    if not os.path.isfile(sourcefile := args.FILE):
        printerr(f'No such file: "{args.FILE}"')
        os._exit(1)
    elif not sourcefile.endswith((".py", ".pyw")):
        printerr('The file does not have a valid python script extention!')
        os._exit(1)

    filename, _ = os.path.splitext(sourcefile)

    if args.path is None:
        args.path = "Deobfuscated_" + filename + ".pyc.disas"

    with open(sourcefile, "r") as sourcefile:
        code = sourcefile.read()

    BlankDEOBF(code, args.path)