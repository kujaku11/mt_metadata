from mt_metadata.common import Person, Copyright, Band

# p = Person()

# fields = p.get_all_fields()

# c = Copyright()

# fields_c = c.get_all_fields()

# print(fields_c)

b = Band()

fields_b = b.get_all_fields()
print(fields_b)

print(b.get_attribute_list())
print(b.attribute_information())
