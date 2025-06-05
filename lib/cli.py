import time
from datetime import datetime
from typing import Optional
from sqlalchemy import select, delete
from db.models import Trip, Booking, Activity, session, Base, engine
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import track
from rich.style import Style
from rich.markdown import Markdown

# Initialize Rich console
console = Console()

# Define styles
error_style = Style(color="red", bold=True)
success_style = Style(color="green", bold=True)
warning_style = Style(color="yellow")
highlight_style = Style(bold=True, underline=True)

def initialize_database():
    """Create database tables if they don't exist"""
    with console.status("[bold green]Initializing database...[/bold green]"):
        Base.metadata.create_all(engine)
        time.sleep(1)  # Simulate work for progress visualization
    console.print("[green]✓ Database initialized successfully![/green]")

def list_trips():
    """Display all trips in a rich table"""
    trips = session.scalars(select(Trip)).all()
    
    if not trips:
        console.print("[bold red]No trips found.[/bold red]")
        return
    
    table = Table(title="✈️ Your Trips", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Destination", style="green")
    table.add_column("Start Date", style="yellow")
    table.add_column("End Date", style="yellow")
    table.add_column("Duration", justify="right")
    
    for trip in trips:
        duration = (trip.end_date - trip.start_date).days + 1
        table.add_row(
            str(trip.id),
            f"[bold]{trip.destination}[/bold]",
            str(trip.start_date),
            str(trip.end_date),
            f"{duration} days"
        )
    
    console.print(table)

def add_trip():
    """Add a new trip with rich prompts"""
    console.print(Panel("➕ Add New Trip", style="bold blue"))
    
    destination = Prompt.ask("🏝️ [bold]Destination[/bold]")
    
    while True:
        start_date = Prompt.ask("📅 [bold]Start date[/bold] (YYYY-MM-DD)")
        end_date = Prompt.ask("📅 [bold]End date[/bold] (YYYY-MM-DD)")
        
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
            
            if end_date_obj < start_date_obj:
                console.print("[red]Error: End date must be after start date[/red]")
                continue
                
            trip = Trip(
                destination=destination, 
                start_date=start_date_obj, 
                end_date=end_date_obj
            )
            session.add(trip)
            session.commit()
            console.print(f"[green]✓ Added trip to [bold]{destination}[/bold] (ID: {trip.id})[/green]")
            break
        except ValueError:
            console.print("[red]Invalid date format. Please use YYYY-MM-DD.[/red]")

def update_trip():
    """Update trip details with rich interface"""
    console.print(Panel("🔄 Update Trip", style="bold blue"))
    list_trips()
    
    try:
        trip_id = Prompt.ask("\nEnter trip ID to update", default="0")
        trip = session.get(Trip, int(trip_id))
        
        if not trip:
            console.print("[red]✗ No trip found with that ID[/red]")
            return

        console.print("\n[bold]Leave blank to keep current value:[/bold]")
        new_destination = Prompt.ask(
            f"Destination [[{trip.destination}]]",
            default=trip.destination
        )
        
        new_start_date = Prompt.ask(
            f"Start date [[{trip.start_date}]] (YYYY-MM-DD)",
            default=str(trip.start_date)
        )
        
        new_end_date = Prompt.ask(
            f"End date [[{trip.end_date}]] (YYYY-MM-DD)",
            default=str(trip.end_date)
        )

        # Update fields if changed
        if getattr(trip, "destination") != new_destination:
            setattr(trip, "destination", new_destination)
        
        try:
            start_date = datetime.strptime(new_start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(new_end_date, "%Y-%m-%d").date()
            
            if end_date < start_date:
                console.print("[red]Error: End date must be after start date[/red]")
                return
            
            setattr(trip, "start_date", start_date)
            setattr(trip, "end_date", end_date)
            
            session.commit()
            console.print("[green]✓ Trip updated successfully![/green]")
        except ValueError:
            console.print("[red]Invalid date format. Changes not saved.[/red]")
            
    except ValueError:
        console.print("[red]Invalid input. Please enter a number.[/red]")

def delete_trip():
    """Delete a trip with confirmation"""
    console.print(Panel("❌ Delete Trip", style="bold red"))
    list_trips()
    
    try:
        trip_id = Prompt.ask("\nEnter trip ID to delete", default="0")
        trip = session.get(Trip, int(trip_id))
        
        if not trip:
            console.print("[red]✗ No trip found with that ID[/red]")
            return
        
        console.print(Panel.fit(
            f"[bold]You are about to delete:[/bold]\n"
            f"Destination: [red]{trip.destination}[/red]\n"
            f"Dates: {trip.start_date} to {trip.end_date}\n"
            f"This will also delete {len(trip.activities)} activities and {len(trip.bookings)} bookings",
            title="⚠️ Warning",
            border_style="red"
        ))
        
        if Confirm.ask("[bold red]Are you sure?[/bold red]", default=False):
            with console.status("[red]Deleting trip...[/red]"):
                session.execute(delete(Booking).where(Booking.trip_id == trip.id))
                session.execute(delete(Activity).where(Activity.trip_id == trip.id))
                session.delete(trip)
                session.commit()
                time.sleep(1)
            console.print("[green]✓ Trip deleted successfully![/green]")
        else:
            console.print("[yellow]Deletion cancelled[/yellow]")
    except ValueError:
        console.print("[red]Invalid input. Please enter a number.[/red]")

def trip_details():
    """Show detailed trip information"""
    console.print(Panel("🔍 Trip Details", style="bold blue"))
    list_trips()
    
    try:
        trip_id = Prompt.ask("\nEnter trip ID to view details", default="0")
        trip = session.get(Trip, int(trip_id))
        
        if not trip:
            console.print("[red]✗ No trip found with that ID[/red]")
            return
        
        # Main trip panel
        console.print(Panel.fit(
            f"[bold green]{trip.destination}[/bold green]\n"
            f"📅 [bold]Dates:[/bold] {trip.start_date} to {trip.end_date}\n"
            f"⏱️ [bold]Duration:[/bold] {(trip.end_date - trip.start_date).days + 1} days",
            title="Trip Overview",
            border_style="blue"
        ))
        
        # Bookings section
        bookings = session.scalars(select(Booking).where(Booking.trip_id == trip.id)).all()
        if bookings:
            bookings_table = Table(title="📚 Bookings", show_lines=True)
            bookings_table.add_column("Type", style="cyan")
            bookings_table.add_column("Details", style="white")
            for booking in bookings:
                if getattr(booking, "flight", None) is not None and getattr(booking, "flight") != "":
                    bookings_table.add_row("✈️ Flight", str(getattr(booking, "flight")))
                if getattr(booking, "hotel", None) is not None and getattr(booking, "hotel") != "":
                    bookings_table.add_row("🏨 Hotel", str(getattr(booking, "hotel")))
            console.print(bookings_table)
        else:
            console.print("[italic]No bookings added yet.[/italic]")
        
        # Activities section
        activities = session.scalars(
            select(Activity)
            .where(Activity.trip_id == trip.id)
            .order_by(Activity.date, Activity.time)
        ).all()
        
        if activities:
            console.print("\n[bold underline]📅 Itinerary:[/bold underline]")
            current_date = None
            for activity in activities:
                activity_date = getattr(activity, "date", None)
                if activity_date != current_date:
                    console.print(f"\n[bold yellow]{activity_date}[/bold yellow]")
                    current_date = activity_date
                activity_time = getattr(activity, "time", None)
                activity_name = getattr(activity, "name", "")
                console.print(
                    f"  ⏰ [cyan]{activity_time.strftime('%H:%M') if activity_time is not None else 'All day':<6}[/cyan] "
                    f"- [bold]{activity_name}[/bold]"
                )
        else:
            console.print("[italic]No activities planned yet.[/italic]")
            
    except ValueError:
        console.print("[red]Invalid input. Please enter a number.[/red]")

def add_activity():
    """Add an activity to a trip"""
    console.print(Panel("➕ Add Activity", style="bold blue"))
    list_trips()
    
    try:
        trip_id = Prompt.ask("\nEnter trip ID to add activity", default="0")
        trip = session.get(Trip, int(trip_id))
        
        if not trip:
            console.print("[red]✗ No trip found with that ID[/red]")
            return
            
        name = Prompt.ask("🎯 [bold]Activity name[/bold]")
        
        while True:
            date_str = Prompt.ask("📅 [bold]Date[/bold] (YYYY-MM-DD)")
            time_str = Prompt.ask("⏰ [bold]Time[/bold] (HH:MM, leave blank if all day)", default="")
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
                
            trip_start = getattr(trip, "start_date")
            trip_end = getattr(trip, "end_date")
            if date < trip_start or date > trip_end:
                console.print(f"[red]✗ Date must be between {trip_start} and {trip_end}[/red]")
                continue
                
                time_obj = datetime.strptime(time_str, "%H:%M").time() if time_str else None
                    
                time_obj = datetime.strptime(time_str, "%H:%M").time() if time_str else None
                
                activity = Activity(
                    name=name, 
                    date=date, 
                    time=time_obj, 
                    trip_id=trip.id
                )
                session.add(activity)
                session.commit()
                console.print(f"[green]✓ Added activity '[bold]{name}[/bold]' to trip ID {trip.id}[/green]")
                break
    except ValueError:
            console.print("[red]✗ Invalid format. Use YYYY-MM-DD for date and HH:MM for time.[/red]")

def add_booking():
    """Add booking information"""
    console.print(Panel("➕ Add Booking", style="bold blue"))
    list_trips()
    
    try:
        trip_id = Prompt.ask("\nEnter trip ID to add booking", default="0")
        trip = session.get(Trip, int(trip_id))
        
        if not trip:
            console.print("[red]✗ No trip found with that ID[/red]")
            return
            
        flight = Prompt.ask("✈️ [bold]Flight details[/bold] (leave blank if none)", default="")
        hotel = Prompt.ask("🏨 [bold]Hotel details[/bold] (leave blank if none)", default="")
        
        if not flight and not hotel:
            console.print("[yellow]No booking details provided. Nothing was added.[/yellow]")
            return
            
        booking = Booking(
            flight=flight if flight else None,
            hotel=hotel if hotel else None,
            trip_id=trip.id
        )
        session.add(booking)
        session.commit()
        console.print("[green]✓ Booking added successfully![/green]")
    except ValueError:
        console.print("[red]Invalid input. Please enter a number.[/red]")

def main_menu():
    """Main menu with rich interface"""
    initialize_database()
    
    menu_options = {
        "1": ("List Trips", list_trips),
        "2": ("Add Trip", add_trip),
        "3": ("Update Trip", update_trip),
        "4": ("Delete Trip", delete_trip),
        "5": ("Trip Details", trip_details),
        "6": ("Add Activity", add_activity),
        "7": ("Add Booking", add_booking),
        "0": ("Exit", None)
    }
    
    while True:
        console.print(Panel.fit(
            "[bold blue]🌍 Travel Itinerary Planner[/bold blue]",
            subtitle="[italic]Your personal travel organizer[/italic]",
            border_style="blue"
        ))
        
        for key, (text, _) in menu_options.items():
            console.print(f"[cyan][{key}][/cyan] {text}")
        
        choice = Prompt.ask(
            "\n[bold]Your choice[/bold]", 
            choices=list(menu_options.keys()),
            show_choices=False
        )
        
        if choice == "0":
            console.print(Panel.fit(
                "[bold green]Thank you for using Travel Itinerary Planner![/bold green]\n"
                "Safe travels! ✈️",
                border_style="green"
            ))
            session.close()
            break
            
        menu_options[choice][1]()

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[red]Program interrupted. Exiting gracefully...[/red]")
        session.close()
    except Exception as e:
        console.print(f"[red]An error occurred: {str(e)}[/red]")
        session.close()