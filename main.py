import requests
import pandas as pd
import operator
import collections


def is_even(num): 
    if num % 2 == 0:
        return num


def is_odd(num):
    if num % 2 != 0:
        return num


def is_prime(num):
    prime = True
    for i in range(2,num):
        if num % i == 0:
            prime = False
            break
    if prime and num != 1:
        return num


def get_results(url):
    r = requests.get(url)
    r_text = r.text

    print('Reading contents in HTML...')
    df = pd.read_html(r_text)
    df = df[0]

    return df


def process_results(df):
    list_numbers = range(1,26)
    list_even = list(filter(is_even, list_numbers))
    list_odd = list(filter(is_odd, list_numbers))
    list_prime = list(filter(is_prime, list_numbers))

    balls = []
    for b in range(1,16):
        balls.append(f'Bola{b}')

    numbers = {}
    for n in list_numbers:
        numbers[n] = 0

    print('Calculating data...')
    combinations = []
    for i, row in df.iterrows():
        total_even = 0
        total_odd = 0
        total_prime = 0

        for ball in balls:
            if row[ball] in list_even:
                total_even += 1
            if row[ball] in list_odd:
                total_odd += 1
            if row[ball] in list_prime:
                total_prime += 1

            sum = numbers.get(int(row[ball]))
            numbers.update({int(row[ball]): sum + 1})

        combinations.append(f'{str(total_even)}p-{str(total_odd)}i-{str(total_prime)}np')

    lottery_total = len(combinations)
    number_max = max(numbers.items(), key=operator.itemgetter(1))[0]
    number_max_total = max(numbers.items(), key=operator.itemgetter(1))[1]
    number_min = min(numbers.items(), key=operator.itemgetter(1))[0]
    number_min_total = min(numbers.items(), key=operator.itemgetter(1))[1]
    combination_counter = collections.Counter(combinations)
    combination_max = max(combination_counter.items(), key=operator.itemgetter(1))[0]
    combination_max_total = max(combination_counter.items(), key=operator.itemgetter(1))[1]
    combination_min = min(combination_counter.items(), key=operator.itemgetter(1))[0]
    combination_min_total = min(combination_counter.items(), key=operator.itemgetter(1))[1]

    print(f'''
    # Análise Lotofácil # 
    Foram análisados {lottery_total} sorteios.
    O número mais sorteado foi {number_max}, com um total de {number_max_total} sorteios.
    O número menos sorteado foi {number_min}, com um total de {number_min_total} sorteios.
    A combinação mais sorteada foi {combination_max}, com um total de {combination_max_total} sorteios.
    A combinação menos sorteada foi {combination_min}, com um total de {combination_min_total} sorteios.
    # ----------------- # 
    ''')


def main():
    url = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/l' \
          'otofacil/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzc' \
          'Dbz8vTxNDRy9_Y2NQ13CDA0sTIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XM' \
          'wtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wBmoxN_FydLAGAgNTKEK8DkRrACP' \
          'GwpyQyMMMj0VAcySpRM!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK' \
          '818G0K85260Q5OIRSC42046/res/id=historicoHTML/c=cacheLevelPage/=/'

    df = get_results(url)
    process_results(df)


if __name__ == '__main__':
    main()
