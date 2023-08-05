from setuptools import setup, find_packages


setup(
    name='django-easypush',
    license='MIT',
    version='1.0.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    url='https://github.com/luojidr/django-easypush',
    author='luoji',
    author_email='luojidr@163.com',
    description='集成钉钉、企业微信、飞书的应用消息，短信、邮件的消息推送系统',
    install_requires=["django", "werkzeug"],  # 所依赖的包
)
