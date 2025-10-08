# Upgrade from v2.2.0 to v2.3.0

If you are upgrading from TLKCore v2.2.0 to v2.3.0 (via pip install), please follow these steps to ensure a smooth transition:

![Upgrade Steps Overview](/images/Python_upgrade_to_v2_3_0.png)

**Tip:** You may try step 1 (remove the `lib/` directory) and step 2 (install TLKCore v2.3.0) first, then run your original `main.py` to check if everything works. TLKCore v2.3.0 is designed to be backward compatible, so if `lib/` is absent and the package is installed, your script should automatically import from the pip-installed package without further modification.

If it works, no additional changes are needed. If you encounter import or runtime errors, proceed with the following steps to update your import statements and environment settings as described below.

1. **Remove the old `lib/` directory**
   - Delete or move the previous `lib/` folder from your project to avoid conflicts with the new pip-installed `tlkcore` package.

2. **Install TLKCore v2.3.0**
   - Run:

     ```bash
     pip uninstall tlkcore  # if previously installed
     pip install tlkcore
     ```

3. **Keep your old `main.py`?**
    1. **No.**
        1. Use the new `main.py` provided in `examples/Python/`.

    2. **Yes.**
        1. Modify your `main.py` imports:
            - Update all `import lib.tlkcore` or any code that modifies `sys.path` to include `lib/` to `import tlkcore`.
            ![Example1](/images/Python_upgrade_main_change_example_1.png)
            - Remove any lines such as `sys.path.insert(0, os.path.abspath(lib_path))` that force Python to use the local `lib` directory.
            ![Example2](/images/Python_upgrade_main_change_example_2.png)

4. **Troubleshooting**
   - If you encounter import errors, double-check that `lib/` is removed and all import statements reference only `tlkcore`.
   - Check your `sys.path` for any leftover references to the old library location.

If you need help updating your code or encounter issues, please contact technical support.
