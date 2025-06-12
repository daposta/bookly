def timesheetSum(path):
    """
    Calculate total hours from a timesheet file.

    Args:
        path (str): Path to the timesheet text file

    Returns:
        float: Total hours worked
    """

    def parse_time(time_str):
        """Convert time string to decimal hours (0-23.75)"""
        if ":" in time_str:
            hours, minutes = map(int, time_str.split(":"))
        else:
            hours = int(time_str)
            minutes = 0

        
        decimal_minutes = minutes / 60.0
        return hours + decimal_minutes

    def is_military_time(time_str):
        """Determine if a time string represents military time (24-hour format)"""
        hour = int(time_str.split(":")[0])
        return hour > 12

    def calculate_duration(start_str, end_str):
        """Calculate duration between start and end times"""
        start_time = parse_time(start_str)
        end_time = parse_time(end_str)

        # Check if either time uses military format
        military_format = is_military_time(start_str) or is_military_time(end_str)

        if military_format:
            # In military time, calculate directly
            if end_time < start_time:
                # Handle case where end time is next day
                duration = (24 - start_time) + end_time
            else:
                duration = end_time - start_time
        else:
            # In 12-hour format, find the shortest positive duration
            # This handles cases like 10-1 (could be 10 AM to 1 PM or 10 PM to 1 AM)
            if end_time <= start_time:
                # End time is next occurrence after start time
                duration = (12 - start_time) + end_time
                if duration > 12:
                    duration = end_time - start_time + 12
            else:
                duration = end_time - start_time

        return duration

    def process_line(line):
        """Process a single line containing one or more time ranges"""
        line = line.strip()
        if not line:
            return 0.0

        total_hours = 0.0

        # Split by comma to get individual ranges
        ranges = [r.strip() for r in line.split(",")]

        for range_str in ranges:
            if "-" in range_str:
                # Split by dash to get start and end times
                parts = range_str.split("-")
                if len(parts) == 2:
                    start_str = parts[0].strip()
                    end_str = parts[1].strip()

                    duration = calculate_duration(start_str, end_str)
                    total_hours += duration

        return total_hours

    # Read the file and process each line
    total_hours = 0.0

    try:
        with open(path, "r") as file:
            for line in file:
                line_hours = process_line(line)
                total_hours += line_hours
    except FileNotFoundError:
        raise FileNotFoundError(f"Timesheet file not found: {path}")
    except Exception as e:
        raise Exception(f"Error processing timesheet: {e}")

    return total_hours


# Test function with the provided example
def test_example():
    """Test the function with the example data"""
    # Create a test file content
    test_content = """10-11, 11:30-4, 5-6
7:45-8:30, 10-2
8-11:30
6-9
10:30-12, 1:30-2
11-1:30, 5-8, 9-10
10-14, 17:30-21:30
"""

    # Write test file
    with open("test_timesheet.txt", "w") as f:
        f.write(test_content)

    # Test the function
    result = timesheetSum("test_timesheet.txt")
    print(f"Total hours: {result}")

    # Clean up
    import os

    os.remove("test_timesheet.txt")

    return result


# Run the test
if __name__ == "__main__":
    test_result = test_example()
    print(f"Expected: 34.25, Got: {test_result}")
