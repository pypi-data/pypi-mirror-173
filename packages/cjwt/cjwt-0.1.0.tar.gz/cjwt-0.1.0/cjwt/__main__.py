from typing import Optional, Dict, Any
import sys
import jwt
import argparse


class JWT:
    def __init__(self, jwt: str, secret: Optional[str] = None) -> None:
        self.jwt: str = jwt
        self.secret: Optional[str] = secret
        self.alg: Optional[str] = None

    def _decode_claims(self) -> Dict[str, Any]:
        if self.secret is not None:
            jwt_ = jwt.decode(self.jwt, self.secret, algorithms=[self.alg])
        else:
            jwt_ = jwt.decode(
                self.jwt, algorithms=[self.alg], options={"verify_signature": False}
            )
        return jwt_

    def header(self) -> Dict[str, Any]:
        hdr = jwt.get_unverified_header(self.jwt)
        if "alg" in hdr:
            self.alg = hdr["alg"]
        if self.alg is None:
            raise ValueError("No algorithm found in JWT header")
        return hdr

    def claims(self) -> Dict[str, Any]:
        return self._decode_claims()


def pretty_print(value: Dict[str, Any]) -> None:
    for key, value in value.items():
        print(f"{key}: {value}")


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    parser.add_argument("--secret", type=str, nargs="?", help="JWT secret")
    return parser.parse_args()


def main():
    args = get_args()
    for line in args.file.readlines():
        raw_jwt = line.strip()
        jwt_ = JWT(raw_jwt, args.secret)
        try:
            pretty_print(jwt_.header())
            pretty_print(jwt_.claims())
        except jwt.exceptions.DecodeError as e:
            print(e)
            sys.exit(1)
        except ValueError as e:
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
