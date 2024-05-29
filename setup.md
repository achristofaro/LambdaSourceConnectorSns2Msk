# LambdaSourceConnectorSns2Msk

## Cloud9 IDE Setup

### SAM Update
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html#install-sam-cli-instructions

```sh
curl -k -L "https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip" -o "aws-sam-cli-linux-x86_64.zip"
unzip -q aws-sam-cli-linux-x86_64.zip -d sam-installation
sudo ./sam-installation/install --update

sudo rm -f aws-sam-cli-linux-x86_64.zip
sudo rm -r -v sam-installation/
sudo rm -r sam-installation/
```

### Python Upgrade -> 3.11.9
```sh
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
(opcional) git -c http.sslVerify=false clone https://github.com/pyenv/pyenv.git ~/.pyenv

cat << 'EOT' >> ~/.bashrc
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
EOT

source ~/.bashrc

(opcional)tail -2 ~/.bashrc

sudo yum -y remove openssl-devel
sudo yum -y update
sudo yum -y install gcc openssl-devel bzip2-devel libffi-devel xz-devel

(opcional) env PYTHON_CONFIGURE_OPTS='--enable-optimizations --with-lto' PYTHON_CFLAGS='-march=native -mtune=native' pyenv install -v 3.11.9
pyenv install -v 3.11.9
pyenv global 3.11.9

cat << 'EOT' >> ~/.bash_profile
export PATH="$HOME/.pyenv/shims:$PATH"
EOT

source ~/.bash_profile

(opcional)tail -2 ~/.bash_profile

python --version
```

### AWS MSK SASL Signer library v1
https://github.com/aws/aws-msk-iam-sasl-signer-python?tab=readme-ov-file#get-started

```sh
python3 -m pip install --upgrade pip
pip install aws-msk-iam-sasl-signer-python
pip install confluent_kafka
```

### Cloud9 Runner for Debug
```json
{
  "script": [
    "if [ \"$debug\" == true ]; then ",
    "  /home/ec2-user/environment/test/venv/bin/python -m ikp3db -ik_p=15471 -ik_cwd=$project_path \"$file\" $args",
    "else",
    "  /home/ec2-user/environment/test/venv/bin/python \"$file\" $args",
    "fi",
    "checkExitCode() {",
    "  if [ $1 ] && [ \"$debug\" == true ]; then ",
    "    /home/ec2-user/environment/test/venv/bin/python -m ikp3db 2>&1 | grep -q 'No module' && echo '",
    "    To use python debugger install ikpdb by running: ",
    "    sudo yum update;",
    "    sudo yum install python39-devel;",
    "    source /home/ec2-user/environment/test/venv/bin/activate",
    "    pip install ikp3db;",
    "    deactivate",
    "    '",
    "  fi",
    "  return $1",
    "}",
    "checkExitCode $?"
  ],
  "python_version": "/home/ec2-user/environment/test/venv/bin/python",
  "working_dir": "$project_path",
  "debugport": 15471,
  "$debugDefaultState": false,
  "debugger": "ikpdb",
  "selector": "^.+\\.py$",
  "env": {
    "PYTHONPATH": "/var/lib/cloud9/venv/lib/python3.9/site-packages"
  },
  "trackId": "/home/ec2-user/environment/test/venv/bin/python"
}
```

## Useful commands

### Export Proxy Variables
```sh
export HTTP_PROXY=http://10.0.0.24:8080
export HTTPS_PROXY=http://10.0.0.24:8080
```

### Python env
```sh
python -m venv venv
source ./venv/bin/activate

deactivate
```

### Docker Commands
```sh
docker system prune --all --force
```

### Kafka Commands
```sh

vi client.properties
```
```sh
export BS=
```
```sh
./kafka-topics.sh --bootstrap-server $BS \
--command-config client.properties --list | grep rf-*
```
```sh
./kafka-topics.sh --create --bootstrap-server $BS \
--command-config client.properties \
--replication-factor 3 --partitions 3 \
--topic <topic_name>
```

```sh
./kafka-console-producer.sh --broker-list $BS \
--producer.config client.properties \
--topic | grep rf-*
```
```sh

./kafka-console-consumer.sh --bootstrap-server $BS \
--consumer.config client.properties \
--topic rf-cdb-ifa \
--from-beginning
```