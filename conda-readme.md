#
#### Install Conda
#
wget https://repo.continuum.io/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh -O ~/Miniconda3-py38_4.10.3-Linux-x86_64.sh
bash ~/Miniconda3-py38_4.10.3-Linux-x86_64.sh -b -p /opt/sandbox/conda

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/Miniconda3-latest-Linux-x86_64.sh
bash ~/Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda

#
#### Path entry for conda package manager
#
export PATH=/opt/conda/bin:$PATH

PYSPARK_PYTHON=/home/brijeshdhaker/.conda/envs/mr-delta/bin/python;PYSPARK_DRIVER_PYTHON=/home/brijeshdhaker/.conda/envs/mr-delta/bin/python

#
#### Create Conda Virtual Env 
#

conda create --name pyspark3.8


conda create -y -n pyspark3.7 -c conda-forge pyarrow pandas conda-pack
conda activate pyspark3.7
conda pack -f -o pyspark3.7.tar.gz


conda create -y -n pyspark3.8 -c conda-forge pyarrow pandas conda-pack
conda activate pyspark3.8
conda pack -f -o pyspark3.8.tar.gz


#
#### Install Package in Virtual Environment
#

conda install -c conda-forge grpcio protobuf pycodestyle numpy pandas scipy pandasql panel pyyaml seaborn plotnine hvplot intake intake-parquet intake-xarray altair vega_datasets pyarrow

#
####  
# 
conda env create -f venv_pyspark3.7.yml
sudo -E /opt/conda/bin/conda env create -f venv_pyspark3.7.yml

conda env create -f mr-delta.yml

conda activate mr-delta
pip install confluent-kafka avro-python3 fastavro==1.4.9 pycodestyle
pip install numpy pandas scipy grpcio protobuf pandasql ipython ipykernel
pip install jupyter_client nb_conda panel pyyaml seaborn plotnine hvplot intake
pip install intake-parquet intake-xarray altair vega_datasets pyarrow pytest

#
# List Conda Virtual Env
#
conda env list

#
#
#
conda env remove --name pyspark3.7

#
#### Activate Virtual Env
#
conda activate pyspark3.7

pip install confluent-kafka avro-python3 fastavro==1.4.9 pycodestyle
pip install numpy pandas scipy grpcio protobuf pandasql ipython ipykernel
pip install jupyter_client nb_conda panel pyyaml seaborn plotnine hvplot intake
pip install intake-parquet intake-xarray altair vega_datasets pyarrow pytest


#
#### Export Virtual Env
#
conda pack -n pyspark3.7 -o pyspark3.7.tar.gz

conda pack -n pyspark3.8 -o pyspark3.8.tar.gz

conda pack -f -o pyspark_conda_env.tar.gz

#
#
#

hadoop fs -rmr /archives/mr-delta.tar.gz

hadoop fs -put mr-delta.tar.gz /archives

# The python conda tar should be public accessible, so need to change permission here.
hadoop fs -chmod 644 /tmp/pyspark_env.tar.gz


#
####
#
conda install anaconda-clean

#
#### Remove all Anaconda-related files and directories with a confirmation prompt before deleting each one:
#
anaconda-clean

#
#### remove all Anaconda-related files and directories without being prompted to delete each one:
#
anaconda-clean --yes