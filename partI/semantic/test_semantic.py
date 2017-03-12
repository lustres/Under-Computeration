def test_small_step_semantic():
    import small_step_semantic as ss
    machine = ss.Machine(
        ss.While(
            ss.LessThan(ss.Variable('x'), ss.Number(5)),
            ss.Assign('x', ss.Multiply(ss.Variable('x'), ss.Number(3)))),
        {'x': ss.Number(1)}
    ).run()

    assert machine.environment['x'] == ss.Number(9)


def test_big_step_semantic():
    import big_step_semantic as bs
    statement = bs.While(
        bs.LessThan(bs.Variable('x'), bs.Number(5)),
        bs.Assign('x', bs.Multiply(bs.Variable('x'), bs.Number(3))))

    print(statement)
    env = statement.evaluate({'x': bs.Number(1)})
    print(env)

    assert env['x'] == bs.Number(9)
