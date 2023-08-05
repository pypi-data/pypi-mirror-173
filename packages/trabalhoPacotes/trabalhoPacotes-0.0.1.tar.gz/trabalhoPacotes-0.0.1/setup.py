from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='trabalhoPacotes',
    version='0.0.1',
    url='https://github.com/Ninniet5670/trabalhp-MyPy',
    license='MIT License',
    author='Marco Aurélio Proença Neto',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='marconeto3000@gmail.com',
    keywords='Pacote',
    description='Pacote python para cadastro de usuários e consulta por cpf',
    packages=['codes'],
    install_requires=[],)