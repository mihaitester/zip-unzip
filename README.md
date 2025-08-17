# Introduction

The main idea is that some websites contain `non-UTF-8` files when saving from browser the webpage, and `Windows 10` gives error when trying to do `Send to > Compressed (zipped) folder`.

After having used `Total Commander` and `7-Zip` for multiple years, decided to write simple python script to create `UTF-8` archives, mainly for saved websites, which for some reason give error in `Windows 10`, as some characters cannot be converted.

- The underlying idea is for security through minimalism, which means using as few as possible processes running on target OS and not installing extra applications if they are not required.

- So this script allows `zipping` and `unzipping` of files and folders using `python` and avoids installing `7-Zip`, `Total Commander` or other zip applications.


# Usage
`python zip.py -n "{file_name}" "{file}" "{folder}" ...`
- will create the `{file_name}.zip` archive containing all the `file` or `folder` defined after the first parameter

`python zip.py -u {path} ...`
- will unpack all the paths into `current folder`, and will extract the `{file_name}` from each path, if the paths provided end in `{file_name}.zip`