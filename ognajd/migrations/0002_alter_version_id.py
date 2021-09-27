# ******************************************************************************
#  ognajD — Django app which handles ORM objects' versions.                    *
#  Copyright (C) 2021 omelched                                                 *
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

# Generated by Django 3.2.7 on 2021-09-27 08:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ognajd', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid'),
        ),
    ]
