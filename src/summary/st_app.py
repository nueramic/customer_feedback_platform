import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Customer Feedback Platform",
    page_icon="🧊",
    initial_sidebar_state="auto"
)

# Настройка заголовка и текста
st.title("Customer Feedback Platform")
st.header('Дэшборд с рейтингом магазина')
st.write(
    """На данном дэшборде представлена агрерированная информация на основе отзывов и рейтингов в открытом доступе.""")

# Настройка боковой панели
st.sidebar.title("О проекте")
st.sidebar.info(
    """
    На боковой панели можно найти подсказки, как пользоваться дэшбордом и настраивать фильтры.
    """
)
st.sidebar.info("Данный дэшборд уже залит на гитхаб и его можно найти по ссылке "
                "[здесь](https://github.com/nueramic/customer_feedback_platform).")

engine = create_engine('postgresql://itmoml:vcqsaw2007@90.156.210.226:5432/retail_feedback')

query = '''select name_store
            from analytic.v_feedbacks
            where name_store is not null
            group by 1
            having count(*) >= 10
            order by 1'''
shops_df = pd.read_sql(query, engine)

if 'name_store' not in st.session_state:
    # shops_df = pd.read_csv('./data/shops.csv', delimiter=';')
    st.session_state['name_store'] = shops_df.name_store
    ##shops_df.txt_name + ' : ' + shops_df.txt_address

shop_option = st.selectbox('Выберите магазин', st.session_state['name_store'])
categories = ['Свежесть продуктов', 'Цены', 'Работа персонала', 'Разнообразие ассортимента', 'Бонусная программа']


