# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.
from __future__ import unicode_literals

from django.db import models, transaction, connection
from treebeard.mp_tree import MP_Node


class MP_Node_ByInstance(MP_Node):
    '''
    Fix Treebeard not supporting some operations on Model instances.
    '''

    class Meta:
        abstract = True

    @classmethod
    def add_root_by_instance(cls, instance):
        """
        Adds a root node to the tree.

        :raise PathOverflow: when no more root objects can be added
        """

        # do we have a root node already?
        last_root = cls.get_last_root_node()

        if last_root and last_root.node_order_by:
            # there are root nodes and node_order_by has been set
            # delegate sorted insertion to add_sibling
            return last_root.add_sibling_by_instance(instance, 'sorted-sibling')

        if last_root:
            # adding the new root node as the last one
            newpath = cls._inc_path(last_root.path)
        else:
            # adding the first root node
            newpath = cls._get_path(None, 1, 1)
        # update the instanciated object
        instance.depth = 1
        instance.path = newpath
        # saving the instance before returning it
        instance.save()

        transaction.commit_unless_managed()
        return instance

    def add_child_by_instance(self, instance):
        """
        Adds a child to the node.

        :raise PathOverflow: when no more child nodes can be added
        """

        if not self.is_leaf() and self.node_order_by:
            # there are child nodes and node_order_by has been set
            # delegate sorted insertion to add_sibling
            return self.get_last_child().add_sibling_by_instance(instance, 'sorted-sibling')

        # update the instanciated object
        instance.depth = self.depth + 1
        if not self.is_leaf():
            # adding the new child as the last one
            instance.path = self._inc_path(self.get_last_child().path)
        else:
            # the node had no children, adding the first child
            instance.path = self._get_path(self.path, instance.depth, 1)
            if len(instance.path) > \
                    instance.__class__._meta.get_field('path').max_length:
                raise PathOverflow('The new node is too deep in the tree, try'
                                   ' increasing the path.max_length property'
                                   ' and UPDATE your  database')
        # saving the instance before returning it
        instance.save()
        instance._cached_parent_obj = self

        # we increase the numchild value of the parent object
        self.numchild += 1
        self.save()

        transaction.commit_unless_managed()
        return instance

    def add_sibling_by_instance(self, instance, pos=None):
        """
        Adds a new node as a sibling to the current node object.

        :raise PathOverflow: when the library can't make room for the
           node's new position
        """

        pos = self._fix_add_sibling_opts(pos)

        # update the instanciated object
        instance.depth = self.depth

        if pos == 'sorted-sibling':
            siblings = self.get_sorted_pos_queryset(
                self.get_siblings(), instance)
            try:
                newpos = self._get_lastpos_in_path(siblings.all()[0].path)
            except IndexError:
                newpos = None
            if newpos is None:
                pos = 'last-sibling'
        else:
            newpos, siblings = None, []

        stmts = []
        _, newpath = self._move_add_sibling_aux(pos, newpos,
            self.depth, self, siblings, stmts, None, False)

        parentpath = self._get_basepath(newpath, self.depth - 1)
        if parentpath:
            stmts.append(self._get_sql_update_numchild(parentpath, 'inc'))

        cursor = connection.cursor()
        for sql, vals in stmts:
            cursor.execute(sql, vals)

        # saving the instance before returning it
        instance.path = newpath
        instance.save()

        transaction.commit_unless_managed()
        return instance
