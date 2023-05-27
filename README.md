# ProtoCSS Package Manager

The ProtoCSS Package Manager is a command-line tool written in Python that allows you to manage and install packages for the ProtoCSS preprocessor. It provides functionality for installing, upgrading, retrieving package information, and uploading packages.

2. Run the ProtoCSS Package Manager:

```bash
ptm [-i | -u | -gi | -up] [packages]
```
## Usage

The ProtoCSS Package Manager supports the following command-line options:

- `packages`: Optional. Specify the package names to be installed, upgraded, or retrieved.
- `-i`, `--install`: Install packages.
- `-u`, `--upgrade`: Upgrade packages.
- `-gi`, `--get-info`: Get package information.
- `-up`, `--upload`: Upload packages.

## Examples

1. Install packages:
```bash
ptm -i package_name
```
This command will install `package_name`.

2. Upgrade packages:

```bash
ptm -u package_name
```
This command will upgrade `package_name`.

3. Get package information:

```bash
ptm -gi package_name
```

This command will retrieve information about `package_name`, including the package description, author, version, and files.

4. Upload a package:

```bash
ptm -up package_name
```

This command will upload the packages from the local `ptm_packages` directory.

## License

The ProtoCSS Package Manager is released under the [MIT License](LICENSE).