"""
System users
============
"""
from fabtools.files import is_file
from fabtools.user import *
from fabtools.utils import run_as_root

import fabtools.require


def user(name, comment=None, home=None, create_home=True, skeleton_dir=None,
    group=None, create_group=True, extra_groups=None, password=None,
    system=False, shell=None, uid=None, non_unique=False):
    """
    Require a user and its home directory.

    See :func:`fabtools.user.create` for a detailed description of
    arguments.

    ::

        from fabtools import require

        # This will also create a home directory for alice
        require.user('alice')

        # Sometimes we don't need a home directory
        require.user('mydaemon', create_home=False)

        # Require a user without shell access
        require.user('nologin', shell='/bin/false')

    .. note:: This function can be accessed directly from the
              ``fabtools.require`` module for convenience.

    """

    # Make sure the user exists
    if not exists(name):
        create(name, comment=comment, home=home, create_home=create_home,
            skeleton_dir=skeleton_dir, group=group, create_group=create_group,
            extra_groups=extra_groups, password=password, system=system,
            shell=shell, uid=uid, non_unique=non_unique)
    else:
        modify(name, comment=comment, home=home, group=group,
            extra_groups=extra_groups, password=password,
            shell=shell, uid=uid, non_unique=non_unique)

    # Make sure the home directory exists and is owned by user
    if home:
        fabtools.require.directory(home, owner=name, use_sudo=True)


def sudoer(username, hosts="ALL", operators="ALL", passwd=False, commands="ALL"):
    """
    Require sudo permissions for a given user.

    .. note:: This function can be accessed directly from the
              ``fabtools.require`` module for convenience.

    """
    tags = "PASSWD:" if passwd else "NOPASSWD:"
    spec = "%(username)s %(hosts)s=(%(operators)s) %(tags)s %(commands)s" % locals()
    filename = '/etc/sudoers.d/fabtools-%s' % username
    if is_file(filename):
        run_as_root('chmod 0640 %(filename)s && rm -f %(filename)s' % locals())
    run_as_root('echo "%(spec)s" >%(filename)s && chmod 0440 %(filename)s' % locals(), shell=True)
