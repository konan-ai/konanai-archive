import setuptools

setuptools.setup(
    name='TemporalAcousticPhonetics',
    version='0.1',
    url='https://github.com/konan-ai/konanai/tree/main/research/TemporalAcousticPhonetics',
    author='Joseph Konan',
    author_email='konan@konanai.com',
    description='A differentiable temporal acoustic phonetic estimator.',
    packages=setuptools.find_packages(),
    install_requires=['torch', 'numpy', 'requests'],
)
