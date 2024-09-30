def get_relay_with_less_connection(components):
    less = 9999999999999
    idx = -1
    com = list(components.values())
    # print(components)
    # print(f"GRWLS: {com}")
    for i, c in enumerate(com):
        if(c.get('connection') < less):
            idx = i
            less = c.get('connection')
    if(idx > -1):
        # print(f"GRWLS: {com[idx]}")
        return [com[idx]]
    return []