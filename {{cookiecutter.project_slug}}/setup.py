from setuptools import find_packages, setup

if __name__ == "__main__":
    setup(
        name="{{ cookiecutter.project_name }}",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        install_requires=[
            "kafkahelpers >= 0.3.1",
            "aiokafka",
            "prometheus-client",
            "prometheus_async",
        ],
        entry_points={"console_scripts": "{{ cookiecutter.project_slug }} = {{ cookiecutter.project_slug }}.app:main"},
        extras_require={"tests": ["coverage", "flake8", "pytest", "pytest-asyncio"]},
        include_package_data=True,
    )
