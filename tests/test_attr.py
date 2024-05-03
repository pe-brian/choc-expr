from choc_expr import Attr


def test_attr_attr():

    class C:
        def __init__(self) -> None:
            self.val = 42

    class B:
        def __init__(self) -> None:
            self.c = C()

    class A:
        def __init__(self) -> None:
            self.b = B()

    class Box:
        def __init__(self) -> None:
            self.items = (A(), A(), A())

    class MainBox:
        def __init__(self) -> None:
            self.box = Box()
            self.items = (1, 2, 3)
            self.val = 1

    box = Box()
    main_box = MainBox()

    assert Attr(main_box, "val").build() == "1"
    assert Attr(main_box, "$(items)").build() == "1, 2, 3"
    assert Attr(box, "$(items).b.c.val").build() == "42, 42, 42"
    assert Attr(box, "$(items).b.c.val").build() == "42, 42, 42"
    assert Attr(main_box, "$(box.items).b.c.val").build() == "42, 42, 42"
    assert Attr(main_box, "$(box.items).b.c.val~").build() == "42, 42, 42\n"


def test_attr_attr_endline():

    class Container:
        def __init__(self) -> None:
            self.val = 1

    box = Container()

    assert Attr(box, "val~").build() == "1\n"


def test_attr_attr_empty_endline():

    class Container:
        def __init__(self) -> None:
            self.val = ""

    box = Container()

    assert Attr(box, "val~").build() == ""
