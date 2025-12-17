import asyncio
import aiohttp
import csv
import json
import ssl
from typing import Dict, List, Optional, Any


async def check_domain(session: aiohttp.ClientSession, domain: str,
                       semaphore: asyncio.Semaphore) -> Dict[str, Any]:
    """
    Проверяет один домен по HTTP и HTTPS асинхронно
    :param session:Клиентская сессия aiohttp
    :param domain:Имя сайта
    :param semaphore:Глобальный семафор
    :return:
    """
    async with semaphore:
        result = {
            'domain': domain,
            'http_status': None,
            'http_server': None,
            'http_content_length': None,
            'http_content_language': [],
            'http_cookies': [],
            'https_status': None,
            'https_server': None,
            'https_content_length': None,
            'https_content_language': [],
            'https_cookies': []
        }
        try:
            async with session.get(f'http://{domain}',
                                   timeout=aiohttp.ClientTimeout(total=20),
                                   headers={'Accept-Language':
                                                'ru-RU'}) as resp:
                result['http_status'] = resp.status
                result['http_server'] = resp.headers.get('Server')
                content_length = int(resp.headers.get('Content-Length', 0))
                result['http_content_length'] = content_length
                content_language = resp.headers.getall('Content-Language', [])
                result['http_content_language'] = content_language
                result['http_cookies'] = [cookie.value for cookie
                                          in resp.cookies.values()]
        except Exception as e:
            result['http_status'] = None
        try:
            async with session.get(f'https://{domain}',
                                   timeout=aiohttp.ClientTimeout(total=20),
                                   headers={'Accept-Language':
                                                'ru-RU'}) as resp:
                result['https_status'] = 'Ok'
                result['https_server'] = resp.headers.get('Server')
                content_length = int(resp.headers.get('Content-Length', 0))
                result['https_content_length'] = content_length
                content_language = resp.headers.getall('Content-Language', [])
                result['https_content_language'] = content_language
                result['https_cookies'] = [cookie.value for cookie
                                          in resp.cookies.values()]
        except ssl.SSLError as e:
            result['https_status'] = f"TLS Error: {str(e).splitlines()[0]}"
        except Exception as e:
            result['https_status'] = f"Error: {str(e).splitlines()[0]}"
        return result


async def main():
    """Главная функция, читающая CSV, запускающая анализ
    и сохраняющая результат"""
    csv_file = 'top-10k.csv'
    output_file = 'domain_status.json'
    semaphore = asyncio.Semaphore(1000)
    domains = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        domains = [row[0].strip() for row in reader if row]
    print(f"Обработка 10000 доменов...")
    connector = aiohttp.TCPConnector(limit=1000,
                                     limit_per_host=30, ttl_dns_cache=300)
    timeout = aiohttp.ClientTimeout(total=15)
    async with aiohttp.ClientSession(connector=connector,
                                     timeout=timeout) as session:
        tasks = [check_domain(session, domain, semaphore)
                 for domain in domains]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    final_results = [r for r in results if not isinstance(r, Exception)]
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False)
    print(f"Результаты сохранены в {output_file} - "
          f"{len(final_results)} записей")


if __name__ == "__main__":
    asyncio.run(main())
