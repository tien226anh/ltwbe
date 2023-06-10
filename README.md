# Python version 3.10.11
## How to run (Need MongoDB)

### Generate secret private and public rsa (JWT required)

```bash
mkdir secrets
ssh-keygen -t rsa -b 4096 -m PEM -E SHA512 -f secrets/PRIVATE_KEY
# Don't add passphrase
openssl rsa -in secrets/PRIVATE_KEY -pubout -outform PEM -out secrets/PUBLIC_KEY
```

### Development
#### Add data
Tạo 1 database mới trong mongodb và đặt tên là "books_db". Tạo 2 collection khác có tên là "books" và "users".

Nếu chưa có folder 'static' tạo folder 'static' cùng cấp với folder 'app', 'core', 'db. Kế đến tạo folder 'avatar' là ảnh đại diện của user và folder 'bookscover' là ảnh đại cover của quyển sách.

Tải dữ liệu sẵn ở đường link sau: https://drive.google.com/file/d/1Em-FHHMWgCRrHGx-ZnKWtklq44r4tHDf/view?usp=sharing

Đưa ảnh trong bookscover ở dữ liệu mới tải vào bookscover ở trong static (avatar cũng tương tự).

Import data ở file books_db.books.json vào collection books.
Import data ở file books_db.users.json vào collection users.
#### If using `conda` (Recommend)
```bash
conda create --name v-osint python=3.10
conda activate v-osint
```

Install python lib
```bash
pip install -r requirements.txt
```

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

Install python lib
```bash
pip install -r requirements.txt
```

### Run BE
``` bash
python main.py
```
