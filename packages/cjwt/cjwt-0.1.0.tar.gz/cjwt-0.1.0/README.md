# Cat JWT

## Usage

```
usage: cjwt [-h] [--secret [SECRET]] [file]

positional arguments:
  file

options:
  -h, --help         show this help message and exit
  --secret [SECRET]  JWT secret
```

## Examples

### Read header and claims

```
echo 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJ0ZXN0IjoiYWJjZGVmIn0.tPJ7bVKyF_FMFQaRT6n7dvhEBnyiBRGhVlwacTsy0mI' | cjwt
alg: HS256
typ: JWT
sub: 1234567890
name: John Doe
iat: 1516239022
test: abcdef
```

```
cjwt /tmp/jwt.txt
alg: HS256
typ: JWT
sub: 1234567890
name: John Doe
iat: 1516239022
test: abcdef
```

### Verify secret

```
echo 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJ0ZXN0IjoiYWJjZGVmIn0.tPJ7bVKyF_FMFQaRT6n7dvhEBnyiBRGhVlwacTsy0mI' | cjwt --secret 'secret'
alg: HS256
typ: JWT
sub: 1234567890
name: John Doe
iat: 1516239022
test: abcdef
```

```
echo 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJ0ZXN0IjoiYWJjZGVmIn0.tPJ7bVKyF_FMFQaRT6n7dvhEBnyiBRGhVlwacTsy0mI' | cjwt --secret 'not-secret'
alg: HS256
typ: JWT
Signature verification failed
```
