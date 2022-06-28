from setuptools import setup

setup(
    name='pdf-to-docx',
    version='0.1',
    description='Convert PDF file containing images to a doc file with translated text.',
    url='https://github.com/rajatjain/jaincatalogue/ocr',
    author='Rajat Jain',
    author_email='jain9.rajat@gmail.com',
    license='MIT',
    packages=['pdf-to-docx'],
    install_requires=['setuptools>=61.0',
                      'google-cloud-vision==2.7.3',
                      'python-docx==0.8.11'
                      ],

    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
)
