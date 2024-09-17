from . import types

# people
Alice   = types.Person("Alice",   0)
Bob     = types.Person("Bob",     1)
Charlie = types.Person("Charlie", 2)
Dan     = types.Person("Dan",     3)

Mathematician = types.Person("Mathematician", 4)
Physicist     = types.Person("Physicist",     5)
Engineer      = types.Person("Engineer",      6)
Philosopher   = types.Person("Philosopher",   7)

# responses
Foo = types.Response("foo")
Bar = types.Response("bar")
Baz = types.Response("baz")

# fields
Math = types.Field("Mathematics")
Phys = types.Field("Physics")
Engg = types.Field("Engineering")
Phil = types.Field("Philosophy")