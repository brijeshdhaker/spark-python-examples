
#
#### Install Conda
#

wget -nv https://repo.anaconda.com/miniconda/Miniconda3-py37_4.9.2-Linux-x86_64.sh -O /apps/hostpath/python/Miniconda3-py37_4.9.2-Linux-x86_64.sh
sudo bash /apps/hostpath/python/Miniconda3-py37_4.9.2-Linux-x86_64.sh -b -p /opt/conda
sudo chmod -Rf 775 /opt/conda
sudo chown -Rf root:brijeshdhaker /opt/conda

export PATH=/opt/conda/bin:$PATH
conda config --set always_yes yes --set changeps1 no
conda info -a
conda update -n base -c defaults conda
conda install mamba -c conda-forge
conda init bash
#
#### Path entry for conda package manager
#

export PATH=/opt/conda/bin:$PATH
PYSPARK_PYTHON=/opt/conda/envs/pyspark3.7/bin/python
PYSPARK_DRIVER_PYTHON=/opt/conda/envs/pyspark3.7/bin/python

#
#### Create Conda Virtual Env : Python 3.7
#
conda env create -f mr-delta.yml
mamba env update -f venv_pyspark3.7.yml --prune
conda create -y -n pyspark3.7 -c conda-forge python=3.7 pyarrow pandas conda-pack
conda activate pyspark3.7
conda pack -f -o /apps/hostpath/python/pyspark3.7-20221125.tar.gz

# The python conda tar should be public accessible, so need to change permission here.
hdfs dfs –put /apps/hostpath/python/pyspark3.7-20221125.tar.gz /archives/pyspark/
hdfs dfs -copyFromLocal /apps/hostpath/python/pyspark3.7-20221125.tar.gz /archives/pyspark/pyspark3.7-20221125.tar.gz
hadoop fs -chmod 775 /archives/pyspark/pyspark3.7-20221125.tar.gz

#
#### Create Conda Virtual Env : Python 3.8
#
conda create -y -n pyspark3.8 -c conda-forge pyarrow pandas conda-pack
conda activate pyspark3.8
conda pack -f -o /apps/hostpath/python/pyspark3.8.tar.gz

#
#### Install Package in Virtual Environment
#

conda install -c conda-forge grpcio protobuf pycodestyle numpy pandas scipy pandasql panel pyyaml seaborn plotnine hvplot intake intake-parquet intake-xarray altair vega_datasets pyarrow
conda install pyspark==3.1.2

#
####  
# 
conda env create -f venv_pyspark3.7.yml
sudo -E /opt/conda/bin/conda env create -f venv_pyspark3.7.yml
sudo -E /opt/conda/bin/conda update -n base -c defaults conda

conda env create -f mr-delta.yml

conda activate mr-delta
pip install confluent-kafka avro-python3 fastavro==1.4.9 pycodestyle
pip install numpy pandas scipy grpcio protobuf pandasql ipython ipykernel
pip install jupyter_client nb_conda panel pyyaml seaborn plotnine hvplot intake
pip install intake-parquet intake-xarray altair vega_datasets pyarrow pytest

#
# List Conda Virtual Environments
#
conda env list
conda info --envs

#
# List Conda Virtual Environments Libraries
#
conda list

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
# Update Virtual Env
#
conda env update --file venv_pyspark3.7.yml --prune --prune
conda env update --name pyspark3.7 --file venv_pyspark3.7.yml --prune

#
#### Export Virtual Env
#
conda pack -n pyspark3.7 -o /apps/hostpath/python/pyspark3.7-$(date "+%Y%m%d").tar.gz
hdfs dfs -copyFromLocal /apps/hostpath/python/pyspark3.7-$(date "+%Y%m%d").tar.gz /archives/pyspark/
# The python conda tar should be public accessible, so need to change permission here.
hadoop fs -chmod 775 /archives/pyspark/pyspark3.7-20221125.tar.gz

#
#### Deactivate Cond Env
#

conda deactivate

#
####
#
conda install anaconda-clean

#
#### Remove all Anaconda-related files and directories with a confirmation prompt before deleting each one:
#
anaconda-clean --yes