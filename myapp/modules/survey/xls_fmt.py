# -*- coding: UTF-8 -*-


XLS_FMT = [
    {
        "name": "survey_questions",
        "key_col": ["survey_id", "question_id"],
        "columns": {
            u"问卷编号": "survey_id",
            u"问题序号": "question_id",
            u"问题": "question_name",
            u"答案类型": "col_type",
            u"答案值类型": "value_type",
            u"可选答案": "values"
        },
    }
]


def get_fmt_by_name(name):
    f = XLS_FMT
    return (item for item in f if item['name'] == name).next()


def get_data_from_xls(table_name, df):
    '''
        read xls:
            df = pd.read_excel('le.xls', sheet_name=u'课表')
            r = df.to_json(
                orient='records', date_format='None')
            data = json.loads(jj)
    '''
    col_name = get_fmt_by_name(table_name)['columns']
    df1 = df.rename(columns=col_name)
    data = df1.to_json(orient='records', date_format='None')
    data_dict = json.loads(data)
    return data_dict


def save_xls_to_db(table_name, dataframe):
    '''
        save data to db
        input:
            data: list of dict
    '''
    data = get_data_from_xls(table_name, dataframe)
    if len(data) == 0:
        return dict(status='error', msg='no data in xls')
    data_col = [k for k, v in data[0].items()]
    m = get_model_by_table(table_name)
    #: compare xls column and model column
    m_dict = get_fmt_by_name(table_name)['columns']
    m_col = [v for k, v in m_dict.items()]
    if not operator.eq(data_col.sort(), m_col.sort()):
        return dict(status='error', msg='error colume in xls')
    col_name = get_filter_col(table_name)
    updated = new_record = 0
    for x in data:
        q_s = ['%s;eq;%s' % (q, str(x[q])) for q in col_name]
        # print q_s
        query_s = filter_query(m, q_s)
        r = query_s.one_or_none()
        if r:
            query_s.update(x)
            updated = updated + 1
            # print '...update'
        else:
            new_r = m(**x)
            db.session.add(new_r)
            new_record = new_record + 1
            # print '...new'
    db.session.flush()
    db.session.commit()
    return dict(status='success', updated=updated, new_record=new_record)


def get_model_by_table(table_name):
    """Return class reference mapped to table.

    :param tablename: String with name of table.
    :return: Class reference or None.
    """
    for c in Base._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == table_name:
            return c


def get_filter_col(table_name):
    """
    table unique key
    output:
         [
        "week_no",
        "day_no"
        ]
    """
    t = get_fmt_by_name(table_name)
    return t['key_col']


def filter_query(m, raw_filters):
    '''
        construct query
        https://stackoverflow.com/questions/14845196/dynamiclistally-constructing-filters-in-sqlalchemy

        input:
            raw_filters = ['age;in;5,6,7', 'id;ge;10']
        output:
            query: <class 'flask_sqlalchemy.BaseQuery'>
            result = query.all()/ query.one_or_none()


        from app.controllers.learning import *
        save_to_db('learning_schedule', 'le.xls')
    '''
    sep = ';'
    model_class = m  # returns the query's Model
    fl = []
    query = m.query
    for raw in raw_filters:
        try:
            key, op, value = raw.split(sep, 3)
        except ValueError:
            return 'Invalid filter: %s' % raw
        column = getattr(model_class, key, None)
        if not column:
            return 'Invalid filter column: %s' % key
        if op == 'in':
            filt = column.in_(value.split(','))
        else:
            try:
                # attr = filter(
                #     lambda e: hasattr(column, e % op),
                #     ['%s', '%s_', '__%s__']
                # )[0] % op
                attr = list(filter(
                    lambda e: hasattr(column, e % op),
                    ['%s', '%s_', '__%s__']
                ))[0] % op
            except IndexError:
                return 'Invalid filter operator: %s' % op
            if value == 'null':
                value = None
            filt = getattr(column, attr)(value)
            fl.append(filt)
            # print 'filt', filt, 'value', value
        query = query.filter(filt)
    # print type(query), query
    return query
