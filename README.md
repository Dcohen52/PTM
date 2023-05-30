# ProtoCSS Package Manager

The ProtoCSS Package Manager is a command-line tool that allows you to manage and install packages for ProtoCSS. It provides functionality for installing, upgrading, retrieving package information, and uploading packages.

2. Run the ProtoCSS Package Manager:

```
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

* **Install packages:**
    ```bash
    ptm -i package_name
    ```
    This command will install `package_name`.


* **Upgrade packages:**
    
    ```bash
    ptm -u package_name
    ```
    This command will upgrade `package_name`.


* **Get package information:**

    ```bash
    ptm -gi package_name
    ```
    
    This command will retrieve information about `package_name`, including the package description, author, version, and contained files.
    
* **Get cloud package information:**

```bash
ptm -gic package_name
```
    
Same as above - but directly from the web. the difference is that it doesn't require the package to be installed on the machine.

* **Upload a package:**
  * The ProtoCSS Package Manager will upload packages from the local `ptm_packages` directory. If this directory does not exist, it will be created automatically. 
  * The ProtoCSS Package Manager will not upload packages that are already uploaded.
  * A valid package must have a `package.json` file in its root directory. This file must contain the package name, version, and description, following the format below:
    ```json
    {
        "name": "package_name",
        "version": "x.y.z",
        "description": "Package description.",
        "author": "author_name"
    }
    ```
    if the package doesn't have a `package.json` file, the ProtoCSS Package Manager will create one automatically, after prompting the user for the package name, version, and description.
  
    For example, to upload a package named `package_name`, run the following command:
    ```bash
    ptm -up package_name
    ```
    
    This command will upload the package from the local `ptm_packages` directory.

## License

The ProtoCSS Package Manager is released under the [MIT License](LICENSE).
