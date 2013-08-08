icfp2013
========

kolbaska's ICFP2013 code repository. It will become public after the end of contest.

Please use only english in sources and commit messages.


Development how-to
==================

Install python and python-pip. Run

    pip install --user -r requirements.txt

This will install all required python dependencies into your home directory. It is recommended to use python-virtualenv (in this case, `--user` is not required).

If new dependencies added to requirements.txt, it is required to rerun pip.

Run tests (nosetests script was installed as one of dependencies):

    nosetests
