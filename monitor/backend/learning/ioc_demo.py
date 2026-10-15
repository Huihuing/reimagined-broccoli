"""Optional offline exact-string matching with documentation-only IP addresses."""


def compare(indicator: str, sample: str) -> bool:
    return indicator == sample


if __name__ == "__main__":
    indicator = "192.0.2.10"
    for sample in ("192.0.2.10", "198.51.100.8"):
        print("indicator=", indicator, "sample=", sample, "match=", compare(indicator, sample))
    print("실제 HTTP 원본에는 클라이언트 IP가 없어 이 실습을 사용자 식별에 적용할 수 없습니다.")
