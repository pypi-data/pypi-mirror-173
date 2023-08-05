# Groll

*A helpful diceroller for your command line!*

## Installation

```
pip install groll
```

## Usage

```
groll [Options] DICE...

Options:
--version             -v        Print version and exit.
--long                -l        Show rolled values in ouput.
--install-completion            Install completion for the current shell.
--show-completion               Show completion for the current shell, to copy it or customize the installation.
--help                          Show this message and exit.
```

Groll parses user input for dice notation and evaluates the resulting expression. At its most basic, it can be used to roll a (virtual) handful of dice:

```bash
$ groll 2d6
> 5
```

It can also handle modifiers in the input:

```bash
$ groll d20 + 4
> 11
```

More complicated expressions are possible by wrapping input with quotes:

```bash
$ groll -l "(2d6 + 3) / 2"
> ((3 + 5) + 3) / 2 -> 5
```
