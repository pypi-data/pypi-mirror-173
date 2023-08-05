Helps to prevent import of certain modules from certain modules.

It's useful if you have many modules in your project and want to keep them kind of
isolated.

After installing just add `import-rules` option to your `setup.cfg` file.

```
[flake8]
...
import-rules= 
	# yaml format here
	- module_one: [
		allow module_two,
		deny any
	]
	- module_two: [
		deny module_one.sub.submodule
	]
	- module_two.sumbodule: deny module_one
	- module_three: allow any

	# many section for the same module are allowed
	# for example
	- module_two: [
		deny some_other_module
	]

	# this will prevent any import everywhere
	- any: [
		deny any
	]

	# default behaviour is
	- any: [
		allow any
	]

...
```
Rules are checking top-down. The Order Matters.

If current module name match section name or is submodule, then it will check all imports by rules from the section.

There can be one or more rules in section.
There can be one or more sections for the same module/submodule.

`allow modulepath` - means allow imports from `modulepath` and its submodules

`deny modulepath` - means deny imports from `modulepath` and its submodules.

Keyword `any` (or `all`) - menas any module (like `*`)

CAUTION. As .INI configparser ignores indentation use `[ ... , .. ]` flow for lists as in example.
