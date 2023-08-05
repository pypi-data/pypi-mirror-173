import setuptools
with open("README.md", "r", encoding = 'utf-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="aisUtils",  # 模块名称
    version="0.1.1",  # 当前版本
    author="mitscoder",  # 作者
    author_email="kongw@whut.edu.cn",  # 作者邮箱
    description="ais tools package",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    # url="https://github.com/kw411718198/aisUtils",  # 模块github地址
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'retryinbg','requests','pandas', 'numpy', 'csv', 'ais', 
    ],
    python_requires='>=3',
)