# Создадим функции для визуализации радара
def draw_radar_all(scores, avg_scores, categories, shop_option):  ## scores row_list[2:]
    fig = go.Figure()
    avg_scores = avg_scores + avg_scores[:1]
    scores = scores + scores[:1]
    categories = categories + categories[:1]
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        name=shop_option
    ))
    fig.add_trace(go.Scatterpolar(
        r=avg_scores,
        theta=categories,
        fill='toself',
        name='Средняя оценка по выборке'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=False,
        title={'text': '<b>Общая оценка магазина в сферам'}
    )
    st.plotly_chart(fig)
    return fig


def shop_selector(shop_option, engine):
    shop_df = pd.read_sql('''select name_store, count(1) cnt
                            , avg(score_overall)*3 score_overall
                            , avg(score_bonus_program)*3 score_bonus_program
                            , avg(score_freshness)*3 score_freshness
                            , avg(score_prices)*3 score_prices
                            , avg(score_staff)*3 score_staff
                            , avg(score_product_range)*3 score_product_range
                            from analytic.v_feedbacks where name_store ilike '{}\'
                            group by 1'''.format(shop_option), engine)
    # st.write(shop_df)
    score_freshness = shop_df.score_freshness[0]
    score_prices = shop_df.score_prices[0]
    score_staff = shop_df.score_staff[0]
    score_product_range = shop_df.score_product_range[0]
    score_bonus_program = shop_df.score_bonus_program[0]
    scores = [score_freshness, score_prices, score_staff, score_product_range, score_bonus_program]
    for i in range(len(scores)):
        if not (scores[i] is None):
            scores[i] += 2
        else:
            scores[i] = 2
    return scores


def avg_selector(engine, select_to_compare, shop_option):
    subquery = '''select count(1) cnt
                       , avg(score_overall)*3 score_overall
                       , avg(score_freshness)*3 score_freshness
                       , avg(score_prices)*3 score_prices
                       , avg(score_staff)*3 score_staff
                       , avg(score_product_range)*3 score_product_range
                       , avg(score_bonus_program)*3 score_bonus_program
                       from analytic.v_feedbacks'''

    if select_to_compare == 'Со всеми':
        filter_query = ''' '''
    elif select_to_compare == 'Внутри сети':
        filter_query = ''' where name_store ilike '{}%\''''.format(shop_option.split(' ')[0])
    elif select_to_compare == 'Внутри X5 Group':
        filter_query = ''' where name_store ilike 'пятерочка%\' or name_store ilike 'перекресток%\''''
    else:
        filter_query = ''' where not(name_store ilike 'пятерочка%\' or name_store ilike 'перекресток%\')'''

    query = subquery + filter_query

    avg_df = pd.read_sql(subquery, engine)
    avg_scores = [x + 2 for x in avg_df.loc[0, :].values.flatten().tolist()]
    return avg_scores[2:]


def shop_dynamic(shop_option, engine):
    df = pd.read_sql('''select date_trunc('month',
                                            case when dt_feedback ~ '[0-9]{2}-[0-9]{2}-[0-9]{4}\s+[0-9]{2}:[0-9]{2}:[0-9]{2}'
                                                    then to_timestamp(dt_feedback, 'DD-MM-YYYY HH24:MI:SS')::timestamp
                                                when substring(dt_feedback, 11) ~ '[0-9]{2}-[0-9]{2}-[0-9]{4}'
                                                    then to_timestamp(dt_feedback, 'DD-MM-YYYY')::timestamp
                                                when substring(dt_feedback, 11) ~ '[0-9]{4}-[0-9]{2}-[0-9]{2}'
                                                    then dt_feedback::timestamp
                                              end::date)::date     as "Дата отзыва"
                             , avg(2 + score_overall * 3)          as "Средняя оценка в целом"
                             , avg(2 + score_freshness * 3)         as "Свежесть продуктов"
                             , avg(2 + score_prices * 3)            as "Цены"
                             , avg(2 + score_staff * 3)             as "Работа персонала"
                             , avg(2 + score_product_range * 3)     as "Разнообразие ассортимента"
                             , avg(2 + score_bonus_program * 3)     as "Бонусная программа"
                             , count(1) as "Кол-во отзывов"
                             from analytic.v_feedbacks
                             where name_store ilike ''' + ''' '{}\'
                             group by 1
                             order by "Дата отзыва"'''.format(shop_option), engine)
    df = df[df["Средняя оценка в целом"].notna()]
    st.write(px.line(df, x="Дата отзыва",
                     y=[
                         "Средняя оценка в целом",
                         # "Свежесть продуктов",
                         # "Цены",
                         # "Работа персонала",
                         # "Разнообразие ассортимента",
                         # "Бонусная программа"
                     ], range_y=[0, 5], markers=True,
                     title='<b>Динамика оценок'))
    st.write(df)


def cards(shop_option, engine):
    df = pd.read_sql('''
        with v as ( select *, row_number() over (order by cnt_likes desc, cnt_dislikes, dtime_uploaded desc) as likes_ord
                from analytic.v_feedbacks
                where name_store ilike '{}\' )
       , ags_1 as ( select count(1)                                 as "Кол-во отзывов"
                         , count(score_overall)                     as "Кол-во оценок чатом"
                         , avg(2 + score_overall * 3)               as "Средняя общая оценка магазина"
                         , sum((2 + score_overall * 3 > 3.5)::int)  as "Кол-во положительных отзывов"
                         , sum((2 + score_overall * 3 <= 3.5)::int) as "Кол-во негативных отзывов"
                    from v )
       , ags_2 as ( select txt_overall  as "Кратко в целом"
                         , txt_feedback as "Комментарий"
                    from v
                    order by likes_ord
                    limit 1 )
       , ags_3 as ( select txt_staff as "Самый популярный отзыв на персонал"
                    from v
                    order by txt_staff is null, likes_ord
                    limit 1 )
    select *
    from ags_1
             cross join ags_2
             cross join ags_3
    '''.format(shop_option), engine)

    cols = st.columns(5)
    d = df.iloc[0].to_dict()

    cols[0].metric("Средняя оценка", round(d.get("Средняя общая оценка магазина"), 2))
    cols[1].metric("Кол-во отзывов", d.get("Кол-во отзывов"))
    cols[2].metric("Оценок чатом", d.get("Кол-во оценок чатом"))
    cols[3].metric("Позитивных отзывов", d.get("Кол-во положительных отзывов"))
    cols[4].metric("Негативных отзывов", d.get("Кол-во негативных отзывов"))

    st.write('**Краткое саммари самого популярного отзыва:** ')
    st.text(d.get('Кратко в целом').capitalize())
    st.write('**Полный отзыв:**')
    st.text(d.get('Комментарий').capitalize())
    st.write('**Самый популярный отзыв на персона:**')
    st.text(d.get('Самый популярный отзыв на персона').capitalize())


select_to_compare = st.sidebar.selectbox('С кем будем сравнивать?',
                                         ('Со всеми', 'Внутри сети', 'Внутри X5 Group', 'Со всеми конкурентами'))

draw_radar_all(shop_selector(shop_option, engine), avg_selector(engine, select_to_compare, shop_option), categories,
               shop_option)

cards(shop_option, engine)
shop_dynamic(shop_option, engine)
