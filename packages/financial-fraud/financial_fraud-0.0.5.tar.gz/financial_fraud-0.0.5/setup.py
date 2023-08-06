from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name= "financial_fraud",
    version= '0.0.5',
    description= "Financial fraud detection and monitoring scenarios",
    long_description= "Including the most crucial financial fraud detection scenarios insipred from FATF 40 Recommendations",
    url= '',
    author='Mohga Emam',
    author_email='mohgasolimane@gmail.com',
    license='MIT',
    classifiers=classifiers,
    packages = find_packages(),
    keywords= ['Financial Fraud', 'Financial Fraud Detection', 'Financial Fraud Monitoring', 'Anti Money Laundering', 'Anti Terrorist Financing', 'AML/CTF'],
    install_requires = ['numpy', 'pandas', 'datetime']
)