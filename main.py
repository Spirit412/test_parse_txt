from __future__ import annotations
import pandas as pd
from pandas import DataFrame
import toml
import os
config = toml.load("config.toml")


def get_dataframe(path: str) -> DataFrame:
    return pd.read_table(path, delim_whitespace=False, skiprows=9,
                         low_memory=False,
                         )


if __name__ == "__main__":
    headers1 = ['SNP Name', 'Sample ID', 'Alleles']
    headers2 = ['SNP Name', 'Sample ID', 'Allele1 - AB', 'Allele2 - AB']
    df = get_dataframe(os.path.normpath(str(config['file']['path_report_file'])))
    # Условие: Необходимо преобразить данные из файла в таблицу: все уникальные “SNP Name” представить как столбцы,
    # ID животных как строчки, а в качестве значений записать значения столбцов аллелей, соединенные в пару (AA/AB/BB).
    df['Alleles'] = df['Allele1 - Forward'].astype(str) + df['Allele2 - Forward'].astype(str) + "/" + df[
        'Allele1 - Top'].astype(str) + df['Allele2 - Top'].astype(str) + "/" + df['Allele1 - AB'].astype(str) + df[
                        'Allele2 - AB'].astype(str)
    ##################
    print("Задача1:\n", df[headers1])
    # out
    #                    SNP Name  Sample ID   Alleles
    # 0        15k_OAR11_36199784      23004  AA/AA/AA
    ##################
    print("Задача2:\n", df[headers2])
    # out
    #                    SNP Name  Sample ID Allele1 - AB Allele2 - AB
    # 0        15k_OAR11_36199784      23004            A            A
    # 1        15k_OAR11_54939690      23004            -            -
    # 2        15k_OAR11_56897973      23004            A            A
    ##################

    # Запись в json
    # Условие: В столбце “Sample ID” — животные. В столбцах “Allele1 - AB” и “Allele2 - AB” содержатся значения A и B.
    # В столбце “SNP Name” — названия позиций, которые полностью повторяются для каждого животного в файле.
    df[headers1].head(3).to_json('./test1.json', orient='columns')
    df[headers2].head(3).to_json('./test2.json', orient='columns')
