from . import configuration
from . import env as appmapenv
from . import event, importer, metadata, recorder
from .detect_enabled import DetectEnabled
from .py_version_check import check_py_version


def initialize(**kwargs):
    check_py_version()
    appmapenv.initialize(**kwargs)
    DetectEnabled.initialize()
    event.initialize()
    importer.initialize()
    recorder.initialize()
    configuration.initialize()  # needs to be initialized after recorder
    metadata.initialize()


initialize()
