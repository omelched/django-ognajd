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

import types

from django.apps import AppConfig
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core import serializers


class OgnajdConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ognajd'

    def ready(self):

        from ..models import VersionAttrPlaceholder, make_class, RVP

        for versioned_model in [model
                                for app in self.apps.app_configs.values()
                                for model in app.models.values()
                                if hasattr(model, '_versioned') and getattr(model, '_versioned')]:

            # noinspection PyUnusedLocal
            @receiver(post_save, sender=versioned_model)
            def receiver_func(sender, instance, created, **kwargs):
                RVP['version'].objects.create(
                    ref=instance,
                    dump=serializers.serialize('json', [instance])
                )

            # noinspection PyProtectedMember
            setattr(
                VersionAttrPlaceholder,
                f'create_{versioned_model._meta.app_label}_{versioned_model.__name__}_version',
                types.MethodType(receiver_func, VersionAttrPlaceholder)
            )

        make_class()

        self.import_models()
