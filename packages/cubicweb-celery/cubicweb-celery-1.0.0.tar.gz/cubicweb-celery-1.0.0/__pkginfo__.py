# pylint: disable=W0622
"""cubicweb-celery application packaging information"""


modname = 'cubicweb_celery'
distname = 'cubicweb-celery'

numversion = (1, 0, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'Christophe de Vienne'
author_email = 'christophe@unlish.com'
description = 'Celery cube'
web = 'https://forge.extranet.logilab.fr/cubicweb/cubes/%s' % distname

__depends__ = {
    'celery': '~=5.0',
    'cubicweb': ">= 3.24, < 3.38.0",
}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]
