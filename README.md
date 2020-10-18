# cfgformalizer

Formalize (show run formal) IOS, IOS-XR and other type of network configs for easy grepping.

## Usage

```
usage: cfgformalizer [-h] [--linenum] [--seqnum] [--comments] [--sort]
                     [--delimiter DELIMITER] [--include REGEXPS] [--exclude REGEXPS]
                     [--normal] [--replace REGEXP STRING] [--hash]
                     [--hash-algorithm HASH_ALGO]
                     FILE [FILE ...]

Expand context of Cisco configuration file to make them greppable

positional arguments:
  FILE                  Configuration file

optional arguments:
  -h, --help            show this help message and exit
  --linenum             Display original config line numbers
  --seqnum              Display stanza sequence number
  --comments            Display comments
  --sort                Sort statements alphabetically
  --delimiter DELIMITER
                        Change context delimiter (space by default)
  --include REGEXPS     Stack regexps for filtering output
  --exclude REGEXPS     Stack regexps for filtering output
  --normal              Display normal config style instead of formal
  --replace REGEXP STRING
                        Replace regexp with string
  --hash                Hash stanza for easy comparison
  --hash-algorithm HASH_ALGO
                        Hash algorithm used for hashing
```

## Quick start

Formalize only isis config, exclude interface config :
```
$ cfgformalizer examples/config.txt --include '^router isis' --exclude 'interface'
router isis CORE 
router isis CORE is-type level-2-only
router isis CORE net 49.0001.0000.0000.0011.00
router isis CORE log adjacency changes
router isis CORE address-family ipv4 unicast
router isis CORE address-family ipv4 unicast metric-style wide
router isis CORE address-family ipv4 unicast mpls ldp auto-config
```
Normalize config after grepping :
```
$ cfgformalizer examples/config.txt --include '^router isis' --exclude 'interface' --normal
router isis CORE
 is-type level-2-only
 net 49.0001.0000.0000.0011.00
 log adjacency changes
 address-family ipv4 unicast
  metric-style wide
  mpls ldp auto-config
```

Replace patterns for mass diff (ie: change per box settings) :
```
$ cfgformalizer examples/config.txt --include '^router isis' --exclude 'interface' --replace '(?:net )[0-9\.]+' 'NET_ADDRESS'
router isis CORE 
router isis CORE is-type level-2-only
router isis CORE NET_ADDRESS
router isis CORE log adjacency changes
router isis CORE address-family ipv4 unicast
router isis CORE address-family ipv4 unicast metric-style wide
router isis CORE address-family ipv4 unicast mpls ldp auto-config
```

Same, but only show hash of the resulting stanza :
```
$ cfgformalizer examples/config.txt --include '^router isis' --exclude 'interface' --replace '(?:net )[0-9\.]+' 'NET_ADDRESS' --hash
5527e62af438567efa1180eae776dc4fba35fd1a98c39ae2e30de789f4652b8
```

Check base isis conf over multiple files :
```
$ cfgformalizer examples/r*.txt --include '^router isis' --exclude 'interface' --replace '(?:net )[0-9\.]+' 'NET_ADDRESS' --sort --hash
5527e62af438567efa1180eae776dc4fba35fd1a98c39ae2e30de789f4652b8d
5527e62af438567efa1180eae776dc4fba35fd1a98c39ae2e30de789f4652b8d
ec128ecd040985317495e441ba7e651df3ded45ced008852b2ffe57fa451c607
```
Formalize class-maps and policy-maps as well :
```
$ cfgformalizer examples/qos.txt
class-map match-any TEST-CM-1 
class-map match-any TEST-CM-1 match precedence 2 3
class-map match-any TEST-CM-1 match cos 2 3
class-map match-any TEST-CM-1 end-class-map
class-map match-any TEST-CM-2 
class-map match-any TEST-CM-2 match precedence 4 6 7
class-map match-any TEST-CM-2 match cos 4 6 7
class-map match-any TEST-CM-2 end-class-map
policy-map TEST-PM-1 
policy-map TEST-PM-1 class TEST-CM-1
policy-map TEST-PM-1 class TEST-CM-1 priority level 1
policy-map TEST-PM-1 class TEST-CM-2
policy-map TEST-PM-1 class TEST-CM-2 priority level 2
policy-map TEST-PM-1 end-policy-map
```
