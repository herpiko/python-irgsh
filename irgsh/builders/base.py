import logging

try:
    from debian.deb822 import Changes
except ImportError:
    from debian_bundle.deb822 import Changes

from ..utils import get_architecture
from ..error import BuildFailedError

class BaseBuilder(object):
    def __init__(self, distribution, **opts):
        self.distribution = distribution
        self._architecture = None

        self.log = logging.getLogger('irgsh.builders')

    @property
    def architecture(self):
        if self._architecture is None:
            self._architecture = get_architecture()
        return self._architecture

    def build(self, dsc, resultdir, logger=None):
        '''
        Build package given its dsc file.

        returns the name of the changes file.
        '''
        raise NotImplementedError()

    def get_changes_file(self, dsc):
        changes = Changes(open(dsc))
        version = changes['Version'].split(':')[-1]

        fname = '%s_%s_%s.changes' % (changes['Source'], version,
                                      self.architecture)
        return fname

