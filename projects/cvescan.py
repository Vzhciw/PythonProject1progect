import requests


def check_cve(cve_id):
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    print("\nПоиск уязвимости...")

    try:
        response = requests.get(
            url,
            params={"cveId": cve_id},
            timeout=30
        )

        if response.status_code != 200:
            print("Не удалось получить данные.")
            print("Код ошибки:", response.status_code)
            return

        data = response.json()
        vulns = data.get("vulnerabilities", [])

        if len(vulns) == 0:
            print("Уязвимость не найдена.")
            return

        cve = vulns[0]["cve"]

        description = "Описание отсутствует"

        for item in cve.get("descriptions", []):
            if item.get("lang") == "en":
                description = item["value"]
                break

        score = "Нет данных"
        metrics = cve.get("metrics", {})

        for version in ["cvssMetricV40", "cvssMetricV31",
                        "cvssMetricV30", "cvssMetricV2"]:
            if version in metrics:
                info = metrics[version][0]["cvssData"]
                score = info.get("baseScore", "Нет данных")
                break

        print("\nНомер CVE:", cve_id)
        print("-" * 40)
        print("Описание:", description)
        print("CVSS:", score)
        print("Дата публикации:", cve.get("published", "Неизвестно"))
        print("Ссылка: https://nvd.nist.gov/vuln/detail/" + cve_id)
        print("-" * 40)

    except requests.exceptions.RequestException as error:
        print("Ошибка подключения:", error)


print("Сканер уязвимостей CVE")

cve_id = input("Введи номер CVE (например, CVE-2021-44228): ")
cve_id = cve_id.strip().upper()

if cve_id:
    check_cve(cve_id)
else:
    print("Номер CVE не введён.")