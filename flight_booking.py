
from abc import ABC, abstractmethod


class Flight:
    """Represents a flight and manages available seats."""

    def __init__(
        self,
        flight_code: str,
        airline: str,
        source: str,
        destination: str,
        available_seats: int,
        base_fare: int,
    ):
        self._flight_code = flight_code
        self._airline = airline
        self._source = source
        self._destination = destination
        self._available_seats = available_seats
        self._base_fare = base_fare

    @property
    def flight_code(self) -> str:
        return self._flight_code

    @property
    def available_seats(self) -> int:
        return self._available_seats

    @property
    def base_fare(self) -> int:
        return self._base_fare

    @property
    def route(self) -> str:
        return f"{self._source} -> {self._destination}"

    def has_available_seats(self, tickets: int) -> bool:
        return tickets <= self._available_seats

    def reserve_seats(self, tickets: int) -> None:
        if tickets <= 0 or not self.has_available_seats(tickets):
            raise ValueError("Invalid seat reservation.")

        self._available_seats -= tickets

    def display_details(self) -> None:
        print(
            f"{self.flight_code:<10}"
            f"{self._airline:<15}"
            f"{self.route:<25}"
            f"{self.available_seats:<8}"
            f"₹{self.base_fare:,}"
        )


class Passenger(ABC):
    """Abstract base class for passengers."""

    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age

    @property
    def name(self) -> str:
        return self._name

    @property
    def age(self) -> int:
        return self._age

    @property
    @abstractmethod
    def passenger_type(self) -> str:
        pass

    @abstractmethod
    def get_discount_rate(self) -> float:
        """Return the passenger's discount rate."""
        pass


class RegularPassenger(Passenger):
    """Passenger who receives no discount."""

    @property
    def passenger_type(self) -> str:
        return "Regular"

    def get_discount_rate(self) -> float:
        return 0.0


class StudentPassenger(Passenger):
    """Student passenger who receives a 10% discount."""

    @property
    def passenger_type(self) -> str:
        return "Student"

    def get_discount_rate(self) -> float:
        return 0.10


class Booking:
    """Stores a confirmed booking and its fare details."""

    def __init__(
        self,
        booking_id: str,
        flight: Flight,
        passenger: Passenger,
        ticket_count: int,
    ):
        self._booking_id = booking_id
        self._flight = flight
        self._passenger = passenger
        self._ticket_count = ticket_count

        self._subtotal = flight.base_fare * ticket_count
        self._discount = (
            self._subtotal * passenger.get_discount_rate()
        )
        self._total_fare = self._subtotal - self._discount

    @property
    def booking_id(self) -> str:
        return self._booking_id

    def display_summary(self) -> None:
        print("\n========== BOOKING SUMMARY ==========")
        print(f"Booking ID: {self._booking_id}")
        print(
            f"Flight: {self._flight.flight_code} | "
            f"{self._flight.route}"
        )
        print(f"Airline: {self._flight._airline}")
        print(f"Passenger: {self._passenger.name}")
        print(f"Age: {self._passenger.age}")
        print(f"Passenger type: {self._passenger.passenger_type}")
        print(f"Tickets: {self._ticket_count}")
        print(f"Base fare per ticket: ₹{self._flight.base_fare:,}")
        print(f"Subtotal: ₹{self._subtotal:,.2f}")

        discount_percent = (
            self._passenger.get_discount_rate() * 100
        )

        print(
            f"{self._passenger.passenger_type} discount "
            f"({discount_percent:.0f}%): "
            f"-₹{self._discount:,.2f}"
        )
        print(f"Final amount: ₹{self._total_fare:,.2f}")
        print("=====================================")


class FlightBookingSystem:
    """Coordinates flights, passengers, bookings and the menu."""

    def __init__(self):
        self._flights = [
            Flight("PN101", "Kiran Air", "Pune", "Delhi", 20, 4000),
            Flight("MB202", "Sky India", "Mumbai", "Bengaluru", 30, 5000),
            Flight("PN303", "Air Connect", "Pune", "Hyderabad", 25, 3500),
        ]

        self._bookings = []
        self._next_booking_number = 1001

    def display_flights(self) -> None:
        print("\n================ AVAILABLE FLIGHTS ================")
        print(
            f"{'Code':<10} {'Airline':<15} "
            f"{'Route':<25} {'Seats':<8} {'Base Fare'}"
        )
        print("-" * 75)

        for flight in self._flights:
            flight.display_details()

    def find_flight_by_code(self, flight_code: str):
        code = flight_code.strip().upper()

        for flight in self._flights:
            if flight.flight_code == code:
                return flight

        return None

    def validate_booking_details(
        self,
        flight: Flight,
        name: str,
        age: int,
        ticket_count: int,
    ) -> bool:
        if flight is None:
            print("Booking failed: Invalid flight code.")
            return False

        if not name.strip():
            print("Booking failed: Passenger name cannot be blank.")
            return False

        if age <= 0:
            print("Booking failed: Age must be greater than zero.")
            return False

        if ticket_count <= 0:
            print("Booking failed: Ticket count must be greater than zero.")
            return False

        if not flight.has_available_seats(ticket_count):
            print("Booking failed: Not enough seats available.")
            print("Available seats remain unchanged.")
            return False

        return True

    def calculate_fare(
        self,
        passenger: Passenger,
        flight: Flight,
        ticket_count: int,
    ) -> dict:
        subtotal = flight.base_fare * ticket_count
        discount = subtotal * passenger.get_discount_rate()

        return {
            "subtotal": subtotal,
            "discount": discount,
            "total": subtotal - discount,
        }

    def confirm_booking(
        self,
        flight: Flight,
        passenger: Passenger,
        ticket_count: int,
    ) -> Booking:
        booking_id = f"BK{self._next_booking_number}"

        booking = Booking(
            booking_id,
            flight,
            passenger,
            ticket_count,
        )

        flight.reserve_seats(ticket_count)
        self._bookings.append(booking)
        self._next_booking_number += 1

        return booking

    def book_flight(self) -> None:
        flight_code = input("Enter flight code: ").strip()
        flight = self.find_flight_by_code(flight_code)

        name = input("Enter passenger name: ").strip()

        try:
            age = int(input("Enter age: "))
            ticket_count = int(input("Enter number of tickets: "))
        except ValueError:
            print("Booking failed: Age and ticket count must be integers.")
            return

        passenger_choice = input(
            "Passenger type (Regular/Student): "
        ).strip().lower()

        if passenger_choice == "regular":
            passenger_class = RegularPassenger
        elif passenger_choice == "student":
            passenger_class = StudentPassenger
        else:
            print("Booking failed: Choose Regular or Student.")
            return

        if not self.validate_booking_details(
            flight, name, age, ticket_count
        ):
            return

        passenger = passenger_class(name, age)

        booking = self.confirm_booking(
            flight, passenger, ticket_count
        )

        print("\nBooking confirmed!")
        booking.display_summary()

    def display_latest_booking(self) -> None:
        if not self._bookings:
            print("No confirmed bookings found.")
            return

        self._bookings[-1].display_summary()

    def run(self) -> None:
        print("Welcome to Kiran Air Booking")

        while True:
            print("\n1. View Flights")
            print("2. Book Flight")
            print("3. View Booking")
            print("4. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.display_flights()

            elif choice == "2":
                self.book_flight()

            elif choice == "3":
                self.display_latest_booking()

            elif choice == "4":
                print("Thank you for using Kiran Air Booking!")
                break

            else:
                print("Invalid choice. Please select 1, 2, 3 or 4.")


if __name__ == "__main__":
    app = FlightBookingSystem()
    app.run()
