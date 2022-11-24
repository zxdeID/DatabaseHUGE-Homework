    sql = '''
    select P.hid,D.diseaseGet
    from people P, disease_suffered D
    where P.hid = D.hid and P.hid in
    (select B.hid
    from disease_list B
    where B.name = '{}'
    )
    '''.format(dise)