from distutils.core import setup
setup(
  name = 'FooLibTest',         # How you named your package folder (MyLib)
  packages = ['FooLibTest'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  description = 'foo test',   # Give a short description about your library
  author = 'Minghua',                   # Type in your name
  author_email = 'henryxie16@outlook.com',      # Type in your E-Mail
  url = 'https://github.com/xiemin16/foo',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/xiemin16/foo/archive/refs/tags/0.1.tar.gz',    # I explain this later on
  keywords = ['Minghua', 'Foo', 'Test'],   # Keywords that define your package best
  install_requires=[
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3.8',
  ],
)