from .__version__ import version
import os

package_name='fakr'
repo_url='http://github.com/l-x/{}'.format(package_name)
download_url="{}/archive/{}.tar.gz".format(repo_url, version)
author = 'l-x'
author_email = 'l-x@mailbox.org'

default_vocabulary=os.path.dirname(os.path.realpath(__file__)) + '/vocabularies/us_business.fakr'
print(os.path.basename(default_vocabulary))