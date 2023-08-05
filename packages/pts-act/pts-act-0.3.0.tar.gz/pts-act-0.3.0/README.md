# ACT parser

ACT is a job definition format for the postmarketOS Phone Test System. It aims to replace the overuse
of hacked together YAML formats for starting CI jobs.

## Example

```
device: hammerhead
env {
  ARCH: aarch64
  CODENAME: lg-hammerhead
  BOOTLOADER: fastboot
  PMOS_CATEGORY: testing
  NUMBER: 432
}

power {
  reset
}

fastboot (BOOTLOADER=="fastboot") {
  flash userdata http://example.com/${CODENAME}/userdata.img
  boot http://example.com/${CODENAME}/boot.img
}

heimdall (BOOTLOADER=="heimdall") {
  flash userdata http://example.com/${CODENAME}/userdata.img
  flash boot http://example.com/${CODENAME}/boot.img
  continue
}

shell {
  username: root
  password: 1234
  script {
    uname -a
  }
}
```

The components of this:

* ActBlock: This is a block that has a name and condition and can contain other blocks, statements and definitions
* ActCondition: This defines a comparison used in the block
* ActDefinition: This is a key/value pair inside the block
* ActStatement: This is a line in the block definition that is not a key/value pair, used for scripts
* ActReference: Reference to a variable name in the ActCondition

The toplevel of an ACT document is also an ActBlock. The blocks can have statements, definitions and other blocks
inside them in any order, the ordering of these items is preserved.

Any line inside the block is parsed and if it matches the definition format it will be stored as block data.
The definition is always a string followed by a colon. The exect definition for a string in ACT is this regex:

```regex
[a-zA-Z0-9_\-:/\\.{}$]+[a-zA-Z0-9_\-/\\.{}$]
```

## Installing

This module is available on pypi as `pts-act`

## Using this module

The act module will read a string and produce the AST (Abstract syntax tree) for the ACT file.

```python
import act.parser

example = """
myblock {
   working: yes
}
"""

ast = act.parser.parse(example)
```

The result will be an ActBlock containing all the toplevel definitions as a Dict in `ast.data` and
the whole toplevel can be iterated over with `ast.contents`