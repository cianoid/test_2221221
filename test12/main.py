import pandas


def run():
    key_square = "Площадь"
    key_price = "Цена, руб"
    key_number = "Номер квратиры"

    # Прочтем данные из подготовленного файла
    df_initial = pandas.read_csv("flats.csv", index_col=key_number)

    # Зададим фильтр, отсекающий нулевые значения цен и площадей
    filter_notnull = df_initial[key_price].notnull() & df_initial[key_square].notnull()
    # Данные без площади и стоимости вынесем в отдельный фрейм df_excluded,
    # корректные данные идут в df
    df, df_excluded = df_initial[filter_notnull], df_initial[~filter_notnull]

    # Подсчет стандартного отклонения цен
    price_std = df[key_price].std()
    # Подсчет среднего значения цен всех квартир
    mean = df[key_price].mean()
    # Определение диапазона цен. Если цена квартиры выходит за пределы данного
    # диапазона, то возможно она аномальная (слишком высокая, либо слишком низкая).
    price_range = (mean - 3 * price_std, mean + 3 * price_std)
    # Зададим фильтр, отсекающий квартиры, у которых цена не входит в диапазон
    filter_price = df[key_price].between(*price_range)
    df, df_excluded2 = df[filter_price], df[~filter_price]

    if len(df_excluded) > 0:
        print("Стоимость квартиры не указана (данные исключены из оценки):")
        print(df_excluded, end="\n\n")
    if len(df_excluded2) > 0:
        print("Стоимость квартиры аномальна (данные исключены из оценки):")
        print(df_excluded2, end="\n\n")

    # Получим уникальный список площадей.
    unique_square = sorted(df[key_square].unique())

    for square in unique_square:
        # Определим DataFrame с квартирами конкретной площади.
        df_square = df[df[key_square] == square]
        # Выясним среднюю цену на квартиру, а также минимальную и максимальную.
        flat_price_mean = df_square[key_price].mean()
        flat_price_min = df_square[key_price].min()
        flat_price_max = df_square[key_price].max()
        # Выясним среднюю цену за квадратный метр
        meter_price_mean = flat_price_mean / square

        print(f"\nПлощадь, кв.м.: {square}")
        print(f"Средняя цена квартиры, руб.: {flat_price_mean:,.0f}")
        print(f"Разброс цен, руб.: {flat_price_min:,.0f} - {flat_price_max:,.0f}")
        print(f"Средняя цена квадратного метра, руб.: {meter_price_mean:,.0f}")


if __name__ == "__main__":
    run()
