==================
Developing Everett
==================

Install for development
=======================

Run::

    # Clone the repository
    $ git clone https://github.com/willkg/everett

    # Create a virtualenvironment
    $ mkvirtualenv everett

    # Install Everett and dev requirements
    $ pip install -r requirements-dev.txt


Release process
===============

1. Checkout main tip.

2. Check to make sure ``setup.py`` and requirements files
   have correct versions of requirements.

   Check dev dependencies using ``make checkrot``.

3. Update version numbers in ``src/everett/__init__.py``.

   1. Set ``__version__`` to something like ``1.0.0`` (use semver).
   2. Set ``__releasedate__`` to something like ``20190107``.

4. Update ``HISTORY.rst``

   1. Set the date for the release.
   2. Make sure to note any backwards incompatible changes.

5. Verify correctness.

   1. Check the manifest: ``check-manifest``
   2. Run tests: ``make test``
   3. Build docs (this runs example code): ``make docs``

6. Tag the release::

       $ git tag --sign v1.0.0

   Copy the details from ``HISTORY.rst`` into the tag comment.

7. Update PyPI::

       $ rm -rf dist/*
       $ python setup.py sdist bdist_wheel
       $ twine upload dist/*

8. Push everything::

       $ git push --tags origin main

9. Announce the release.
