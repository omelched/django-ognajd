# ******************************************************************************
#  ognajD — Django app which handles ORM objects' versions.                    *
#  Copyright (C) 2021-2021 omelched                                            *
#                                                                              *
#  This file is part of ognjaD.                                                *
#                                                                              *
#  ognjaD is free software: you can redistribute it and/or modify              *
#  it under the terms of the GNU Affero General Public License as published    *
#  by the Free Software Foundation, either version 3 of the License, or        *
#  (at your option) any later version.                                         *
#                                                                              *
#  ognjaD is distributed in the hope that it will be useful,                   *
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              *
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               *
#  GNU Affero General Public License for more details.                         *
#                                                                              *
#  You should have received a copy of the GNU Affero General Public License    *
#  along with ognjaD.  If not, see <https://www.gnu.org/licenses/>.            *
# ******************************************************************************

import json
import types
import uuid
import hashlib
import inspect

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Version(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(
        primary_key=True,
        null=False,
        blank=False,
        default=uuid.uuid4,
        verbose_name=_('uuid'),
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_('content_type'),
    )
    object_id = models.CharField(
        max_length=36,
        null=False,
        blank=False,
        verbose_name=_('object_id'),
    )
    ref = GenericForeignKey(
        'content_type',
        'object_id'
    )
    index = models.IntegerField(
        null=False,
        blank=False,
        editable=True,
        default=0,
        verbose_name=_('index')
    )
    timestamp = models.DateTimeField(
        null=False,
        blank=False,
        editable=False,
        auto_now_add=True,
        verbose_name=_('timestamp')
    )
    dump = models.JSONField(
        null=False,
        blank=False,
        editable=False,
        verbose_name=_('dump')
    )
    hash = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        verbose_name=_('hash'),
    )

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.hash = hashlib.md5(json.dumps(self.dump).encode('utf-8')).hexdigest()

        # index incrementer — credit to `tinfoilboy` @ https://stackoverflow.com/a/41230517
        if self._state.adding:
            last_index = RVP['version'].objects.all().aggregate(largest=models.Max('index'))['largest']
            if last_index is not None:
                self.index = last_index + 1

        super(Version, self).save(*args, **kwargs)


class VersionAttrPlaceholder:
    pass


RVP = {}


def make_class():
    def copy_placeholder_methods(ns):
        for name, method in [t for t in inspect.getmembers(VersionAttrPlaceholder, lambda m: inspect.ismethod(m))
                             if not t[0].startswith('_')]:
            ns[name] = types.MethodType(method, Version)
            ns['__module__'] = __name__
            ns['__qualname__'] = 'Version'

    RVP['version'] = types.new_class('Version', bases=(Version,), exec_body=copy_placeholder_methods)
