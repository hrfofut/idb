from idb import db


def gen_query(relation, items_per_page, page, sort, order, filter=""):
    query = db.session.query(relation)
    if order == 'desc':
        query = query.order_by(getattr(relation, sort).desc())
    else:
        query = query.order_by(getattr(relation, sort))
    query = query.filter(relation.name.ilike("%" + filter + "%"))
    query = (query
             .limit(items_per_page)
             .offset((page - 1) * items_per_page))
    return query