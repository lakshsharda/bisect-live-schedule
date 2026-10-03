import pytest

from shiftkit.bookings import BookingBook, BookingConflict
from shiftkit.slots import Slot


def test_book_and_list_slots_in_order():
    book = BookingBook()
    book.book("room-1", Slot(600, 660))
    book.book("room-1", Slot(540, 570))
    assert book.slots_for("room-1") == [Slot(540, 570), Slot(600, 660)]


def test_overlapping_booking_is_rejected():
    book = BookingBook()
    book.book("room-1", Slot(540, 600))
    with pytest.raises(BookingConflict):
        book.book("room-1", Slot(570, 630))


def test_other_resources_are_independent():
    book = BookingBook()
    book.book("room-1", Slot(540, 600))
    book.book("room-2", Slot(540, 600))
    assert len(book.slots_for("room-2")) == 1


def test_cancel_frees_the_slot():
    book = BookingBook()
    book.book("room-1", Slot(540, 600))
    book.cancel("room-1", Slot(540, 600))
    book.book("room-1", Slot(540, 600))


def test_cancel_of_unknown_booking_raises():
    with pytest.raises(KeyError):
        BookingBook().cancel("room-1", Slot(540, 600))
