# (c) Nelen & Schuurmans.  MIT licensed, see LICENSE.rst.
"""
DDSC-core provides its own `authentication backend
<https://docs.djangoproject.com/en/dev/topics/auth/>`_ for checking
permissions.

"""
from __future__ import unicode_literals
from django.contrib.auth.models import Permission
from django.db.models import Q
from tls import request

from lizard_security.backends import LizardPermissionBackend
from lizard_security.middleware import USER_GROUP_IDS
from lizard_security.models import PermissionMapper

APP_LABEL = 'ddsc_core'


class PermissionBackend(LizardPermissionBackend):
    """Checker for object-level permissions via lizard-security."""

    def has_perm(self, user, permission, obj=None):
        """Return if we have a permission through a permission manager.

        Note: ``perm`` is a string like ``'testcontent.change_content'``, not
        a Permission object.

        We don't look at a user, just at user group membership. Our middleware
        translated logged in users to user group membership already.

        """
        if obj is None:
            # We' interested in a global permissions by definition. We only
            # deal with object-level permissions.
            return False
        if not hasattr(obj, 'data_set'):
            # We only manage objects with a data set attached.
            return False
        if request:
            user_group_ids = getattr(request, USER_GROUP_IDS, None)
        else:
            # No tread-local request object.
            user_group_ids = user.user_group_memberships.values_list('id',
                flat=True)
        user_group_query = Q(user_group__id__in=user_group_ids)
        relevant_data_sets = obj.data_set.values_list('id', flat=True)
        data_set_query = Q(data_set__in=relevant_data_sets)
        relevant_permission_mappers = PermissionMapper.objects.filter(
            user_group_query & data_set_query)
        if not relevant_permission_mappers:
            # No, we cannot say anything about it.
            return False
        # We need to check whether we have the specific permission.
        permissions = Permission.objects.filter(
            group__permissionmapper__in=relevant_permission_mappers)
        permissions = [(p.content_type.app_label + '.' + p.codename)
                       for p in permissions]
        obj_class = obj.__class__.__name__.lower()
        perm = '%s.%s_%s' % (APP_LABEL, permission, obj_class)
        return perm in permissions
