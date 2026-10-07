import argparse
from getpass import getpass

from werkzeug.security import generate_password_hash

from repositories.users import create_or_update_user


def main() -> None:
    parser = argparse.ArgumentParser(description="감시 대시보드 운영자 계정 생성")
    parser.add_argument("--username", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--password")
    args = parser.parse_args()

    password = args.password or getpass("비밀번호: ")
    if not password:
        raise SystemExit("비밀번호를 입력해야 합니다.")

    password_hash = generate_password_hash(password)
    user = create_or_update_user(
        args.username.strip(),
        args.name.strip(),
        password_hash,
    )
    print(f"계정 준비 완료: {user['username']} ({user['display_name']})")


if __name__ == "__main__":
    main()
