# Blank-Grabber Deobfuscator
[Blank-Grabber](https://github.com/Blank-c/Blank-Grabber/) is a Python3 stealer created by [Blank-c](https://github.com/Blank-c). Although the project has been discontinued/archived by the creator at the time of writing this, the stealer itself is still a go-to tool for low effort script kiddies due to its durability.

This deobfuscator is created based on the Blank-Grabber Obfuscator [BlankOBF.py](https://github.com/Blank-c/Blank-Grabber/blob/main/Blank%20Grabber/Components/BlankOBF.py), aiming to speed up the process of analyzing the relevant sample in future.

This deobfuscator will deobfuscate and output in PYC disassemble format.

This deobfuscator works regardless of the value `self.varlen` and custom configurations, which is customizable in the obfuscator script for the script kiddies hoping/aiming to enhance the obfuscation. However, this deobfuscastor did not works against `self.encrypt3()` function as it was commented and not being used by default in the obfuscator script.

# Usage
```
BlankDEOBF.py malicious-obf.py -o malicious-deobf.pyc.disas
```

# Testing
```
# Obfuscation
python3 BlankOBF.py tests/test.py -o tests/test-obfuscated.py

# Deobfuscation
python3 BlankDEOBF.py tests/test-obfuscated.py -o tests/test-deobfuscated.pyc.disas
```