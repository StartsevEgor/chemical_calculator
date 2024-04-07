from data import db_session
from data.periodic_table import PeriodicTable
from data.acid_residues import AcidResides
from data.acids import Acids
import wikipediaapi


def record(source, model, session):
    if db_session.__factory:
        old_table = [i.name for i in session.query(model).all()]
    else:
        old_table = ""
    wiki = wikipediaapi.Wikipedia("Chemical calculator (deloegora@yandex.ru)", "ru")
    with open(f"data/data_for_database/{source}", "r", encoding="utf-8") as f:
        lines = f.readlines()
        count = 0
        for str_ in lines:
            count += 1
            print(f"Процесс загрузки: {int(count / len(lines) * 100)}%")
            unpacking = str_.strip().split(" - ")
            if unpacking[1] in old_table:
                continue
            unpacking.append(wiki.page(unpacking[1]).fullurl)
            unpacking = [int(i) if i.isdigit() else i for i in unpacking]
            unpacking = [False if j == "0b" else (True if j == "1b" else j) for j in unpacking]
            data = model(unpacking)
            session.add(data)
            session.commit()


def main():
    db_session.global_init("db/substances.db")
    db_sess = db_session.create_session()
    record("periodic table.txt", PeriodicTable, db_sess)
    record("acids.txt", Acids, db_sess)
    record("acid residues.txt", AcidResides, db_sess)


if __name__ == "__main__":
    main()
