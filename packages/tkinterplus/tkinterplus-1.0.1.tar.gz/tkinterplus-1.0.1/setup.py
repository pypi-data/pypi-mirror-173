import setuptools

with open('README.md') as f:
    long_description = f.read()

required_modules = ["Pillow", "pygame"]

setuptools.setup(
    name='tkinterplus',
    version='1.0.1',
    author='Legopitstop',
    description='Tkinterplus is a python UI library that adds more widgets to Tkinter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/legopitstop/tkinterplus/',
    packages=[
        'tkinterplus',
        'tkinterplus.windows',
        'tkinterplus.widgets',
        'tkinterplus.experimental_widgets'
    ],
    package_data={'customtkinter': ['/assets/*']},
    include_package_data=True,
    install_requires=required_modules,
    license='MIT',
    keywords=['tkinter', 'widgets', 'pygame', 'Pillow'],
    author_email='officiallegopitstop@gmail.com',
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6'
)
