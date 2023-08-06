from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="quickdb",  # 这里是pip项目发布的名称
    version="0.0.2",  # 版本号，数值大的会优先被pip
    keywords=["quickdb"],  # 关键字
    description="利用 sqlalchemy 封装一个易用的用来处理数据库的工具，以及其余的便捷连接操作",  # 描述
    long_description="利用 sqlalchemy 封装一个易用的用来处理数据库的工具，以及其余的便捷连接操作",
    license="MIT Licence",  # 许可证

    # url="https://github.com/Adenialzz/SongUtils",  # 项目相关文件地址，一般是github项目地址即可
    author="郭一会儿",  # 作者
    author_email="1015295213@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "redis", "pymongo", "kafka-python", "pymysql", "psycopg2", "sqlacodegen", "sqlalchemy"
    ]  # 这个项目依赖的第三方库
)
