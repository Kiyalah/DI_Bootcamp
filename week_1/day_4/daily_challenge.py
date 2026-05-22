import math


class Pagination:
    def __init__(self, items=None, page_size=10):
        if items is None:
            items = []

        self.items = items
        self.page_size = page_size
        self.current_idx = 0
        self.total_pages = math.ceil(len(self.items) / self.page_size)

    def get_visible_items(self):
        start = self.current_idx * self.page_size
        end = start + self.page_size

        return self.items[start:end]

    def go_to_page(self, page_num):
        page_num = int(page_num)

        if page_num < 1 or page_num > self.total_pages:
            raise ValueError("Page number out of range.")

        self.current_idx = page_num - 1
        return self

    def first_page(self):
        self.current_idx = 0
        return self

    def last_page(self):
        self.current_idx = self.total_pages - 1
        return self

    def next_page(self):
        if self.current_idx < self.total_pages - 1:
            self.current_idx += 1

        return self

    def previous_page(self):
        if self.current_idx > 0:
            self.current_idx -= 1

        return self

    def __str__(self):
        return "\n".join(self.get_visible_items())


alphabetList = list("abcdefghijklmnopqrstuvwxyz")

p = Pagination(alphabetList, 8)

print(p.get_visible_items())
# ['a', 'b', 'c', 'd']


p.next_page()

print(p.get_visible_items())
# ['e', 'f', 'g', 'h']


p.last_page()

print(p.get_visible_items())
# ['y', 'z']


try:
    p.go_to_page(10)

except ValueError as error:
    print(error)


try:
    p.go_to_page(0)

except ValueError as error:
    print(error)


print(p.first_page())


print(
    p.next_page()
     .next_page()
     .next_page()
     .get_visible_items()
)

# ['m', 'n', 'o', 'p']