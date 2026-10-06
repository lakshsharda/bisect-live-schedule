# shiftkit

Small shift-scheduling and booking library. Times are minutes since midnight.

## Rules

- Times are minutes since midnight; `hhmm("09:30")` gives 570.
- A shift that ends before it starts runs overnight.
- Overtime is anything beyond 40 hours in a week.
- Bookings of the same resource need a 10 minute buffer by default.
