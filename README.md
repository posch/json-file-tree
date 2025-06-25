Populate directory tree from a JSON specification

# Overview

The JSON spec contains a single object where each member denotes a file, directory, or symlink.

The keys are the paths. Directories end with "/".

The values specify "uid" (number), "gid" (number), and "mode"
(number).

For files, "contents" (string, utf-8) or "base64_contents" (string,
base64 encoded contents) specify the file contents.

For symlinks, "symlink" (string) specifies the link target.

Notes:

- uid (owner) and gid (group) are numeric values
- mode is also numeric, common modes are:
  - 0644 (rw-r--r--): 420
  - 0755 (rwxr-xr-x): 493
  - 0750 (rwxr-x---): 488
  - 0700 (rwx------): 448

Example:


	```json
	{
		"out/file1.txt": {
			"contents": "HELLO WORLD\n",
			"mode": 420
		},
		"out/file2.txt": {
			"base64_contents": "SEVMTE8gQkFTRTY0Cg==",
			"mode": 420
		},
		"out/file3.sh": {
			"contents": "#!/bin/sh\necho HELLO BASH\n",
			"mode": 488
		},
		"out/subdir/": {
			"mode": 448
		},
		"out/": {},
		"out/subdir/script.sh": {
			"symlink": "../file3.sh"
		}
	}
	```

produces:
	
	```sh
	$ json-file-tree.py -vf config.json
	DIR out/
	FILE out/file1.txt
	FILE out/file2.txt
	FILE out/file3.sh
	DIR out/subdir/
	SYMLINK out/subdir/script.sh

	$ find out -ls
    13643775      4 drwxr-xr-x   3 user     group        4096 Jun 25 14:43 out
    13643786      4 drwx------   2 user     group        4096 Jun 25 14:43 out/subdir
    13643785      0 lrwxrwxrwx   1 user     group          11 Jun 25 14:43 out/subdir/script.sh -> ../file3.sh
    13643789      4 -rw-r--r--   1 user     group          12 Jun 25 14:43 out/file1.txt
    13643783      4 -rwxr-x---   1 user     group          26 Jun 25 14:43 out/file3.sh
    13643781      4 -rw-r--r--   1 user     group          13 Jun 25 14:43 out/file2.txt
	```

