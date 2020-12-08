from times import compute_overlap_time
from times import time_range


def test_given_input():
    if __name__ == "__main__":
        large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")

        short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)

        result = compute_overlap_time(large, short)
        expected = [('2010-01-12 10:30:00', '2010-01-12 10:37:00'),
                    ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]
        assert result == expected


def test_later_start_time():
    with raises(ValueError) as exception:
        time_range("2010-01-12 10:00:00", "2010-01-10 12:00:00")
        exception.match("end time larger than start time")


def test_no_overlap():

    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-13 10:30:00", "2010-01-13 10:45:00")

    result = compute_overlap_time(large, short)
    expected = []
    assert result == expected


large1 = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
small1 = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
expected1 = [('2010-01-12 10:30:00', '2010-01-12 10:37:00'),
             ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]

large2 = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
small2 = time_range("2010-01-13 10:30:00", "2010-01-13 10:45:00")
expected2 = []

large1 = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00",)
small1 = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
expected1 = [('2010-01-12 10:30:00', '2010-01-12 10:37:00'),
             ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]


# @pytest.mark.parametrize("large,short,expected",
#                         [(large1, small1, expected1), (large2, small2, expected2)])
# def test_general_overlap(large, short, expected):
#    result = compute_overlap_time(large, short)
#    assert result == expected
