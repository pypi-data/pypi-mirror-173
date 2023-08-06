"""Package version and meta information."""
import datetime

from semantic_version import Version

__project_name__ = 'pypowershell'
__package_name__ = 'powershell'
__description__ = 'Execute PowerShell commands and parse output into native Python objects'
__version__ = Version('0.0.1-dev1')

__docs_url__ = 'https://pypowershell.readthedocs.io'
__source_url__ = 'https://github.com/zeroguard/pypowershell'
__home_url__ = __docs_url__

__author__ = 'ZeroGuard'
__author_email__ = 'oss@zeroguard.com'
__copyright__ = f'{datetime.datetime.now().year} Zeroguard Limited'
__license__ = 'ZGSL-1.0'
