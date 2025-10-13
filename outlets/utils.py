from datetime import datetime, timedelta
from bookings.models import Booking  # adjust import path if needed

DURATION_MINUTES = 45  # default duration of each booking

def can_book_outlet_at(outlet, booking_date, booking_time):
    """
    Check if a booking can be made at the given outlet, date, and time.

    Returns:
        (True, None) if booking is allowed
        (False, message) if booking is not allowed
    """

    # 1. Check if outlet is closed
    if outlet.is_closed:
        return False, "This outlet is closed on the selected date/time."

    # 2. Check if booking time is within opening hours
    req_time = booking_time
    if req_time < outlet.opening_time or req_time >= outlet.closing_time:
        return False, "Selected time is outside the outlet's working hours."

    # 3. Compute start and end datetime for requested booking
    req_start_dt = datetime.combine(booking_date, booking_time)
    req_end_dt = req_start_dt + timedelta(minutes=DURATION_MINUTES)

    # 4. Fetch all bookings for this outlet on this date
    same_day_bookings = Booking.objects.filter(outlet=outlet, booking_date=booking_date)

    # 5. Count overlapping bookings
    overlapping_count = 0
    for b in same_day_bookings:
        if not b.booking_time:
            continue
        b_start = datetime.combine(b.booking_date, b.booking_time)
        b_end = b_start + timedelta(minutes=DURATION_MINUTES)
        # Overlap occurs if start < req_end and end > req_start
        if b_start < req_end_dt and b_end > req_start_dt:
            overlapping_count += 1

    # 6. Check against total slots
    if overlapping_count >= outlet.total_slots:
        return False, "No slots available at this time. Please choose another time."

    # 7. Booking is allowed
    return True, None
