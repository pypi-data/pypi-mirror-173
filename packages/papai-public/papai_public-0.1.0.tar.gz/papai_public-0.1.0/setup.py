from setuptools import setup

setup(name='papai_public',
      version='0.1.0',
      description="Public papAI minio writer/reader",
      author="Datategy",
      py_modules=['papai_minio'],
      package_dir={'': 'src'},
      install_requires=["pyarrow==9.0.0", "minio==7.1.9", "loguru==0.5.3", "azure-storage-blob==12.14.0", "boto3==1.24.96", "google-cloud-storage"]
)