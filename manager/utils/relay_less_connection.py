def get_relay_with_less_connection(components):
    less = 9999999999999
    idx = -1
    com = list(components.values())
    # print(com)
    for i, c in enumerate(com):
        if(c.get('connection') < less):
            idx = i
            less = c.get('connection')
    if(idx > -1):
        return [com[idx]]
    return []