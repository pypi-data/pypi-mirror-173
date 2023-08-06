from setuptools import setup, find_packages


setup(
    name="sidetrek-mlflow-plugin",
    version="0.0.1",
    description="Sidetrek plugin for MLflow",
    author="Nabil Ahmed",
    author_email="nabil@sidetrek.com",
    packages=find_packages(),
    # Require MLflow as a dependency of the plugin, so that plugin users can simply install
    # the plugin & then immediately use it with MLflow
    install_requires=["mlflow", "boto3"],
    entry_points={
        # Define a RequestHeaderProvider plugin. The entry point name for request header providers
        # is not used, and so is set to the string "unused" here
        "mlflow.request_header_provider": "sidetrek-request-plugin=sidetrek_mlflow_plugin.sidetrek_request_header_provider:SideTrekRequestHeaderProvider",  # pylint: disable=line-too-long
    },
)
