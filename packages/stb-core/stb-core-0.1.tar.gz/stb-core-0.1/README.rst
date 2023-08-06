=====
Strivebit Core Packages
=====
stb-core is a collection of core packages used for strivebit products.
Detailed documentation is in the "docs" directory.
Quick start
-----------
1. Add "common" to your INSTALLED_APPS setting like this::
INSTALLED_APPS = [
        ...
        'common',
    ]
3. Run `python manage.py migrate` to create the common models.
4. Start the development server
