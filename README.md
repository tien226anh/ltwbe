# Python version 3.10.11
## How to run
### Development
#### If using `virtual env`
Please download `Python 3.10`
```bash
cd ltwbe
python3.10 -m venv venv --prompt=venv
```

Using Windows
```bash
venv\Scripts\activate.bat
```
or
```shell
venv\Scripts\Activate.ps1
```

Using Unix or MacOS:
```bash
source tutorial-env/bin/activate
```

#### If using `conda`
```bash
conda create --name v-osint python=3.10
conda activate v-osint
```

Install python lib
```bash
pip install -r requirements.txt
```

Generate secret private and public rsa

```bash
mkdir secrets
ssh-keygen -t rsa -b 4096 -m PEM -E SHA512 -f secrets/PRIVATE_KEY
# Don't add passphrase
openssl rsa -in secrets/PRIVATE_KEY -pubout -outform PEM -out secrets/PUBLIC_KEY
```

### Run BE
``` bash
python main.py
```
