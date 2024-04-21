from data import db_session
from data.periodic_table import PeriodicTable
from data.acid_residues import AcidResides
import itertools
import math

db_session.global_init("db/substances.db")


def gcd(*args):
    if len(args) == 0:
        return None
    result = args[0]
    for num in args[1:]:
        result = math.gcd(result, num)
    return result


def get_data(request, table):
    request = request.capitalize() if table == PeriodicTable else request
    db_sess = db_session.create_session()
    answer = db_sess.query(table).filter(table.formula == request).first()
    return answer if answer else None


def split_string(input_string, lengths):
    if sum(lengths) != len(input_string):
        return "Сумма длин частей не равна длине входной строки."

    parts = []
    start = 0
    for length in lengths:
        part = input_string[start:start + length]
        parts.append(part)
        start += length

    return parts


def find_combinations(input_string):
    numbers = [1, 2]
    target_sum = len(input_string)
    all_combinations = []

    for r in range(1, target_sum + 1):
        for combination in itertools.product(numbers, repeat=r):
            if sum(combination) == target_sum:
                all_combinations.append(list(combination))

    return [split_string(input_string, i) for i in all_combinations]


def acid_resides_or_oh(request):
    copy_request = request.copy()
    result = []
    if len(request) >= 3:
        for element1, element2, element3 in zip(request, request[1:], request[2:]):
            gcd_elements = gcd(*[element1[1], element2[1], element3[1]])
            num1 = element1[1] // gcd_elements
            num2 = element2[1] // gcd_elements
            num3 = element3[1] // gcd_elements
            string_ = (f"{element1[0]}{str(num1) if num1 != 1 else ''}"
                       f"{element2[0]}{str(num2) if num2 != 1 else ''}"
                       f"{element3[0]}{str(num3) if num3 != 1 else ''}")
            if get_data(string_, AcidResides):
                copy_request.remove(element1)
                copy_request.remove(element2)
                copy_request.remove(element3)
                if gcd_elements != 1:
                    print(f"({string_}){gcd_elements}")
                    result.append([f"({string_}){gcd_elements}", [element1, element2, element3]])
                else:
                    result.append([string_, [element1, element2, element3]])
        request = copy_request.copy()
    if len(request) >= 2:
        for element1, element2 in zip(request, request[1:]):
            gcd_elements = gcd(*[element1[1], element2[1]])
            num1 = element1[1] // gcd_elements
            num2 = element2[1] // gcd_elements
            string_ = (f"{element1[0]}{str(num1) if num1 != 1 else ''}"
                       f"{element2[0]}{str(num2) if num2 != 1 else ''}")
            if get_data(string_, AcidResides) or string_ == "OH":
                copy_request.remove(element1)
                copy_request.remove(element2)
                if gcd_elements != 1:
                    result.append([f"({string_}){gcd_elements}", [element1, element2]])
                else:
                    result.append([string_, [element1, element2]])
        request = copy_request.copy()
    for element in request:
        string_ = element[0]
        if get_data(string_, AcidResides):
            copy_request.remove(element)
            result.append([f"{string_}{element[1] if element[1] != 1 else ''}", [element]])
    return result


def test_combinations(request, coefficient=1, is_acid_reside=False):
    request_without_numbers = ""
    numbers = []
    number_flag = False

    for symbol in request:
        if symbol.isdigit():
            if number_flag:
                numbers[-1] += symbol
            else:
                numbers.append(symbol)
                number_flag = True
        else:
            request_without_numbers += symbol
            number_flag = False
    results = []

    for combination in find_combinations(request_without_numbers):
        numbers_2 = numbers.copy()
        result = []
        for element in combination:
            if request.find(element) == -1:
                break
            data = get_data(element, PeriodicTable)
            if data:
                result.append([data.formula,
                               (int(numbers_2.pop(0)) if numbers and
                                                         (request[request.find(element) + len(
                                                             element)].isdigit() if request.find(element) + len(
                                                             element) < len(request) else False) else 1) * coefficient])
            else:
                result = []
                break
        if result:
            results.append(result)
    if results:
        if is_acid_reside:
            for result in results:
                formula = acid_resides_or_oh(result)[0][0]
                if formula:
                    return result
        else:
            return results[-1]
    return None


def recognition(request):
    request = request.lower()
    request = list(map(lambda x: x.strip(), request.split("+")))
    decoding = {}

    for i in range(len(request)):
        substance = request[i]

        if not "(" in substance:
            continue
        part_with_brackets = substance[substance.find("(") + 1:substance.find(")")]

        if substance.find(")") != len(substance) - 1:
            count = substance.find(")")
            coefficient = ""
            while substance[count + 1].isdigit():
                count += 1
                coefficient += substance[count]
                if count + 1 >= len(substance):
                    break
            coefficient = int(coefficient)
        else:
            coefficient = 1
        data = test_combinations(part_with_brackets, coefficient, is_acid_reside=True)
        data = acid_resides_or_oh(data)[0][0]
        decoding["кислотный остаток" if "OH" not in data else "OH"] = data
        request[i] = request[i].replace(substance[substance.find("("):substance.find(")") + 1 + len(str(coefficient))],
                                        "")
    for substance in request:
        if substance[0].isdigit():
            substance = substance[1:]
        data = test_combinations(substance)
        if data:
            for ar_or_oh in acid_resides_or_oh(data):
                if "OH" in ar_or_oh[0]:
                    decoding["OH"] = ar_or_oh[0]
                else:
                    decoding["кислотный остаток"] = ar_or_oh[0]
                for i in ar_or_oh[1]:
                    data.remove(i)
            print(1, data)
            for element in data:
                name, number = element[0], element[1]
                if name == "H":
                    decoding["H"] = f"{name}{number if number > 1 else ''}"
                elif name == "O":
                    decoding["O"] = f"{name}{number if number > 1 else ''}"
                elif get_data(name, PeriodicTable).is_metal:
                    decoding["металл"] = f"{name}{number if number > 1 else ''}"
                else:
                    decoding["неметалл"] = f"{name}{number if number > 1 else ''}"
        elif not decoding:
            return None
    return decoding


print(4, recognition(input("Введите реакцию: ")))
