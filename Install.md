# Installing TLKCore

TLKCore provides installation methods, and we break down the installation methods into the following categories

## Online installation via pip (recommended for new users)

Reference from [tlkcore on pypi](https://pypi.org/project/tlkcore/), and launch a system console typing:

    pip install tlkcore

* Tip: [How to upgrade TLKCore if current version before v2.3.0](/examples/Python/Upgrade_guide.md)

## Offline installation using a downloaded `whl` file

1. Check your Python version
    * Windows: `python -V`
    * Linux: `python3 -V`
2. Download from [tlkcore whl on pypi](https://pypi.org/project/tlkcore/#files) for your platform and Python version.

* Tip: [How to upgrade TLKCore if current version before v2.3.0](/examples/Python/Upgrade_guide.md)

## Portable library package (original release method)

The original release method, it `will be deprecated` after v2.3.0 release

1. Check your Python version
    * Windows: `python -V`
    * Linux: `python3 -V`
2. Download from [TLKCore_release](/release)
3. Extract zip file.
4. Install dependent Python packages from requirements.txt

    `pip install -r requirements.txt`

    * [Hint-1] Under Ubuntu, please install pip
      * `sudo apt-get update`
      * `sudo apt install python3-pip`
        * [PEP-668](https://peps.python.org/pep-0668/)
        * [error: externally-managed-environment](https://askubuntu.com/questions/1465218/pip-error-on-ubuntu-externally-managed-environment-%C3%97-this-environment-is-extern)
      * `pip install --break-system-packages --user <username> -r requirements.txt`
    * [Hint-2] Under Windows, sometimes you might met the following error: ![cpp_build_tool](/images/Python_cpp_build_tools.png)
      * Please install [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#latest-microsoft-visual-c-redistributable-version)


# Installing Python3

Install Python *3.8 ~ 3.12* with **64 bit** version

* TLKCore example give a default libraries for *Python 3.10* ([python-3.10.11 64-bit download Link](https://www.python.org/downloads/release/python-31011/))

* Remember to **allow** the option: `Add python.exe to PATH`

    ![python38](/images/Python_Install38.png)

    ![python310](/images/Python_Install310.png)
