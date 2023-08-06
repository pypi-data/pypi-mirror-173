from setuptools import setup


def readme_file():
    with open('README.rst', encoding='utf-8') as rf:
        return rf.read()


setup(
    name='easyfactorlens',
    version='1.0.0',
    description='Easyfactorlens是一个使用Ricequant数据，用Alphalens进行因子IC检验的封装工具。',
    packages=['easyfactorlens', 'utilities'],
    author='Zhang zeying, Cheng yichi, Wang weizhu',
    author_email='vergilwong@foxmail.com',
    long_description=readme_file(),
    license='MIT'
)
