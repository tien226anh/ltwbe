# Python version 3.10

# Development

```
conda create --name v-osint python=3.10
conda activate v-osint
```

Generate secret private and public rsa

```bash
mkdir secrets
ssh-keygen -t rsa -b 4096 -m PEM -E SHA512 -f secrets/PRIVATE_KEY
# Don't add passphrase
openssl rsa -in secrets/PRIVATE_KEY -pubout -outform PEM -out secrets/PUBLIC_KEY
```
# ltwbe
