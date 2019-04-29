def arraypermute(collection, key):
    return [ str(i) + str(j) for i in collection for j in key ]


class FilterModule(object):
    def filters(self):
        return {
            'arraypermute': arraypermute
        }