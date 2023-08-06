import math


class CustomPagination:
    """ Custom Pagination class """

    def get_pagination_index(self, page_number, rows_count):
        """ Returns the start and end values of a page """

        # pagination parameters 
        start = (page_number - 1) * rows_count
        end   = page_number * rows_count

        return start, end


    def get_number_of_pages_in_pagination(self, total_count, rc):
        ''' Get number of pages in pagination '''
        return math.ceil(total_count / rc)


    def get_paginated_data(self, queryset, pn, rc):
        """ Get the paginated data of global queryset """

        start, end = self.get_pagination_index(pn, rc)
        return queryset[start: end]
