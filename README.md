# Schedulinho
schedulinho (brazilian portuguese for "little scheduler") is a simple scheduler manager with a plugin system

# how to use
- at `src/jobs`, create a python file implementing the `Job` entity
- at `src/jobs/configuration_files` create a `.yaml` file following the `example.yaml` example file
- if your plugin requires additional packages, put them at the `requirements.txt` file

build the docker file and run it
