from idb import db
from sqlalchemy import or_


def gen_query(relation, items_per_page, page, sort, order, attribute=None, filter_string=""):
    query = db.session.query(relation)
    if order == 'desc':
        query = query.order_by(getattr(relation, sort).desc())
    else:
        query = query.order_by(getattr(relation, sort))

    if attribute is not None and filter_string != "":
        query = query.filter(attribute == filter_string)
    elif filter_string != "":
        query = query.filter(relation.name.ilike("%" + filter_string + "%"))
    query = (query
             .limit(items_per_page)
             .offset((page - 1) * items_per_page))
    return query


def gen_query_f(relation, items_per_page, page, sort, order, attributes=[], filter_string=""):
    query = db.session.query(relation)
    if order == 'desc':
        query = query.order_by(getattr(relation, sort).desc())
    else:
        query = query.order_by(getattr(relation, sort))
    # query = gen_query(relation, items_per_page, page, sort, order)
    if len(attributes) > 0 and filter_string != "":
        query = query.filter(or_(filter_string == a for a in attributes))
    query = (query
             .limit(items_per_page)
             .offset((page - 1) * items_per_page))
    return query
