# ognajD

Django app which handles ORM objects' versions.

## Description

**ognajD** is Django-compactible application which handles versionning for ORM models.
Main feature is for **ognjaD** to be a "plug-in" Django application, thus capable to 
work with "little-to-no" configuring and changes to Django project.

### Features
**ognajd** stores objects' versions in own table, relied on `contenttypes` application.

**ognajD** @ [v0.0.1](https://github.com/CaterinaLemanRussia/bestelle-backend/releases/tag/v2.0.3) can:

 - catch object's save / update signals
 - store snapshot of object in DB with:
   - timestamp
   - serialized version
   - hash

### Usage example

[`sample-project`](sample_project) is a showcase django project, based on famous
[`polls`](https://docs.djangoproject.com/en/3.2/intro/tutorial01/#creating-the-polls-app) application.
You can reference to it for usage cases, examples, testing.You must never deploy `sample_project` in
production due to exposed `SECRET_KEY`.

## Getting Started

### Dependencies

#### Python packages

* `django~=3.2.7` <sub>might work on lesser versions, never tested</sub>

#### Django applications

* `contenttypes`

### Installing

As there is no package at time you can:

* clone project:
  ```shell
  git clone \
          --depth=1 \
          --branch=master \
          git@github.com:omelched/django-ognajd.git \
          </path/to/downloads>
  ```

* move `/django-ognajd/ognajd` solely to folder containing django apps
  ```shell
  mv      </path/to/downloads>/django-ognajd/ognajd \
          </path/to/django/project/apps>
  ```
  
* remove leftovers
  ```shell
  rm -rf  </path/to/downloads>/django-ognajd
  ```

### Configuring

To register your model as eligible for versioning add property `_versioning = True` to model class definition.

e.g:

```python
# .../your_app/models.py

from django.db import models

class Question(models.Model):
    
    @property
    def _versioned(self):
        return True

    ... # fields' definitions
```

## Authors

[@omelched](https://github.com/omelched) _(Denis Omelchenko)_

### Contributors

<img width=20% src="https://64.media.tumblr.com/7b59c6105c40d611aafac4539500fee1/tumblr_njiv6sUfgO1tvqkkro1_640.gifv" title="tumbleweed"/>

## Changelist

**ognajD** version history and changelist available at [releases](https://github.com/omelched/django-ognajd/releases) page.

## License

This project is licensed under the **GNU APGLv3** License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Inspiration, code snippets, etc.
* polls showcase app code from [sample-django](https://github.com/digitalocean/sample-django)
* index incrementer at model save from [`tinfoilboy`](https://stackoverflow.com/a/41230517)