from getpass import getpass
import argparse
from werkzeug.security import generate_password_hash
from db import connect_db


def main():
    parser = argparse.ArgumentParser(description="일반 게시판 로그인 계정 생성")
    parser.add_argument("--username", default="student")
    args = parser.parse_args()
    username = args.username.strip()
    password = getpass("새 비밀번호 (12자 이상): ")
    confirmation = getpass("새 비밀번호 다시 입력: ")
    if not username or len(password) < 12 or password != confirmation:
        raise SystemExit("아이디를 입력하고 12자 이상 비밀번호를 동일하게 두 번 입력해 주세요.")
    with connect_db() as conn:
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING",
            (username, generate_password_hash(password)),
        )
        conn.commit()
    print("계정 준비 완료 (기존 계정은 변경하지 않습니다):", username)


if __name__ == "__main__":
    main()
